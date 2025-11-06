from typing import List, Optional
import logging
from datetime import datetime
from app.models.event import Event, EventPriority

logger = logging.getLogger(__name__)


class ParserService:
    def __init__(self):
        pass

    def parse(self) -> Event:
        pass
    
_parser_service_instance: Optional[ParserService] = None


def get_parser_service() -> ParserService:
    global _parser_service_instance
    if _parser_service_instance is None:
        _parser_service_instance = ParserService()
    return _parser_service_instance
