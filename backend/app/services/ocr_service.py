"""
Dependencies:
- Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
- Windows Version: tesseract-ocr-w64-setup-5.3.4.20240503.exe
- macOS: brew install tesseract-lang

Language Support: 
- chi_sim+eng


Environment Variables:
- TESSERACT_CMD: Custom path to tesseract executable (optional)
"""

import pytesseract
from PIL import Image
from pathlib import Path
from typing import Optional, Dict, List, Any
import logging
import platform
import os
import shutil

logger = logging.getLogger(__name__)

# Configure Teseseract executable file path (cross-os support)
def _get_tesseract_cmd() -> Optional[str]:
    """
    auto-detect Tesseract executable file path
    
    Priority:
    1. TESSERACT_CMD
    2. tesseract in system PATH
    3. Default installation location for tesseract
    """
    env_path = os.getenv('TESSERACT_CMD')
    if env_path and Path(env_path).exists():
        logger.info(f"使用环境变量指定的 Tesseract 路径: {env_path}")
        return env_path
    
    tesseract_in_path = shutil.which('tesseract')
    if tesseract_in_path:
        logger.info(f"在系统 PATH 中找到 Tesseract: {tesseract_in_path}")
        return tesseract_in_path
    
    system = platform.system()
    default_paths = []
    
    if system == "Windows":
        default_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
    elif system == "Darwin":  # macOS
        default_paths = [
            "/usr/local/bin/tesseract",
            "/opt/homebrew/bin/tesseract",  # Apple Silicon
            "/usr/bin/tesseract",
        ]
    elif system == "Linux":
        default_paths = [
            "/usr/bin/tesseract",
            "/usr/local/bin/tesseract",
        ]
    
    for path in default_paths:
        if Path(path).exists():
            logger.info(f"Found Tesseract in: {path}")
            return path
    
    logger.warning("Unable to find Tesseract executable file, please ensure Tesseract OCR installed.")
    return None


# set tesseract path
_tesseract_path = _get_tesseract_cmd()
if _tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = _tesseract_path
else:
    logger.warning(
        "Tesseract OCR not configured, please set the environment variable TESSERACT_CMD or insure tesseract is in  system PATH."
        f"Current OS: {platform.system()}\n"
    )


"""
OCR recog service class
"""
class OCRService:
    def __init__(self, lang: str = 'chi_sim+eng'):
        """
        initialize OCR service
        
        Args:
            lang: recog language, default chinese+english
        """
        self.lang = lang
        logger.info(f"OCR service initialized, language: {lang}")
    


    def extract_text_from_image(
        self, 
        image_path: str,
        config: Optional[str] = None
    ) -> str:
        """
        从图片中提取文字
        
        Args:
            image_path: 图片文件路径
            config: Tesseract 配置参数（可选）
            
        Returns:
            提取的文本内容
            
        Raises:
            FileNotFoundError: 图片文件不存在
            Exception: OCR 识别失败
        """
        try:
            if not Path(image_path).exists():
                raise FileNotFoundError(f"图片文件不存在: {image_path}")
            
            image = Image.open(image_path)
            

            text = pytesseract.image_to_string(
                image, 
                lang=self.lang,
                config=config or ''
            )
            
            logger.info(f"成功识别图片: {image_path}")
            return text.strip()
            
        except FileNotFoundError:
            raise
        except Exception as e:
            logger.error(f"OCR 识别失败: {str(e)}")
            raise Exception(f"OCR 识别失败: {str(e)}")
    
    def extract_text_from_bytes(
        self, 
        image_bytes: bytes,
        config: Optional[str] = None
    ) -> str:
        """
        从字节流中提取文字（用于处理上传的文件）
        
        Args:
            image_bytes: 图片字节流
            config: Tesseract 配置参数（可选）
            
        Returns:
            提取的文本内容
        """
        try:
            from io import BytesIO
            
            # 从字节流创建图片对象
            image = Image.open(BytesIO(image_bytes))
            
            # 执行 OCR 识别
            text = pytesseract.image_to_string(
                image,
                lang=self.lang,
                config=config or ''
            )
            
            logger.info("成功识别上传的图片")
            return text.strip()
            
        except Exception as e:
            logger.error(f"OCR 识别失败: {str(e)}")
            raise Exception(f"OCR 识别失败: {str(e)}")
    
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """
        获取图片信息和 OCR 识别数据
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            包含图片信息和识别数据的字典
        """
        try:
            if not Path(image_path).exists():
                raise FileNotFoundError(f"图片文件不存在: {image_path}")
            
            image = Image.open(image_path)
            
            # 获取详细的 OCR 数据
            data = pytesseract.image_to_data(
                image,
                lang=self.lang,
                output_type=pytesseract.Output.DICT
            )
            
            return {
                "image_size": image.size,
                "image_format": image.format,
                "image_mode": image.mode,
                "ocr_data": data
            }
            
        except Exception as e:
            logger.error(f"获取图片信息失败: {str(e)}")
            raise Exception(f"获取图片信息失败: {str(e)}")
    
    def is_tesseract_available(self) -> bool:
        """
        检查 Tesseract 是否可用
        
        Returns:
            True 如果可用，否则 False
        """
        try:
            version = pytesseract.get_tesseract_version()
            logger.info(f"Tesseract 版本: {version}")
            return True
        except Exception as e:
            logger.error(f"Tesseract 不可用: {str(e)}")
            return False
    
    def get_available_languages(self) -> List[str]:
        """
        get the language list that Tesseract supports
        """
        try:
            langs = pytesseract.get_languages()
            logger.info(f"Supported languages: {langs}")
            return langs
        except Exception as e:
            logger.error(f"Unable to obtain supported language list: {str(e)}")
            return []


# Create global OCR service instance (SIngleton Pattern)
_ocr_service: Optional[OCRService] = None


def get_ocr_service() -> OCRService:
    global _ocr_service
    if _ocr_service is None:
        _ocr_service = OCRService()
    return _ocr_service

def extract_text_from_image(image_path: str) -> str:
    service = get_ocr_service()
    return service.extract_text_from_image(image_path)


def extract_text_from_bytes(image_bytes: bytes) -> str:
    service = get_ocr_service()
    return service.extract_text_from_bytes(image_bytes)
