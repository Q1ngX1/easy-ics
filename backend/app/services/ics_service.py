"""
ICS 服务模块
处理日历事件与 ICS 文件格式的转换
"""

from datetime import datetime, timezone
from typing import List, Optional
import uuid
import logging
from app.models.event import Event

logger = logging.getLogger(__name__)


class ICSService:
    """ICS 文件生成服务"""
    
    # ICS 文件格式常量
    ICS_VERSION = "2.0"
    PRODID = "-//Easy ICS//Easy ICS v1.0//CH"
    CALSCALE = "GREGORIAN"
    METHOD = "PUBLISH"
    
    def __init__(self):
        """初始化 ICS 服务"""
        self.timezone = timezone.utc
    
    def generate_ics(self, events: List[Event]) -> str:
        """
        生成 ICS 文件内容
        
        Args:
            events: Event 对象列表
            
        Returns:
            ICS 格式字符串
            
        Raises:
            ValueError: 当事件列表为空时抛出异常
        """
        if not events:
            raise ValueError("事件列表不能为空")
        
        if not isinstance(events, list):
            raise ValueError("events 必须是列表类型")
        
        # 构建 ICS 文件
        ics_lines = self._build_vcalendar_header()
        
        # 添加事件
        for event in events:
            try:
                vevent = self._build_vevent(event)
                ics_lines.extend(vevent)
            except Exception as e:
                logger.error(f"构建事件失败: {str(e)}", exc_info=True)
                raise ValueError(f"构建事件失败: {str(e)}")
        
        # 添加结尾
        ics_lines.append("END:VCALENDAR")
        
        return "\r\n".join(ics_lines)
    
    def _build_vcalendar_header(self) -> List[str]:
        """
        构建 VCALENDAR 头部
        
        Returns:
            ICS 头部行列表
        """
        now = datetime.now(self.timezone).strftime("%Y%m%dT%H%M%SZ")
        
        return [
            "BEGIN:VCALENDAR",
            f"VERSION:{self.ICS_VERSION}",
            f"PRODID:{self.PRODID}",
            f"CALSCALE:{self.CALSCALE}",
            f"METHOD:{self.METHOD}",
            f"X-WR-CALNAME:Easy ICS Calendar",
            f"X-WR-TIMEZONE:UTC",
            f"DTSTAMP:{now}",
            "BEGIN:VTIMEZONE",
            "TZID:UTC",
            "BEGIN:STANDARD",
            "DTSTART:19700101T000000",
            "TZOFFSETFROM:+0000",
            "TZOFFSETTO:+0000",
            "TZNAME:UTC",
            "END:STANDARD",
            "END:VTIMEZONE",
        ]
    
    def _build_vevent(self, event: Event) -> List[str]:
        """
        构建单个 VEVENT 块
        
        Args:
            event: Event 对象
            
        Returns:
            VEVENT 内容行列表
        """
        vevent = ["BEGIN:VEVENT"]
        
        # 生成 UID (唯一标识符)
        uid = self._generate_uid(event)
        vevent.append(f"UID:{uid}")
        
        # 时间戳
        dtstamp = datetime.now(self.timezone).strftime("%Y%m%dT%H%M%SZ")
        vevent.append(f"DTSTAMP:{dtstamp}")
        
        # 开始时间
        dtstart = self._format_datetime(event.start_time)
        vevent.append(f"DTSTART:{dtstart}")
        
        # 结束时间
        dtend = self._format_datetime(event.end_time)
        vevent.append(f"DTEND:{dtend}")
        
        # 创建时间和修改时间
        created = datetime.now(self.timezone).strftime("%Y%m%dT%H%M%SZ")
        vevent.append(f"CREATED:{created}")
        vevent.append(f"LAST-MODIFIED:{created}")
        
        # 标题 (SUMMARY)
        vevent.append(f"SUMMARY:{self._escape_text(event.title)}")
        
        # 地点 (LOCATION)
        if event.location:
            vevent.append(f"LOCATION:{self._escape_text(event.location)}")
        
        # 描述 (DESCRIPTION)
        if event.description:
            vevent.append(f"DESCRIPTION:{self._escape_text(event.description)}")
        
        # 状态 (STATUS) - 默认为 CONFIRMED
        vevent.append("STATUS:CONFIRMED")
        
        # 优先级 (PRIORITY)
        priority_value = self._get_priority_value(event)
        vevent.append(f"PRIORITY:{priority_value}")
        
        # 提醒 (VALARM - 可选)
        if event.reminder_minutes is not None and event.reminder_minutes > 0:
            alarm = self._build_valarm(event.reminder_minutes)
            vevent.extend(alarm)
        
        vevent.append("END:VEVENT")
        
        return vevent
    
    def _build_valarm(self, reminder_minutes: int) -> List[str]:
        """
        构建提醒块 (VALARM)
        
        Args:
            reminder_minutes: 提前多少分钟提醒
            
        Returns:
            VALARM 内容行列表
        """
        return [
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            f"TRIGGER:-PT{reminder_minutes}M",
            "DESCRIPTION:Event Reminder",
            "END:VALARM",
        ]
    
    def _format_datetime(self, dt: datetime) -> str:
        """
        格式化日期时间为 ICS 格式
        
        Args:
            dt: datetime 对象
            
        Returns:
            格式化后的日期时间字符串 (YYYYMMDDTHHmmssZ 格式)
        """
        if dt.tzinfo is None:
            # 如果没有时区信息，转换为 UTC
            dt = dt.replace(tzinfo=self.timezone)
        
        # 转换为 UTC
        dt_utc = dt.astimezone(self.timezone)
        
        return dt_utc.strftime("%Y%m%dT%H%M%SZ")
    
    def _generate_uid(self, event: Event) -> str:
        """
        生成事件的唯一标识符 (UID)
        
        Args:
            event: Event 对象
            
        Returns:
            唯一标识符字符串
        """
        # 使用 UUID 和事件信息生成唯一 ID
        unique_id = uuid.uuid4().hex[:8]
        timestamp = int(event.start_time.timestamp())
        domain = "easy-ics.local"
        
        return f"{unique_id}-{timestamp}@{domain}"
    
    def _escape_text(self, text: str) -> str:
        """
        转义 ICS 格式中的特殊字符
        
        Args:
            text: 待转义的文本
            
        Returns:
            转义后的文本
            
        规则:
            - 逗号 (,) -> \\,
            - 分号 (;) -> \\;
            - 反斜杠 (\\) -> \\\\
            - 换行符 (\\n) -> \\n (保留)
        """
        if not text:
            return ""
        
        # 按照 ICS 规范转义特殊字符
        text = text.replace("\\", "\\\\")  # 反斜杠必须先转义
        text = text.replace(";", "\\;")
        text = text.replace(",", "\\,")
        
        return text
    
    def _get_priority_value(self, event: Event) -> int:
        """
        获取优先级数值 (1-9)
        
        Args:
            event: Event 对象
            
        Returns:
            优先级数值 (1=低, 5=中, 9=高)
        """
        priority_map = {
            "低": 1,
            "中": 5,
            "高": 9,
        }
        
        priority_str = event.priority.value if hasattr(event.priority, 'value') else str(event.priority)
        return priority_map.get(priority_str, 5)  # 默认为中等优先级
    
    def parse_ics(self, ics_content: str) -> List[Event]:
        """
        解析 ICS 文件内容为 Event 对象列表
        
        Args:
            ics_content: ICS 文件内容字符串
            
        Returns:
            Event 对象列表
            
        Raises:
            ValueError: 当 ICS 内容格式不正确时抛出异常
        """
        if not ics_content or not isinstance(ics_content, str):
            raise ValueError("ICS 内容不能为空且必须是字符串")
        
        events = []
        lines = ics_content.strip().split("\n")
        
        in_vevent = False
        event_data = {}
        
        for line in lines:
            line = line.strip().rstrip("\r")
            
            if line == "BEGIN:VEVENT":
                in_vevent = True
                event_data = {}
            elif line == "END:VEVENT":
                if in_vevent and event_data:
                    try:
                        event = self._parse_vevent(event_data)
                        events.append(event)
                    except Exception as e:
                        logger.warning(f"解析事件失败: {str(e)}")
                in_vevent = False
            elif in_vevent and ":" in line:
                key, value = line.split(":", 1)
                # 移除参数部分 (例如 DTSTART;TZID=UTC:...)
                if ";" in key:
                    key = key.split(";")[0]
                event_data[key] = value
        
        return events
    
    def _parse_vevent(self, event_data: dict) -> Event:
        """
        从事件数据字典解析为 Event 对象
        
        Args:
            event_data: 事件数据字典
            
        Returns:
            Event 对象
        """
        from app.models.event import EventPriority
        
        title = event_data.get("SUMMARY", "未命名事件")
        location = event_data.get("LOCATION")
        description = event_data.get("DESCRIPTION")
        
        # 解析时间
        dtstart_str = event_data.get("DTSTART", "")
        dtend_str = event_data.get("DTEND", "")
        
        start_time = self._parse_datetime(dtstart_str)
        end_time = self._parse_datetime(dtend_str)
        
        # 解析优先级
        priority_value = event_data.get("PRIORITY", "5")
        priority = self._parse_priority(int(priority_value))
        
        return Event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            location=location,
            description=description,
            priority=priority
        )
    
    def _parse_datetime(self, dt_str: str) -> datetime:
        """
        解析 ICS 格式的日期时间字符串
        
        Args:
            dt_str: 日期时间字符串
            
        Returns:
            datetime 对象
        """
        # 支持的格式：
        # - 20251026T140000Z (UTC)
        # - 20251026T140000 (本地时间)
        # - 20251026 (全天)
        
        dt_str = dt_str.strip()
        
        try:
            if dt_str.endswith("Z"):
                # UTC 时间
                return datetime.strptime(dt_str, "%Y%m%dT%H%M%SZ").replace(tzinfo=self.timezone)
            elif "T" in dt_str:
                # 本地时间
                return datetime.strptime(dt_str, "%Y%m%dT%H%M%S")
            else:
                # 全天事件
                return datetime.strptime(dt_str, "%Y%m%d")
        except ValueError as e:
            logger.error(f"日期时间解析失败: {dt_str}, {str(e)}")
            # 返回当前时间作为后备
            return datetime.now()
    
    def _parse_priority(self, priority_value: int) -> any:
        """
        解析优先级数值为优先级枚举
        
        Args:
            priority_value: 优先级数值 (1-9)
            
        Returns:
            优先级枚举值
        """
        from app.models.event import EventPriority
        
        if priority_value >= 7:
            return EventPriority.HIGH
        elif priority_value >= 4:
            return EventPriority.MEDIUM
        else:
            return EventPriority.LOW
