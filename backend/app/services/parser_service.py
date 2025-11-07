from typing import List, Optional
import logging
from datetime import datetime
from app.models.event import Event, EventPriority
#from parser import re_parser, spaCy_parser

logger = logging.getLogger(__name__)


class ParserService:
    def __init__(self):
        pass

    def parse(self, text: str, timezone: Optional[str] = None) -> Event:
        """
        Parse text content and extract event information
        
        Args:
            text: Plain text content to parse
            timezone: Optional IANA timezone string (e.g., 'Asia/Shanghai')
            
        Returns:
            Event object with parsed information
            
        Raises:
            NotImplementedError: If parsing implementation is not ready
            ValueError: If text is empty
        """
        if not text or text.strip() == "":
            raise ValueError("Text content cannot be empty")
        
        # TODO: Implement actual parsing logic
        # Current implementation is placeholder
        # When implemented, use timezone for date/time interpretation
        raise NotImplementedError("Text parsing service is under development")
    
_parser_service_instance: Optional[ParserService] = None


def get_parser_service() -> ParserService:
    global _parser_service_instance
    if _parser_service_instance is None:
        _parser_service_instance = ParserService()
    return _parser_service_instance
