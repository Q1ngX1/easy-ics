# Easy ICS 后端启动指南

## 📋 目录

1. [快速开始](#快速开始)
2. [环境检查](#环境检查)
3. [启动服务](#启动服务)
4. [使用脚本](#使用脚本)
5. [API 接口](#api-接口)
6. [测试](#测试)
7. [故障排除](#故障排除)
8. [开发工作流](#开发工作流)

---

## 🚀 快速开始

### 最快启动方式（推荐）

```bash
# 1. 进入后端目录
cd backend

# 2. 启动开发服务器
uvicorn app.main:app --reload

# 3. 访问 API 文档
# 在浏览器中打开：http://localhost:8000/docs
```

**完成！** 🎉 您的 Easy ICS 后端服务已在运行。

---

## 🔍 环境检查

### 自动环境检查

使用启动脚本进行自动环境检查：

```bash
# 方式 1: 显示完整的启动信息和检查（推荐）
python run.py.py

# 方式 2: 仅运行环境检查
python run.py.py --check
```

**脚本会检查以下内容：**
- \u2713 Python 版本 (需要 3.11+)
- \u2713 Tesseract OCR 是否安装
- \u2713 Python 依赖是否完整
- \u2713 项目文件是否存在
- \u2713 提供详细的启动指南

### 手动检查

```bash
# 检查 Python 版本
python --version

# 检查 Tesseract
tesseract --version

# 检查 Python 包
pip list | grep -E "fastapi|pydantic|uvicorn|pytesseract"

# 验证项目结构
ls -la backend/app/
```

---

## 💻 启动服务

### 方式 1: 开发模式（推荐）

```bash
cd backend
uvicorn app.main:app --reload
```

**特点：**
- 🔄 代码修改自动重新加载
- 🐛 详细的错误信息
- 📊 完整的日志输出
- 👌 最适合本地开发

**输出示例：**
```
INFO:     Will watch for changes in these directories: ['backend']
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started server process [12345]
INFO:     Application startup complete
```

### 方式 2: 生产模式

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**特点：**
- 🚀 生产就绪
- 🔒 绑定所有网卡
- ⚡ 无文件监听开销

### 方式 3: 自定义端口

```bash
# 指定端口 8001
uvicorn app.main:app --reload --port 8001

# 指定主机和端口
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 方式 4: 使用启动脚本

```bash
# 使用脚本启动服务
python run.py.py --run
```

---

## 🛠️ 使用脚本

### run.py.py 脚本用法

这是一个强大的辅助脚本，可以自动检查环境和启动服务。

#### 基本命令

```bash
# 显示完整的启动信息和建议（默认）
python run.py.py

# 启动服务（包含环境检查）
python run.py.py --run

# 仅检查环境
python run.py.py --check

# 显示帮助信息
python run.py.py --help
```

#### 脚本功能详解

**1. 环境检查**

脚本会检查：
- Python 版本是否 >= 3.11
- Tesseract OCR 是否安装
- 所有必需的 Python 包是否安装
- 项目关键文件是否存在

**检查输出示例：**
```
\u2713 Python 3.11.14
\u2713 Tesseract OCR: tesseract 5.3.0
\u2713 FastAPI
\u2713 Pydantic
\u2713 Uvicorn
\u2713 主应用: backend/app/main.py
```

**2. 启动指南**

脚本会显示：
- 快速启动命令
- API 端点列表
- 测试方法
- 常见问题解决方案

**3. 一键启动**

使用 `--run` 参数：
```bash
python run.py.py --run
```

这会自动：
1. 检查环境
2. 如果环境正常，启动服务
3. 在 http://localhost:8000/docs 提供 API 文档

---

## 📡 API 接口

启动服务后，可以访问以下端点：

### 1. 文档和探索

| 链接 | 说明 |
|------|------|
| http://localhost:8000/docs | **Swagger UI** - 交互式 API 文档 |
| http://localhost:8000/redoc | **ReDoc** - 备用 API 文档 |
| http://localhost:8000/openapi.json | OpenAPI 规范 JSON |

### 2. 核心端点

#### 🔍 OCR 图像识别

```bash
# 健康检查
curl http://localhost:8000/api/check_health

# 上传图片进行 OCR 识别
curl -X POST "http://localhost:8000/api/upload/img" \
  -F "file=@image.png" \
  -F "lang=chi_sim+eng"

# 响应示例
{
  "success": true,
  "text": "识别出的文字",
  "filename": "image.png",
  "length": 123
}
```

#### 📝 文本解析（开发中）

```bash
curl -X POST "http://localhost:8000/api/upload/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "2025年10月26日下午2点开会"}'
```

#### 📅 ICS 文件下载

```bash
curl -X POST "http://localhost:8000/api/download_ics" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      {
        "title": "项目会议",
        "start_time": "2025-10-26T14:00:00",
        "end_time": "2025-10-26T15:00:00",
        "location": "会议室 A"
      }
    ]
  }' \
  --output calendar.ics
```

---

## 🧪 测试

### 1. 使用 Swagger UI 测试（推荐）

1. 启动服务：`uvicorn app.main:app --reload`
2. 打开：http://localhost:8000/docs
3. 选择端点，点击 "Try it out"
4. 输入参数并执行

### 2. 使用 curl 测试

```bash
# 健康检查
curl http://localhost:8000/api/check_health | jq

# 上传图片
curl -X POST "http://localhost:8000/api/upload/img" \
  -F "file=@test_image.png" | jq

# 下载 ICS 文件
curl -X POST "http://localhost:8000/api/download_ics" \
  -H "Content-Type: application/json" \
  -d '{"events": [...]}' \
  -o calendar.ics
```

### 3. 运行单元测试

```bash
# 运行所有测试
cd backend
pytest tests/ -v

# 运行 OCR 服务测试
pytest tests/ocr_test.py -v

# 运行 ICS 服务测试
pytest tests/ics_service_test.py -v

# 生成覆盖率报告
pytest tests/ --cov=app --cov-report=html
```

---

## 🐛 故障排除

### 问题 1: 端口 8000 已被占用

**错误信息：**
```
ERROR: Address already in use
```

**解决方法：**
```bash
# 方法 1: 使用其他端口
uvicorn app.main:app --reload --port 8001

# 方法 2: 查找并关闭占用端口的进程
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### 问题 2: ModuleNotFoundError

**错误信息：**
```
ModuleNotFoundError: No module named 'app'
```

**解决方法：**
```bash
# 确保在 backend 目录运行
cd backend
uvicorn app.main:app --reload

# 或者设置 PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 问题 3: Tesseract 未找到

**错误信息：**
```
TesseractNotFoundError: tesseract is not installed
```

**解决方法：**

**Windows:**
1. 从 https://github.com/UB-Mannheim/tesseract/wiki 下载安装程序
2. 推荐安装到 `C:\Program Files\Tesseract-OCR\`
3. 重启系统使 PATH 生效

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### 问题 4: Python 依赖缺失

**错误信息：**
```
ImportError: No module named 'fastapi'
```

**解决方法：**
```bash
cd backend
pip install -e .

# 或者安装完整的开发依赖
pip install -e ".[dev]"
```

### 问题 5: 连接被拒绝

**错误信息：**
```
Connection refused on localhost:8000
```

**解决方法：**
```bash
# 1. 检查服务是否运行
# 2. 验证端口是否正确
# 3. 重新启动服务
cd backend
uvicorn app.main:app --reload
```

---

## 📊 开发工作流

### 典型的开发周期

#### 1. 启动开发环境

```bash
# 打开终端
cd c:\000\Code\easy-ics\backend

# 启动开发服务器
uvicorn app.main:app --reload

# 打开另一个终端进行测试
```

#### 2. 开发和测试

```bash
# 编辑源代码
# 代码会自动重新加载

# 在浏览器中测试
# http://localhost:8000/docs

# 或使用 curl 测试
curl http://localhost:8000/api/check_health
```

#### 3. 运行单元测试

```bash
# 在新的终端中
cd backend

# 运行特定的测试
pytest tests/ics_service_test.py -v

# 运行所有测试
pytest tests/ -v
```

#### 4. 查看日志

开发服务器输出会显示：
- 请求日志
- 错误信息
- 性能警告
- 重新加载通知

### 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # 应用入口
│   ├── api.py                  # API 路由
│   ├── models/
│   │   ├── __init__.py
│   │   └── event.py            # 事件模型
│   └── services/
│       ├── __init__.py
│       ├── ocr_service.py      # OCR 服务
│       ├── parser_service.py   # 文本解析服务
│       └── ics_service.py      # ICS 生成服务
├── tests/
│   ├── __init__.py
│   ├── ocr_test.py             # OCR 测试
│   ├── ics_service_test.py     # ICS 测试
│   └── image/                  # 测试图片目录
├── docs/
│   ├── API.md                  # API 文档
│   ├── ICS_SERVICE.md          # ICS 服务文档
│   ├── ICS_SERVICE_QUICK_REFERENCE.md  # 快速参考
│   └── run.py.md      # 本文档
├── pyproject.toml              # 项目配置
├── run.py.py          # 启动脚本
└── README.md                   # 项目说明
```

### 常用命令速记

```bash
# 启动开发服务
cd backend && uvicorn app.main:app --reload

# 运行所有测试
pytest tests/ -v

# 运行特定测试类
pytest tests/ics_service_test.py::TestICSService -v

# 生成覆盖率报告
pytest tests/ --cov=app --cov-report=html

# 检查代码格式
black app/

# 检查类型提示
mypy app/

# 列出依赖
pip freeze
```

---

## 📚 相关文档

- 📖 [README.md](../README.md) - 项目总体说明
- 📡 [API.md](api.md) - API 接口文档
- 📅 [ICS_SERVICE.md](ICS_SERVICE.md) - ICS 服务详细文档
- ⚡ [ICS_SERVICE_QUICK_REFERENCE.md](ICS_SERVICE_QUICK_REFERENCE.md) - ICS 服务快速参考

---

## 💡 提示

**开发效率建议：**

1. 使用 VS Code 的 Python 扩展和 FastAPI 扩展
2. 启用 Swagger UI 进行 API 调试
3. 使用单元测试确保代码质量
4. 定期查看服务器日志了解发生的情况
5. 使用 `--reload` 标志进行快速迭代开发

**生产部署准备：**

1. 移除 `--reload` 标志
2. 使用生产级 ASGI 服务器（如 Gunicorn）
3. 配置 HTTPS/SSL
4. 设置环境变量
5. 使用容器化部署（Docker）

---

**祝您开发愉快！🎉**
