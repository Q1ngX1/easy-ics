# ICS Service 快速参考

## 🚀 快速开始

### 导入服务
```python
from app.services.ics_service import ICSService
from app.models.event import Event, EventPriority
from datetime import datetime, timedelta
```

### 创建事件
```python
# 简单事件
event = Event(
    title="会议",
    start_time=datetime(2025, 10, 26, 14, 0),
    end_time=datetime(2025, 10, 26, 15, 0)
)

# 完整事件
event = Event(
    title="项目评审",
    start_time=datetime(2025, 10, 26, 14, 0),
    end_time=datetime(2025, 10, 26, 15, 30),
    location="会议室 B",
    description="第四季度项目评审会议",
    priority=EventPriority.HIGH,
    reminder_minutes=30
)
```

### 生成 ICS 文件
```python
# 创建服务实例
service = ICSService()

# 生成 ICS 内容
events = [event1, event2, event3]
ics_content = service.generate_ics(events)

# 保存到文件
with open("calendar.ics", "w", encoding="utf-8") as f:
    f.write(ics_content)

# 或者返回给客户端
return StreamingResponse(
    iter([ics_content]),
    media_type="text/calendar; charset=utf-8",
    headers={"Content-Disposition": "attachment; filename=calendar.ics"}
)
```

### 解析 ICS 文件
```python
# 读取 ICS 文件
with open("calendar.ics", "r", encoding="utf-8") as f:
    ics_content = f.read()

# 解析事件
service = ICSService()
events = service.parse_ics(ics_content)

# 处理事件
for event in events:
    print(f"标题: {event.title}")
    print(f"时间: {event.start_time} - {event.end_time}")
    print(f"地点: {event.location}")
    print(f"描述: {event.description}")
```

## 🔧 常用方法

| 方法 | 功能 | 返回值 |
|------|------|--------|
| `generate_ics(events)` | 生成 ICS 文件 | `str` |
| `parse_ics(content)` | 解析 ICS 文件 | `List[Event]` |
| `_format_datetime(dt)` | 格式化日期时间 | `str` |
| `_escape_text(text)` | 转义特殊字符 | `str` |
| `_get_priority_value(event)` | 获取优先级数值 | `int` |

## 📝 常见使用场景

### 场景 1: 创建多个事件
```python
events = [
    Event(title="站会", start_time=..., end_time=...),
    Event(title="代码评审", start_time=..., end_time=...),
    Event(title="计划会", start_time=..., end_time=...),
]
ics_content = service.generate_ics(events)
```

### 场景 2: 带有提醒的事件
```python
event = Event(
    title="重要会议",
    start_time=datetime(2025, 10, 26, 9, 0),
    end_time=datetime(2025, 10, 26, 10, 0),
    reminder_minutes=60  # 提前 1 小时提醒
)
```

### 场景 3: 全天事件
```python
event = Event(
    title="公司休息日",
    start_time=datetime(2025, 10, 26, 0, 0),
    end_time=datetime(2025, 10, 26, 23, 59)
)
```

### 场景 4: 导入外部日历
```python
# 从 Google Calendar, Outlook 等导入
ics_content = read_external_ics_file()
events = service.parse_ics(ics_content)
```

## ⚙️ 优先级设置

```python
# 低优先级
Event(..., priority=EventPriority.LOW)      # 数值: 1

# 中优先级 (默认)
Event(..., priority=EventPriority.MEDIUM)   # 数值: 5

# 高优先级
Event(..., priority=EventPriority.HIGH)     # 数值: 9
```

## 🕐 时间格式

```python
# 推荐：ISO 格式
start_time=datetime(2025, 10, 26, 14, 0)    # 2025-10-26 14:00:00

# 自 ISO 字符串解析
datetime.fromisoformat("2025-10-26T14:00:00")

# 相对时间
from datetime import timedelta
now = datetime.now()
event_time = now + timedelta(hours=2)
```

## ⚠️ 常见错误

### 错误 1: 事件列表为空
```python
# ❌ 错误
service.generate_ics([])

# ✅ 正确
service.generate_ics([event1, event2])
```

### 错误 2: 时间格式不正确
```python
# ❌ 错误
Event(..., start_time="2025-10-26 14:00:00")

# ✅ 正确
Event(..., start_time=datetime(2025, 10, 26, 14, 0))
```

### 错误 3: 结束时间早于开始时间
```python
# ❌ 错误
start_time=datetime(2025, 10, 26, 15, 0)
end_time=datetime(2025, 10, 26, 14, 0)

# ✅ 正确
start_time=datetime(2025, 10, 26, 14, 0)
end_time=datetime(2025, 10, 26, 15, 0)
```

## 📊 特殊字符处理

自动转义：
```python
# 输入包含特殊字符
event = Event(
    title="项目讨论; 会议室 A,B",
    description="待办: 1,2,3\n讨论"
)

# 自动转义为
"项目讨论\; 会议室 A\,B"
```

## 🧪 测试

```bash
# 运行所有 ICS 服务测试
python -m pytest tests/ics_service_test.py -v

# 运行特定测试
python -m pytest tests/ics_service_test.py::TestICSService::test_generate_ics_success -v

# 查看覆盖率
python -m pytest tests/ics_service_test.py --cov=app.services.ics_service
```

## 📚 相关资源

- **RFC 5545**: https://tools.ietf.org/html/rfc5545
- **iCalendar 规范**: https://en.wikipedia.org/wiki/ICalendar
- **Event 模型**: `app/models/event.py`
- **API 文档**: `docs/api.md`

## 💬 常见问题

**Q: 如何添加提醒？**
A: 使用 `reminder_minutes` 参数：
```python
Event(..., reminder_minutes=15)  # 提前 15 分钟
```

**Q: 如何处理多个时区？**
A: 服务自动转换为 UTC，建议输入时使用 UTC 或带时区的 datetime

**Q: 是否支持循环事件？**
A: 当前版本不支持，可在后续版本中添加 RRULE 支持

**Q: 生成的 ICS 文件可以在哪些应用中打开？**
A: 所有主流日历应用，如：
- Google Calendar
- Microsoft Outlook
- Apple Calendar
- Mozilla Thunderbird
- 等等
