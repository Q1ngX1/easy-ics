"""
ICS Servuce unit test
"""

import pytest
from datetime import datetime, timedelta
from app.models.event import Event, EventPriority
from app.services.ics_service import ICSService


class TestICSService:
    """ICS 服务测试"""
    
    @pytest.fixture
    def ics_service(self):
        """创建 ICS 服务实例"""
        return ICSService()
    
    @pytest.fixture
    def sample_events(self):
        """创建示例事件"""
        now = datetime.now()
        return [
            Event(
                title="团队会议",
                start_time=now,
                end_time=now + timedelta(hours=1),
                location="会议室 A",
                description="讨论项目进度",
                priority=EventPriority.HIGH
            ),
            Event(
                title="午餐时间",
                start_time=now + timedelta(hours=2),
                end_time=now + timedelta(hours=3),
                location="食堂",
                description="团队午餐",
                priority=EventPriority.LOW,
                reminder_minutes=15
            )
        ]
    
    def test_generate_ics_success(self, ics_service, sample_events):
        """测试成功生成 ICS 文件"""
        ics_content = ics_service.generate_ics(sample_events)
        
        assert ics_content is not None
        assert "BEGIN:VCALENDAR" in ics_content
        assert "END:VCALENDAR" in ics_content
        assert "BEGIN:VEVENT" in ics_content
        assert "END:VEVENT" in ics_content
        assert "团队会议" in ics_content
        assert "午餐时间" in ics_content
    
    def test_generate_ics_empty_list(self, ics_service):
        """测试空事件列表"""
        with pytest.raises(ValueError, match="事件列表不能为空"):
            ics_service.generate_ics([])
    
    def test_generate_ics_invalid_type(self, ics_service):
        """测试无效的事件类型"""
        with pytest.raises(ValueError, match="events 必须是列表类型"):
            ics_service.generate_ics("invalid")
    
    def test_format_datetime(self, ics_service):
        """测试日期时间格式化"""
        dt = datetime(2025, 10, 26, 14, 30, 0)
        formatted = ics_service._format_datetime(dt)
        
        assert formatted is not None
        assert "202510261430" in formatted
        assert formatted.endswith("Z")
    
    def test_escape_text(self, ics_service):
        """测试文本转义"""
        test_cases = [
            ("简单文本", "简单文本"),
            ("带;分号的文本", "带\\;分号的文本"),
            ("带,逗号的文本", "带\\,逗号的文本"),
            ("带\\反斜杠的文本", "带\\\\反斜杠的文本"),
        ]
        
        for input_text, expected in test_cases:
            assert ics_service._escape_text(input_text) == expected
    
    def test_escape_text_empty(self, ics_service):
        """测试空文本转义"""
        assert ics_service._escape_text("") == ""
        assert ics_service._escape_text(None) == ""
    
    def test_get_priority_value(self, ics_service):
        """测试优先级转换"""
        low_event = Event(
            title="低优先级",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            priority=EventPriority.LOW
        )
        
        medium_event = Event(
            title="中优先级",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            priority=EventPriority.MEDIUM
        )
        
        high_event = Event(
            title="高优先级",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            priority=EventPriority.HIGH
        )
        
        assert ics_service._get_priority_value(low_event) == 1
        assert ics_service._get_priority_value(medium_event) == 5
        assert ics_service._get_priority_value(high_event) == 9
    
    def test_generate_uid(self, ics_service):
        """测试 UID 生成"""
        event = Event(
            title="测试事件",
            start_time=datetime(2025, 10, 26, 14, 0, 0),
            end_time=datetime(2025, 10, 26, 15, 0, 0)
        )
        
        uid1 = ics_service._generate_uid(event)
        uid2 = ics_service._generate_uid(event)
        
        assert uid1 is not None
        assert uid2 is not None
        # UID 应该包含域名
        assert "@easy-ics.local" in uid1
        assert "@easy-ics.local" in uid2
    
    def test_parse_ics(self, ics_service, sample_events):
        """测试 ICS 文件解析"""
        # 先生成 ICS 文件
        ics_content = ics_service.generate_ics(sample_events)
        
        # 再解析 ICS 文件
        parsed_events = ics_service.parse_ics(ics_content)
        
        assert len(parsed_events) > 0
        assert any("团队会议" in event.title for event in parsed_events)
        assert any("午餐时间" in event.title for event in parsed_events)
    
    def test_parse_ics_empty(self, ics_service):
        """测试空 ICS 内容"""
        with pytest.raises(ValueError, match="ICS 内容不能为空"):
            ics_service.parse_ics("")
    
    def test_parse_datetime_utc(self, ics_service):
        """测试 UTC 格式日期时间解析"""
        dt = ics_service._parse_datetime("20251026T140000Z")
        
        assert dt is not None
        assert dt.year == 2025
        assert dt.month == 10
        assert dt.day == 26
    
    def test_parse_datetime_local(self, ics_service):
        """测试本地格式日期时间解析"""
        dt = ics_service._parse_datetime("20251026T140000")
        
        assert dt is not None
        assert dt.year == 2025
        assert dt.month == 10
        assert dt.day == 26
    
    def test_parse_datetime_date_only(self, ics_service):
        """测试仅日期解析"""
        dt = ics_service._parse_datetime("20251026")
        
        assert dt is not None
        assert dt.year == 2025
        assert dt.month == 10
        assert dt.day == 26
    
    def test_parse_priority(self, ics_service):
        """测试优先级解析"""
        assert ics_service._parse_priority(1) == EventPriority.LOW
        assert ics_service._parse_priority(5) == EventPriority.MEDIUM
        assert ics_service._parse_priority(9) == EventPriority.HIGH
    
    def test_ics_with_reminder(self, ics_service):
        """测试包含提醒的事件"""
        event = Event(
            title="重要会议",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            reminder_minutes=30
        )
        
        ics_content = ics_service.generate_ics([event])
        
        assert "BEGIN:VALARM" in ics_content
        assert "PT30M" in ics_content
        assert "END:VALARM" in ics_content
    
    def test_ics_without_location_description(self, ics_service):
        """测试没有地点和描述的事件"""
        event = Event(
            title="简单事件",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1)
        )
        
        ics_content = ics_service.generate_ics([event])
        
        assert "BEGIN:VCALENDAR" in ics_content
        assert "END:VCALENDAR" in ics_content
        assert "简单事件" in ics_content
