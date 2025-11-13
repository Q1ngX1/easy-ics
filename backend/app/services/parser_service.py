from typing import List, Optional
import logging
from datetime import datetime
from app.models.event import Event, EventPriority
from app.services.parser.dateparser_parser import get_dateparser_service

logger = logging.getLogger(__name__)


class ParserService:
    def __init__(self):
        self.dateparser_service = None
    
    def _get_dateparser_service(self, timezone: Optional[str] = None):
        """获取 dateparser 服务实例"""
        if timezone:
            return get_dateparser_service(timezone=timezone)
        if self.dateparser_service is None:
            self.dateparser_service = get_dateparser_service()
        return self.dateparser_service

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
        
        try:
            # 使用 dateparser 服务解析事件
            dateparser_svc = self._get_dateparser_service(timezone)
            event_dict = dateparser_svc.parse_event(text)
            
            # 验证必要字段
            if not event_dict.get("start_time"):
                raise ValueError(f"Cannot parse event from text: {text}")
            
            # 构建 Event 对象
            event = Event(
                title=event_dict.get("title", "日程"),
                start_time=event_dict["start_time"],
                end_time=event_dict["end_time"],
                location=event_dict.get("location"),
                description=f"原始文本: {text}",
                priority=EventPriority.MEDIUM
            )
            
            logger.info(f"Successfully parsed event: {event.title}")
            return event
            
        except Exception as e:
            logger.error(f"Error parsing event: {str(e)}", exc_info=True)
            raise ValueError(f"Failed to parse event: {str(e)}")
    
_parser_service_instance: Optional[ParserService] = None


def get_parser_service() -> ParserService:
    global _parser_service_instance
    if _parser_service_instance is None:
        _parser_service_instance = ParserService()
    return _parser_service_instance
