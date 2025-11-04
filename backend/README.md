# Easy ICS Backend

图片/文字生成 ICS 日历文件的后端 API 服务

## 📋 功能特性

- ✅ OCR 图像识别（Tesseract）
- ✅ ICS 文件生成（核心功能已完成）
- ✅ ICS 文件解析（核心功能已完成）
- ✅ 跨平台支持（Windows / macOS / Linux）
- ✅ RESTful API 接口
- ⚠️ 文本解析（开发中）

## 🛠️ 技术栈

- **FastAPI**: Web 框架
- **Tesseract OCR**: 图像文字识别
- **Pydantic**: 数据验证
- **Pillow**: 图像处理

## 📦 安装依赖

### 1. 安装 Python 依赖

```bash
cd backend
pip install -e .
```

### 2. 安装 Tesseract OCR

#### Windows
下载并安装：https://github.com/UB-Mannheim/tesseract/wiki

推荐安装路径：`C:\Program Files\Tesseract-OCR\`

#### macOS
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### 3. 安装中文语言包（可选）

#### macOS
```bash
brew install tesseract-lang
```

#### Linux
```bash
sudo apt-get install tesseract-ocr-chi-sim  # 简体中文
sudo apt-get install tesseract-ocr-chi-tra  # 繁体中文
```

## 🚀 运行服务

### 方式 1: 使用 uvicorn（开发模式）

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 方式 2: 使用 fastapi CLI

```bash
cd backend
fastapi dev app/main.py
```

访问：
- API 文档：http://localhost:8000/docs
- 备用文档：http://localhost:8000/redoc
- 健康检查：http://localhost:8000/health

## 🔧 配置

### 环境变量配置

复制示例配置文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件，设置 Tesseract 路径（如果需要）：

```env
# 如果 tesseract 不在系统 PATH 中，请设置此路径
TESSERACT_CMD=/path/to/tesseract
```

### Tesseract 路径检测优先级

1. **环境变量** `TESSERACT_CMD`
2. **系统 PATH** 中的 `tesseract` 命令
3. **平台默认路径**：
   - Windows: `C:\Program Files\Tesseract-OCR\tesseract.exe`
   - macOS: `/usr/local/bin/tesseract` 或 `/opt/homebrew/bin/tesseract`
   - Linux: `/usr/bin/tesseract`

## 📡 API 接口

### 1. OCR 图像识别

**上传图片并识别**
```bash
POST /api/ocr/upload
Content-Type: multipart/form-data

# curl 示例
curl -X POST "http://localhost:8000/api/ocr/upload" \
     -F "file=@/path/to/image.png" \
     -F "lang=chi_sim+eng"
```

**响应示例**：
```json
{
  "success": true,
  "text": "识别出的文字内容",
  "filename": "image.png",
  "length": 123
}
```

### 2. OCR 健康检查

```bash
GET /api/ocr/health

# curl 示例
curl http://localhost:8000/api/ocr/health
```

**响应示例**：
```json
{
  "status": "healthy",
  "tesseract_available": true,
  "supported_languages": ["chi_sim", "chi_tra", "eng"],
  "default_language": "chi_sim+eng"
}
```

### 3. 文本解析（开发中）

```bash
POST /api/upload/text
Content-Type: application/json

# curl 示例
curl -X POST "http://localhost:8000/api/upload/text" \
     -H "Content-Type: application/json" \
     -d '{"text":"2025年10月26日下午2点开会"}'
```

### 4. 生成 ICS 文件 ✅

```bash
POST /api/download_ics
Content-Type: application/json

# curl 示例
curl -X POST "http://localhost:8000/api/download_ics" \
     -H "Content-Type: application/json" \
     -d '{
       "events": [
         {
           "title": "项目会议",
           "start_time": "2025-10-26T14:00:00",
           "end_time": "2025-10-26T15:00:00",
           "location": "会议室 A",
           "description": "讨论项目进度"
         }
       ]
     }' \
     --output calendar.ics
