"""
Dependencies:
- Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
- Version: tesseract-ocr-w64-setup-5.3.4.20240503.exe
"""

import pytesseract
from PIL import Image
from pathlib import Path
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

# 配置 Tesseract 可执行文件路径
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class OCRService:
    """OCR 识别服务类"""
    
    def __init__(self, lang: str = 'chi_sim+eng'):
        """
        初始化 OCR 服务
        
        Args:
            lang: 识别语言，默认中英文
                 - 'chi_sim': 简体中文
                 - 'eng': 英文
                 - 'chi_sim+eng': 中英文混合
        """
        self.lang = lang
        logger.info(f"OCR 服务初始化完成，语言设置: {lang}")
    
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
            # 检查文件是否存在
            if not Path(image_path).exists():
                raise FileNotFoundError(f"图片文件不存在: {image_path}")
            
            # 打开图片
            image = Image.open(image_path)
            
            # 执行 OCR 识别
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
    
    def get_image_info(self, image_path: str) -> Dict[str, any]:
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
        获取 Tesseract 支持的语言列表
        
        Returns:
            支持的语言代码列表
        """
        try:
            langs = pytesseract.get_languages()
            logger.info(f"支持的语言: {langs}")
            return langs
        except Exception as e:
            logger.error(f"获取语言列表失败: {str(e)}")
            return []


# 创建全局 OCR 服务实例（单例模式）
_ocr_service: Optional[OCRService] = None


def get_ocr_service() -> OCRService:
    """
    获取 OCR 服务实例（单例模式）
    
    Returns:
        OCR 服务实例
    """
    global _ocr_service
    if _ocr_service is None:
        _ocr_service = OCRService()
    return _ocr_service


# 便捷函数
def extract_text_from_image(image_path: str) -> str:
    """
    便捷函数：从图片中提取文字
    
    Args:
        image_path: 图片文件路径
        
    Returns:
        提取的文本内容
    """
    service = get_ocr_service()
    return service.extract_text_from_image(image_path)


def extract_text_from_bytes(image_bytes: bytes) -> str:
    """
    便捷函数：从字节流中提取文字
    
    Args:
        image_bytes: 图片字节流
        
    Returns:
        提取的文本内容
    """
    service = get_ocr_service()
    return service.extract_text_from_bytes(image_bytes)
