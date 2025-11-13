"""
Date/Time Parser using dateparser library

Supports:
- Relative dates: "明天", "下周一", "后天"
- Time expressions: "下午2点", "14:00", "2点半"
- Combined: "明天下午2点", "下周一上午10点"
- Multiple languages: Chinese, English, etc.
"""

import re
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import dateparser

logger = logging.getLogger(__name__)


class DateParserService:
    """
    使用 dateparser 库解析日期时间的服务
    """
    
    def __init__(self, timezone: Optional[str] = None):
        """
        初始化日期解析服务
        
        Args:
            timezone: IANA 时区字符串，例如 'Asia/Shanghai'
        """
        self.timezone = timezone or 'UTC'
        self.default_hour = 9  # 默认小时
        self.default_minute = 0  # 默认分钟
    
    def parse_datetime(self, text: str) -> Optional[datetime]:
        """
        解析文本中的日期时间
        
        Args:
            text: 包含日期时间的文本
            
        Returns:
            解析出的 datetime 对象，失败返回 None
            
        Examples:
            >>> service = DateParserService()
            >>> service.parse_datetime("明天下午2点")
            datetime(2025, 11, 14, 14, 0, 0)
            
            >>> service.parse_datetime("下周一上午10点")
            datetime(2025, 11, 17, 10, 0, 0)
        """
        try:
            # 使用 dateparser 解析
            parsed = dateparser.parse(
                text,
                settings={
                    'TIMEZONE': self.timezone,
                    'PREFER_DATES_FROM': 'current_period',
                    'LANGUAGES': ['zh', 'en'],
                    'RETURN_AS_TIMEZONE_AWARE': True,
                }
            )
            
            if parsed:
                logger.debug(f"Parsed '{text}' -> {parsed}")
                return parsed
            
            logger.warning(f"Failed to parse: {text}")
            return None
            
        except Exception as e:
            logger.error(f"Error parsing '{text}': {str(e)}")
            return None
    
    def extract_duration(self, text: str) -> int:
        """
        从文本中提取持续时间（分钟）
        
        Examples:
            >>> service.extract_duration("开会1小时")
            60
            
            >>> service.extract_duration("会议30分钟")
            30
        """
        # 匹配 "X小时" 或 "X个小时"
        hours_match = re.search(r'(\d+)\s*个?小时', text)
        if hours_match:
            return int(hours_match.group(1)) * 60
        
        # 匹配 "X分钟"
        minutes_match = re.search(r'(\d+)\s*分钟', text)
        if minutes_match:
            return int(minutes_match.group(1))
        
        # 默认 1 小时
        return 60
    
    def extract_location(self, text: str) -> Optional[str]:
        """
        从文本中提取地点信息
        
        支持模式：
        - "在XX"
        - "位于XX"
        - "地点：XX"
        - "会议室XX"
        
        Examples:
            >>> service.extract_location("在楼下咖啡厅开会")
            "楼下咖啡厅"
            
            >>> service.extract_location("会议室A讨论")
            "会议室A"
        """
        # 常见地点前缀词
        location_patterns = [
            r'在\s*([^，。！？、]+)',  # "在X"
            r'位于\s*([^，。！？、]+)',  # "位于X"
            r'地点[：:]\s*([^，。！？、]+)',  # "地点:X"
            r'(会议室[A-Z0-9]+)',  # "会议室A"
            r'(楼下[^，。！？、]+)',  # "楼下X"
            r'(线上|远程|电话|视频)',  # 特殊地点
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text)
            if match:
                location = match.group(1).strip()
                logger.debug(f"Extracted location: {location}")
                return location
        
        return None
    
    def extract_title(self, text: str, preserve_datetime: bool = False) -> str:
        """
        从文本中提取事件标题（去除日期、时间、地点等信息）
        
        Args:
            text: 原始文本
            preserve_datetime: 是否保留日期时间信息在标题中
            
        Returns:
            清理后的事件标题
            
        Examples:
            >>> service.extract_title("明天下午2点在会议室A开会讨论项目")
            "讨论项目" 或 "开会讨论项目"
        """
        title = text
        
        # 移除日期时间表达式
        datetime_patterns = [
            r'(明天|今天|昨天|后天)',
            r'(下周|上周|这周|下个月|上个月)',
            r'(周[一二三四五六日]|星期[一二三四五六日])',
            r'(\d{1,4}[-/]\d{1,2}[-/]\d{1,2})',  # YYYY-MM-DD
            r'(上午|下午|中午|晚上)',
            r'(\d{1,2}[:点：]\d{1,2}(?:[:点：]\d{1,2})?)',  # HH:MM(:SS)
            r'(\d+小时|\d+分钟)',
        ]
        
        for pattern in datetime_patterns:
            title = re.sub(pattern, '', title)
        
        # 移除地点信息
        location_patterns = [
            r'在\s*[^，。！？、]+',
            r'位于\s*[^，。！？、]+',
            r'地点[：:][^，。！？、]+',
            r'会议室[A-Z0-9]+',
        ]
        
        for pattern in location_patterns:
            title = re.sub(pattern, '', title)
        
        # 清理多余空格和标点
        title = re.sub(r'\s+', ' ', title).strip()
        title = re.sub(r'^[，。！？、\s]+|[，。！？、\s]+$', '', title)
        
        # 如果标题为空，使用通用标题
        if not title:
            title = "日程"
        
        logger.debug(f"Extracted title: {title}")
        return title
    
    def parse_event(
        self, 
        text: str
    ) -> Dict[str, any]:
        """
        从文本中解析事件信息
        
        Returns:
            包含以下字段的字典：
            {
                "title": str,
                "start_time": datetime,
                "end_time": datetime,
                "location": Optional[str],
                "duration_minutes": int,
                "confidence": float  # 0-1, 置信度
            }
        """
        if not text or text.strip() == "":
            raise ValueError("Text cannot be empty")
        
        result = {
            "title": None,
            "start_time": None,
            "end_time": None,
            "location": None,
            "duration_minutes": 60,
            "confidence": 0.0,
            "raw_text": text
        }
        
        try:
            # 1. 解析开始时间
            start_time = self.parse_datetime(text)
            if not start_time:
                logger.warning(f"Cannot parse datetime from: {text}")
                return result
            
            result["start_time"] = start_time
            result["confidence"] += 0.3
            
            # 2. 提取持续时间
            duration_minutes = self.extract_duration(text)
            result["duration_minutes"] = duration_minutes
            result["confidence"] += 0.2
            
            # 3. 计算结束时间
            end_time = start_time + timedelta(minutes=duration_minutes)
            result["end_time"] = end_time
            result["confidence"] += 0.2
            
            # 4. 提取地点
            location = self.extract_location(text)
            if location:
                result["location"] = location
                result["confidence"] += 0.15
            
            # 5. 提取标题
            title = self.extract_title(text)
            result["title"] = title
            result["confidence"] += 0.15
            
            # 确保置信度 <= 1.0
            result["confidence"] = min(result["confidence"], 1.0)
            
            logger.info(f"Parsed event: {result['title']} @ {result['start_time']}")
            return result
            
        except Exception as e:
            logger.error(f"Error parsing event: {str(e)}", exc_info=True)
            return result
    
    def parse_multiple_events(
        self,
        text: str,
        split_pattern: Optional[str] = None
    ) -> List[Dict[str, any]]:
        """
        从文本中解析多个事件
        
        支持按行、按句号、按分号分割事件
        
        Args:
            text: 包含多个事件的文本
            split_pattern: 自定义分割模式（正则表达式）
            
        Returns:
            事件列表
            
        Examples:
            >>> text = "明天2点开会。后天下午3点讨论方案。"
            >>> service.parse_multiple_events(text)
            [
                {...},  # 明天2点开会
                {...}   # 后天下午3点讨论方案
            ]
        """
        # 默认分割模式：句号、感叹号、问号
        if split_pattern is None:
            split_pattern = r'[。！？\n]'
        
        # 分割文本
        sentences = re.split(split_pattern, text)
        
        events = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:  # 跳过空行
                try:
                    event = self.parse_event(sentence)
                    if event.get("start_time"):
                        events.append(event)
                except Exception as e:
                    logger.warning(f"Failed to parse event from '{sentence}': {str(e)}")
        
        logger.info(f"Parsed {len(events)} events from text")
        return events


# 全局单例
_dateparser_service: Optional[DateParserService] = None


def get_dateparser_service(timezone: Optional[str] = None) -> DateParserService:
    """
    获取 DateParserService 单例
    
    Args:
        timezone: 可选的时区，覆盖全局设置
        
    Returns:
        DateParserService 实例
    """
    global _dateparser_service
    if _dateparser_service is None:
        _dateparser_service = DateParserService(timezone=timezone)
    elif timezone and timezone != _dateparser_service.timezone:
        # 如果指定了不同的时区，创建新实例
        return DateParserService(timezone=timezone)
    return _dateparser_service
