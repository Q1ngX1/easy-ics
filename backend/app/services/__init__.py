"""
Services module

including:
- OCRService
- get_ocr_service: get ocr service instantce
- ParserService: text parsing service
- ICSService: generate ice file
"""

from .ocr_service import OCRService, get_ocr_service
from .parser_service import ParserService
from .ics_service import ICSService

__all__ = [
    'OCRService',
    'get_ocr_service',
    #'ParserService',
    'ICSService',
]
