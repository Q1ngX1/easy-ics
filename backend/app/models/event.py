"""
事件模型定义
包含业务模型和 Pydantic 数据验证模型
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


# ===== 业务模型 =====

class EventPriority(Enum):
    """事件优先级"""
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"


class Event:
    """日程事件业务模型"""
    
    def __init__(
        self,
        title: str,
        start_time: datetime,
        end_time: datetime,
        location: Optional[str] = None,
        description: Optional[str] = None,
        priority: EventPriority = EventPriority.MEDIUM,
        reminder_minutes: Optional[int] = None
    ):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.description = description
        self.priority = priority
        self.reminder_minutes = reminder_minutes
    
    def duration_hours(self) -> float:
        """计算事件持续时间(小时)"""
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600
    
    def is_all_day(self) -> bool:
        """判断是否为全天事件"""
        return (
            self.start_time.hour == 0 and 
            self.start_time.minute == 0 and
            self.end_time.hour == 23 and 
            self.end_time.minute == 59
        )
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "title": self.title,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "location": self.location,
            "description": self.description,
            "priority": self.priority.value,
            "reminder_minutes": self.reminder_minutes,
            "duration_hours": self.duration_hours()
        }
    
    def __repr__(self) -> str:
        return f"Event(title='{self.title}', start={self.start_time})"


# ===== Pydantic 数据验证模型 (API 用) =====

class EventData(BaseModel):
    """
    事件数据 - API 请求/响应模型
    用于验证和转换 API 输入/输出
    """
    title: str = Field(..., description="事件标题", min_length=1, max_length=100)
    start_time: str = Field(..., description="开始时间 (ISO 格式: 2025-10-26T14:00:00)")
    end_time: str = Field(..., description="结束时间 (ISO 格式: 2025-10-26T16:00:00)")
    location: Optional[str] = Field(None, description="地点", max_length=200)
    description: Optional[str] = Field(None, description="描述", max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "项目讨论",
                "start_time": "2025-10-26T14:00:00",
                "end_time": "2025-10-26T16:00:00",
                "location": "会议室A",
                "description": "讨论项目进度"
            }
        }


class ICSDownloadRequest(BaseModel):
    """
    ICS 下载请求模型
    包含多个事件的列表
    """
    events: List[EventData] = Field(..., description="事件列表", min_items=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "events": [
                    {
                        "title": "项目讨论",
                        "start_time": "2025-10-26T14:00:00",
                        "end_time": "2025-10-26T16:00:00",
                        "location": "会议室A"
                    },
                    {
                        "title": "团队站会",
                        "start_time": "2025-10-27T10:00:00",
                        "end_time": "2025-10-27T10:30:00",
                        "location": "线上"
                    }
                ]
            }
        }