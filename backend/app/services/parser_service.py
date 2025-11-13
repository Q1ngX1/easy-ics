from typing import List, Optional
import logging
from datetime import datetime
from app.models.event import Event, EventPriority


logger = logging.getLogger(__name__)


class ParserService:
    def __init__(self):
        self.dateparser_service = None
    


    def parse(self, text: str, timezone: Optional[str] = None) -> List:
        """
        Parse text content and extract event information
        
        Args:
            text: Plain text content to parse
            timezone: Optional IANA timezone string (e.g., 'Asia/Shanghai')
            
        Returns:
            Event object with parsed information
            
        Raises:
            ValueError: If text is empty or cannot be parsed
        """
        if not text or text.strip() == "":
            raise ValueError("Text content cannot be empty")
        
_parser_service_instance: Optional[ParserService] = None


def get_parser_service() -> ParserService:
    global _parser_service_instance
    if _parser_service_instance is None:
        _parser_service_instance = ParserService()
    return _parser_service_instance
