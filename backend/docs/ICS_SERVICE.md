# ICS Service 实现文档

## 📋 概述

`ICSService` 是 Easy ICS 项目的核心服务，负责处理日历事件与 ICS 文件格式的相互转换。该服务实现了 RFC 5545 标准中的核心功能。

## ✨ 主要功能

### 1. ICS 文件生成 (`generate_ics`)

将 `Event` 对象列表转换为标准 ICS 文件格式。

**特性：**
- \u2713 生成符合 RFC 5545 标准的 ICS 文件
- \u2713 支持多个事件批量生成
- \u2713 自动生成唯一事件 ID (UID)
- \u2713 完整的事件元数据支持

**使用示例：**
```python
from app.services.ics_service import ICSService
from app.models.event import Event
from datetime import datetime, timedelta

# 创建服务实例
ics_service = ICSService()

# 创建事件
event = Event(
    title="项目会议",
    start_time=datetime(2025, 10, 26, 14, 0),
    end_time=datetime(2025, 10, 26, 15, 0),
    location="会议室 A",
    description="讨论项目进度",
    reminder_minutes=15
)

# 生成 ICS 内容
ics_content = ics_service.generate_ics([event])

# 保存或返回给客户端
with open("calendar.ics", "w", encoding="utf-8") as f:
    f.write(ics_content)
```

### 2. ICS 文件解析 (`parse_ics`)

将 ICS 文件内容解析为 `Event` 对象列表。

**特性：**
- \u2713 解析标准 ICS 格式文件
- \u2713 支持多事件解析
- \u2713 容错处理（忽略解析失败的事件）
- \u2713 自动时区转换

**使用示例：**
```python
# 读取 ICS 文件
with open("calendar.ics", "r", encoding="utf-8") as f:
    ics_content = f.read()

# 解析为事件对象
events = ics_service.parse_ics(ics_content)

for event in events:
    print(f"事件: {event.title}")
    print(f"开始时间: {event.start_time}")
    print(f"结束时间: {event.end_time}")
```

## 🔧 核心方法

### `generate_ics(events: List[Event]) -> str`

**参数：**
- `events`: Event 对象列表

**返回值：**
- 字符串格式的 ICS 文件内容

**异常：**
- `ValueError`: 当事件列表为空或类型不合法时抛出

### `parse_ics(ics_content: str) -> List[Event]`

**参数：**
- `ics_content`: ICS 文件内容字符串

**返回值：**
- Event 对象列表

**异常：**
- `ValueError`: 当内容为空或不是字符串时抛出

## 📊 支持的事件属性

| 属性 | ICS 字段 | 说明 |
|------|---------|------|
| `title` | SUMMARY | 事件标题 |
| `start_time` | DTSTART | 开始时间 |
| `end_time` | DTEND | 结束时间 |
| `location` | LOCATION | 事件地点 |
| `description` | DESCRIPTION | 事件描述 |
| `priority` | PRIORITY | 优先级 (1=低, 5=中, 9=高) |
| `reminder_minutes` | VALARM | 提前多少分钟提醒 |

## 🕐 时间格式支持

服务支持多种时间格式的解析和转换：

| 格式 | 示例 | 说明 |
|------|------|------|
| UTC时间 | `20251026T140000Z` | 国际标准时间 |
| 本地时间 | `20251026T140000` | 本地时区时间 |
| 仅日期 | `20251026` | 全天事件 |

## 🔐 文本转义规则

ICS 格式要求对特殊字符进行转义：

```python
特殊字符转义规则：
- 反斜杠 (\)  → \\
- 分号 (;)    → \;
- 逗号 (,)    → \,
- 换行符      → 保留

示例：
"项目讨论; 会议室" → "项目讨论\; 会议室"
"待办项: A,B,C"   → "待办项: A\,B\,C"
```

## 🎯 优先级映射

```python
优先级转换：
- EventPriority.LOW (低)    → 1
- EventPriority.MEDIUM (中) → 5
- EventPriority.HIGH (高)   → 9
```