```

**响应**：生成的 ICS 文件（可直接导入日历应用）

## 🎯 ICS 服务文档

ICS Service 是 Easy ICS 的核心服务，负责日历事件与 ICS 文件格式的转换。

### 功能清单

- ✅ **ICS 文件生成** - 将事件对象转换为标准 ICS 格式
- ✅ **ICS 文件解析** - 将 ICS 文件解析为事件对象
- ✅ **时间格式转换** - 支持多种时间格式
- ✅ **特殊字符转义** - 自动处理特殊字符
- ✅ **优先级管理** - 支持事件优先级设置
- ✅ **提醒功能** - 支持配置事件提醒
- ✅ **完整的单元测试** - 测试覆盖率高

### 快速示例

```python
from app.services.ics_service import ICSService
from app.models.event import Event, EventPriority
from datetime import datetime, timedelta

# 创建事件
event = Event(
    title="项目会议",
    start_time=datetime(2025, 10, 26, 14, 0),
    end_time=datetime(2025, 10, 26, 15, 0),
    location="会议室 A",
    description="讨论项目进度",
    priority=EventPriority.HIGH,
    reminder_minutes=30
)

# 生成 ICS 文件
service = ICSService()
ics_content = service.generate_ics([event])

# 保存文件
with open("calendar.ics", "w", encoding="utf-8") as f:
    f.write(ics_content)

# 或者解析已有的 ICS 文件
with open("existing.ics", "r", encoding="utf-8") as f:
    events = service.parse_ics(f.read())
```

### 详细文档

- 📖 [ICS Service 完整文档](./docs/ICS_SERVICE.md) - 深入了解所有功能和高级特性
- 📚 [快速参考指南](./docs/ICS_SERVICE_QUICK_REFERENCE.md) - 常用方法速查表

## 🧪 测试

### 测试 Tesseract 安装

```bash
# 检查版本
tesseract --version

# 查看支持的语言
tesseract --list-langs
```

### 测试 OCR 服务

```python
from app.services.ocr_service import extract_text_from_image

text = extract_text_from_image("test_image.png")
print(text)
```

### 测试 API

使用 FastAPI 自动生成的文档界面：http://localhost:8000/docs

## 📁 项目结构

```
backend/
├── pyproject.toml          # 项目配置
├── .env.example            # 环境变量示例
├── README.md              # 本文档
├── docs/
│   ├── ICS_SERVICE.md                    # ICS 服务详细文档 ✅
│   └── ICS_SERVICE_QUICK_REFERENCE.md    # 快速参考 ✅
└── app/                   # 应用主目录
    ├── __init__.py
    ├── main.py           # 应用入口
    ├── api.py            # API 路由
    ├── models/           # 数据模型
    │   ├── __init__.py
    │   └── event.py      # 事件模型 ✅
    └── services/         # 业务服务
        ├── __init__.py
        ├── ocr_service.py      # OCR 识别 ✅
        ├── parser_service.py   # 文本解析 ⚠️ 开发中
        └── ics_service.py      # ICS 生成 ✅
└── tests/
    ├── __init__.py
    ├── ocr_test.py
    ├── ics_service_test.py     # ICS 服务单元测试 ✅
    └── image/
```

## 🐛 常见问题

### 问题 1: Tesseract 未找到

**错误信息**：
```
TesseractNotFoundError: tesseract is not installed
```

**解决方法**：
1. 确保已安装 Tesseract OCR
2. 将 tesseract 添加到系统 PATH
3. 或设置环境变量 `TESSERACT_CMD`

### 问题 2: 识别语言不支持

**错误信息**：
```
TesseractError: Failed to load language 'chi_sim'
```

**解决方法**：
安装对应的语言包（参考安装依赖部分）

### 问题 3: 无法识别图片中的文字

**可能原因**：
- 图片质量太低
- 文字太小或模糊
- 语言设置不正确

**建议**：
- 提高图片分辨率
- 确保文字清晰
- 使用正确的语言参数

## 📝 开发计划

- [x] OCR 图像识别服务
- [x] API 路由框架
- [x] 跨平台支持
- [x] 事件数据模型 ✅
- [x] ICS 文件生成服务 ✅
- [x] ICS 文件解析服务 ✅
- [x] ICS 服务单元测试 ✅
- [ ] 文本解析服务（开发中）
- [ ] 集成测试
- [ ] Docker 部署

## 📄 许可证

MIT
