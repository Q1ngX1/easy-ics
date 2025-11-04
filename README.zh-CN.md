# Easy ICS 📅

[English](README.md) | [中文](README.zh-CN.md)

将图片、文本转换为日历文件的智能工具

## ✨ 核心功能

- 🖼️ **OCR 图像识别** - 从图片中识别日历信息
- 📝 **文本解析** - 从自然语言文本提取事件
- 📅 **ICS 生成** - 生成标准日历文件格式
- 🔄 **完整流程** - 一键从图片/文本生成日历

## 🚀 快速开始

### 后端服务启动

```bash
# 进入后端目录
cd backend

# 启动开发服务器
uvicorn app.main:app --reload

# 访问 API 文档
# 打开浏览器：http://localhost:8000/docs
```

**详细指南：** 📖 [后端启动指南](./backend/docs/BACKEND_STARTUP.md)

### 前端开发服务启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问应用
# 打开浏览器：http://localhost:5173
```

## 📁 项目结构

```
easy-ics/
├── backend/                    # Python FastAPI 后端
│   ├── app/
│   │   ├── main.py            # 应用入口
│   │   ├── api.py             # API 路由
│   │   ├── models/            # 数据模型
│   │   └── services/          # 业务逻辑
│   ├── tests/                 # 单元测试
│   ├── docs/                  # 文档
│   ├── pyproject.toml         # 项目配置
│   └── backend_startup.py     # 启动脚本
├── frontend/                   # React 前端
│   ├── src/
│   │   ├── pages/             # 页面
│   │   ├── components/        # 组件
│   │   └── App.jsx            # 主应用
│   ├── package.json
│   └── vite.config.js
└── docs/                       # 项目文档
```

## 🛠️ 技术栈

### 后端
- **FastAPI** - 现代 Web 框架
- **Pydantic** - 数据验证
- **Tesseract OCR** - 图像识别
- **Python 3.11+** - 编程语言

### 前端
- **React** - UI 框架
- **Vite** - 构建工具
- **CSS3** - 样式

## 📚 文档

| 文档 | 说明 |
|------|------|
| [后端启动指南](./backend/docs/BACKEND_STARTUP.md) | 如何启动后端服务和使用启动脚本 |
| [后端 README](./backend/README.md) | 后端项目详细说明 |
| [ICS 服务文档](./backend/docs/ICS_SERVICE.md) | ICS 文件生成和解析完整文档 |
| [ICS 快速参考](./backend/docs/ICS_SERVICE_QUICK_REFERENCE.md) | ICS 服务常用方法速查 |
| [前端 README](./frontend/README.md) | 前端项目说明 |

## 🔧 环境要求

### 后端
- Python >= 3.11
- pip 或 uv 包管理器
- Tesseract OCR（可选，用于图片识别）

### 前端
- Node.js >= 18
- npm 或 yarn

## ⚙️ 安装依赖

### 后端

```bash
cd backend

# 方式 1: 使用 pip
pip install -e .

# 方式 2: 使用 uv
uv sync
```

### 前端

```bash
cd frontend
npm install
```

## 📡 API 端点

启动后端服务后，访问 http://localhost:8000/docs 查看完整的交互式 API 文档。

**主要端点：**
- `GET /api/check_health` - 健康检查
- `POST /api/upload/img` - 上传图片进行 OCR 识别
- `POST /api/upload/text` - 解析文本提取事件
- `POST /api/download_ics` - 生成 ICS 文件

## 🧪 测试

### 后端测试

```bash
cd backend

# 运行所有测试
pytest tests/ -v

# 运行特定测试类
pytest tests/ics_service_test.py -v

# 生成覆盖率报告
pytest tests/ --cov=app --cov-report=html
```

### 前端测试

```bash
cd frontend

# 运行测试
npm run test
```

## 🐛 常见问题

**Q: 如何启动开发环境？**

A: 运行以下命令：
```bash
# 后端
cd backend && uvicorn app.main:app --reload

# 前端（新终端）
cd frontend && npm run dev
```

**Q: 如何测试 API？**

A: 启动后端后，访问 http://localhost:8000/docs 使用 Swagger UI 测试

**Q: Tesseract 如何安装？**

A: 参考 [后端 README](./backend/README.md#-安装依赖) 中的安装指南

## 📖 使用示例

### 从文本生成 ICS 文件

```python
from app.services.ics_service import ICSService
from app.models.event import Event
from datetime import datetime

# 创建事件
event = Event(
    title="项目会议",
    start_time=datetime(2025, 10, 26, 14, 0),
    end_time=datetime(2025, 10, 26, 15, 0),
    location="会议室 A"
)

# 生成 ICS
service = ICSService()
ics_content = service.generate_ics([event])

# 保存文件
with open("calendar.ics", "w") as f:
    f.write(ics_content)
```

### 使用 API 生成日历

```bash
curl -X POST "http://localhost:8000/api/download_ics" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      {
        "title": "项目会议",
        "start_time": "2025-10-26T14:00:00",
        "end_time": "2025-10-26T15:00:00"
      }
    ]
  }' \
  --output calendar.ics
```

## 🚀 部署

### Docker 部署（计划中）

```bash
docker-compose up
```

### 生产部署

后端：
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

前端：
```bash
npm run build
# 将 dist 目录部署到静态服务器
```

## 📝 开发计划

- [x] 项目结构搭建
- [x] 后端框架初始化
- [x] OCR 服务实现
- [x] ICS 生成服务
- [x] ICS 解析服务
- [x] 基础 API 路由
- [x] 前端页面优化
- [ ] 文本解析服务
- [ ] 完整的集成测试
- [ ] Docker 部署配置
- [ ] 生产环境优化

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 💬 联系方式

- GitHub Issues: [项目问题追踪](../../issues)
- 项目主页: [GitHub](https://github.com/Q1ngX1/easy-ics)

---

**Made with ❤️ by the Easy ICS Team** 