## 💡 使用场景

### 场景 1: 从用户输入生成 ICS 文件

```python
# API 接收请求
@router.post("/api/download_ics")
async def download_ics(request: ICSDownloadRequest):
    ics_service = ICSService()
    
    # 转换数据模型
    events = []
    for event_data in request.events:
        event = Event(
            title=event_data.title,
            start_time=datetime.fromisoformat(event_data.start_time),
            end_time=datetime.fromisoformat(event_data.end_time),
            location=event_data.location,
            description=event_data.description
        )
        events.append(event)
    
    # 生成 ICS 文件
    ics_content = ics_service.generate_ics(events)
    
    # 返回文件下载
    return StreamingResponse(
        iter([ics_content]),
        media_type="text/calendar; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=calendar.ics"}
    )
```

### 场景 2: 导入外部 ICS 文件

```python
# 读取上传的 ICS 文件
ics_content = await file.read()
ics_content_str = ics_content.decode("utf-8")

# 解析事件
ics_service = ICSService()
events = ics_service.parse_ics(ics_content_str)

# 存储或处理事件
for event in events:
    # 保存到数据库或进行其他处理
    save_to_database(event)
```

## 🧪 测试

项目包含完整的单元测试套件 (`tests/ics_service_test.py`)，覆盖以下场景：

- \u2713 基本的 ICS 生成功能
- \u2713 多事件批处理
- \u2713 特殊字符转义
- \u2713 时间格式转换
- \u2713 优先级处理
- \u2713 提醒功能
- \u2713 错误处理

**运行测试：**
```bash
cd backend
python -m pytest tests/ics_service_test.py -v
```

## 📝 ICS 文件结构示例

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Easy ICS//Easy ICS v1.0//CH
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Easy ICS Calendar
X-WR-TIMEZONE:UTC
DTSTAMP:20251026T120000Z
BEGIN:VTIMEZONE
...
END:VTIMEZONE
BEGIN:VEVENT
UID:a1b2c3d4-1762012800@easy-ics.local
DTSTAMP:20251026T120000Z
DTSTART:20251026T140000Z
DTEND:20251026T150000Z
CREATED:20251026T120000Z
LAST-MODIFIED:20251026T120000Z
SUMMARY:项目会议
LOCATION:会议室 A
DESCRIPTION:讨论项目进度
STATUS:CONFIRMED
PRIORITY:9
BEGIN:VALARM
ACTION:DISPLAY
TRIGGER:-PT15M
DESCRIPTION:Event Reminder
END:VALARM
END:VEVENT
END:VCALENDAR
```

## 🚀 高级特性

### 1. 唯一事件 ID 生成

服务自动为每个事件生成唯一的 UID：
- 格式：`{uuid}-{timestamp}@easy-ics.local`
- 确保在日历系统中的唯一性

### 2. 时区处理

- 自动转换为 UTC 格式存储
- 支持本地时间和 UTC 时间的相互转换
- 完整的 VTIMEZONE 信息

### 3. 事件提醒

支持配置提醒时间，将生成 VALARM 块：
```python
event = Event(
    title="重要会议",
    start_time=...,
    end_time=...,
    reminder_minutes=30  # 提前 30 分钟提醒
)
```

## 🐛 错误处理

服务提供完善的错误处理机制：

```python
try:
    ics_content = ics_service.generate_ics(events)
except ValueError as e:
    # 处理数据验证错误
    logger.error(f"ICS 生成失败: {str(e)}")
except Exception as e:
    # 处理未知错误
    logger.error(f"未知错误: {str(e)}")
```

## 📚 相关文件

- `app/services/ics_service.py` - ICS 服务实现
- `app/models/event.py` - 事件模型定义
- `tests/ics_service_test.py` - 单元测试
- `app/api.py` - API 端点定义

## 📖 参考资源

- RFC 5545: Internet Calendaring and Scheduling Core Object Specification
- iCalendar 标准: https://tools.ietf.org/html/rfc5545
