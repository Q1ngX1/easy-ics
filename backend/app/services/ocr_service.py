"""
Dependencies:
- Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki https://digi.bib.uni-mannheim.de/tesseract/
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
        logger.info(f"Specifying the Tesseract path using environment variables: {env_path}")
        return env_path
    
    tesseract_in_path = shutil.which('tesseract')
    if tesseract_in_path:
        logger.info(f"Find Tesseract in system PATH: {tesseract_in_path}")
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
    
    def extract_text_from_bytes(
        self, 
        image_bytes: bytes,
        config: Optional[str] = None
    ) -> str:
        """
        Extract text from uploaded image
        
        Args:
            image_bytes: image bytes stream
            config: Tesseract configuration arguments (optional)
            
        Returns:
            Text Content
        """
        try:
            from io import BytesIO

            image = Image.open(BytesIO(image_bytes))
            
            text = pytesseract.image_to_string(
                image,
                lang=self.lang,
                config=config or ''
            )
            
            logger.info("Successfully identified image")
            return text.strip()
            
        except Exception as e:
            logger.error(f"OCR recognition failed: {str(e)}")
            raise Exception(f"OCR recognition failed: {str(e)}")

    def extract_text_from_image(
        self, 
        image_path: str,
        config: Optional[str] = None
    ) -> str:
        """
        Extract text from local image file

        Args:
            image_path
            config: Tesseract configuration arguments (optional)
            
        Returns:
            Text content
            
        Raises:
            FileNotFoundError
            Exception: OCR Failure
        """
        try:
            if not Path(image_path).exists():
                raise FileNotFoundError(f"image file unexist: {image_path}")
            
            image = Image.open(image_path)

            text = pytesseract.image_to_string(
                image, 
                lang=self.lang,
                config=config or ''
            )
            
            logger.info(f"Image successfully recognized: {image_path}")
            return text.strip()
            
        except FileNotFoundError:
            raise
        except Exception as e:
            logger.error(f"OCR recognition failed: {str(e)}")
            raise Exception(f"OCR recognition failed: {str(e)}")
    
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """
        Get image information and OCR recognition data
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary containing image information and recognition data
        """
        try:
            if not Path(image_path).exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            image = Image.open(image_path)
            
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
            logger.error(f"Failed to get image info: {str(e)}")
            raise Exception(f"Failed to get image info: {str(e)}")
    
    def is_tesseract_available(self) -> bool:
        """
        Check Tesseract avaliability
        """
        try:
            version = pytesseract.get_tesseract_version()
            logger.info(f"Tesseract version: {version}")
            return True
        except Exception as e:
            logger.error(f"Tesseract is unavaliable: {str(e)}")
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
