# Easy ICS API 文档

## 概述

Easy ICS API 是一个 RESTful 服务，用于将图片或文本转换为 ICS 日历文件。提供 OCR 识别、文本解析和日历文件生成功能。

## 基本信息

- **基础 URL**: `http://localhost:8000`
- **API 版本**: 0.1.0
- **数据格式**: JSON
- **文档**: 
  - Swagger UI: `/docs`
  - ReDoc: `/redoc`

## API 端点概览

| 方法 | 端点 | 描述 | 状态 |
|------|------|------|------|
| POST | `/api/ocr/upload` | 上传图片进行 OCR 识别 | \u2713 已实现 |
| GET | `/api/ocr/health` | OCR 服务健康检查 | \u2713 已实现 |
| POST | `/api/text/parse` | 解析文本提取事件 | 🚧 开发中 |
| POST | `/api/ics/generate` | 生成 ICS 日历文件 | 🚧 开发中 |
| POST | `/api/process` | 完整处理流程 | 🚧 开发中 |

---

## 详细 API 文档

### 1. OCR 图片上传

#### 端点
```
POST /api/ocr/upload
```

#### 说明
上传图片文件进行 OCR 文字识别，支持多种图片格式和识别语言。

#### 请求参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| file | File | \u2713 | 上传的图片文件 (PNG, JPG, JPEG, BMP, TIFF) |
| lang | String | ✘ | OCR 识别语言，例如 `chi_sim+eng` (默认: `chi_sim+eng`) |

#### 支持的图片格式
- PNG
- JPG / JPEG
- BMP
- TIFF
- GIF (通常)

#### 支持的识别语言
| 代码 | 语言 |
|------|------|
| chi_sim | 简体中文 |
| chi_tra | 繁体中文 |
| eng | 英文 |
| jpn | 日文 |
| fra | 法文 |
| deu | 德文 |
| spa | 西班牙文 |

#### 响应示例 (成功)

```bash
curl -X POST "http://localhost:8000/api/ocr/upload" \
  -F "file=@image.png" \
  -F "lang=chi_sim+eng"
```

**状态码**: 200 OK

**响应体**:
```json
{
  "success": true,
  "text": "会议 10月28日 14:00-16:00\n地点：会议室 A\n参与者：张三、李四",
  "filename": "image.png",
  "length": 42
}
```

#### 响应示例 (文本为空)

**状态码**: 200 OK

**响应体**:
```json
{
  "success": true,
  "text": "",
  "message": "Unable to identify text from the image",
  "filename": "image.png"
}
```

#### 错误响应

**不支持的文件类型** (400)
```json
{
  "detail": "不支持的文件类型: application/pdf，请上传图片文件"
}
```

**文件为空** (400)
```json
{
  "detail": "上传的文件为空"
}
```

**OCR 服务错误** (500)
```json
{
  "detail": "OCR service fail: [错误信息]"
}
```

---

### 2. OCR 健康检查

#### 端点
```
GET /api/ocr/health
```

#### 说明
检查 OCR 服务的可用性和配置信息。

#### 请求示例

```bash
curl "http://localhost:8000/api/ocr/health"
```

#### 响应示例 (正常)

**状态码**: 200 OK

**响应体**:
```json
{
  "status": "healthy",
  "tesseract_available": true,
  "supported_languages": [
    "chi_sim",
    "eng",
    "chi_tra",
    "jpn"
  ],
  "default_language": "chi_sim+eng"
}
```

#### 响应示例 (异常)

**状态码**: 503 Service Unavailable

**响应体**:
```json
{
  "status": "unhealthy",
  "tesseract_available": false,
  "message": "Tesseract OCR 不可用，请检查安装"
}
```

#### 错误响应

**内部错误** (503)
```json
{
  "status": "error",
  "message": "[错误详情]"
}
```

---

### 3. 文本解析

#### 端点
```
POST /api/text/parse
```

#### 说明
解析文本内容，提取日历事件信息（如时间、地点、参与者等）。

#### 请求参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| text | String | \u2713 | 待解析的文本内容（可来自 OCR 或用户输入） |

#### 请求示例

```bash
curl -X POST "http://localhost:8000/api/text/parse" \
  -F "text=会议 10月28日 14:00-16:00 地点：会议室 A"
```

#### 响应示例 (待实现)

**状态码**: 501 Not Implemented

**响应体**:
```json
{
  "detail": "文本解析功能正在开发中，请等待 parser_service 实现"
}
```

#### 预期响应格式 (实现后)

```json
{
  "success": true,
  "events": [
    {
      "title": "会议",
      "start_time": "2024-10-28T14:00:00",
      "end_time": "2024-10-28T16:00:00",
      "location": "会议室 A",
      "description": ""
    }
  ]
}
```

---

### 4. ICS 文件生成

#### 端点
```
POST /api/ics/generate
```

#### 说明
根据事件数据生成标准的 ICS 日历文件，可用于导入各类日历应用。

#### 请求参数

目前无参数（待实现）

#### 请求示例

```bash
curl -X POST "http://localhost:8000/api/ics/generate"
```

#### 响应示例 (待实现)

**状态码**: 501 Not Implemented

**响应体**:
```json
{
  "detail": "ICS 生成功能正在开发中，请等待 ics_service 实现"
}
```

#### 预期响应格式 (实现后)

**状态码**: 200 OK

**响应头**:
```
Content-Type: text/calendar
Content-Disposition: attachment; filename="calendar.ics"
```

**响应体** (ICS 格式):
```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Easy ICS//Easy ICS 0.1.0//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
UID:event1@easy-ics
DTSTAMP:20241028T100000Z
DTSTART:20241028T140000
DTEND:20241028T160000
SUMMARY:会议
LOCATION:会议室 A
END:VEVENT
END:VCALENDAR
```

---

### 5. 完整处理流程

#### 端点
```
POST /api/process
```

#### 说明
一站式服务，将上传的图片通过 OCR、文本解析、ICS 生成完整处理，直接返回可下载的日历文件。

#### 请求参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| file | File | \u2713 | 上传的图片文件 |

#### 请求示例

```bash
curl -X POST "http://localhost:8000/api/process" \
  -F "file=@calendar.png"
```

#### 响应示例 (待实现)

**状态码**: 501 Not Implemented

**响应体**:
```json
{
  "detail": "完整流程功能正在开发中"
}
```

#### 预期响应格式 (实现后)

**状态码**: 200 OK

**响应头**:
```
Content-Type: text/calendar
Content-Disposition: attachment; filename="calendar.ics"
```

**响应体**: ICS 日历文件内容

---

## 错误处理

### 标准错误响应格式

所有错误响应都遵循以下格式：

```json
{
  "detail": "错误描述信息"
}
```

### 常见 HTTP 状态码

| 状态码 | 描述 | 原因 |
|--------|------|------|
| 200 | OK | 请求成功 |
| 400 | Bad Request | 请求参数错误或格式不正确 |
| 500 | Internal Server Error | 服务器内部错误 |
| 501 | Not Implemented | 功能尚未实现 |
| 503 | Service Unavailable | 服务不可用（如 Tesseract 未安装） |

---

## 使用示例

### 示例 1: 完整工作流

#### 步骤 1: 检查 OCR 服务

```bash
curl "http://localhost:8000/api/ocr/health"
```

#### 步骤 2: 上传图片进行 OCR 识别

```bash
curl -X POST "http://localhost:8000/api/ocr/upload" \
  -F "file=@calendar.png" \
  -F "lang=chi_sim+eng" \
  -o ocr_result.json

cat ocr_result.json
```

响应:
```json
{
  "success": true,
  "text": "团队会议\n2024年10月28日\n14:00-16:00\n会议室A",
  "filename": "calendar.png",
  "length": 37
}
```

#### 步骤 3: 解析文本（待实现）

```bash
curl -X POST "http://localhost:8000/api/text/parse" \
  -F "text=团队会议 2024年10月28日 14:00-16:00 会议室A"
```

#### 步骤 4: 生成 ICS 文件（待实现）

```bash
curl -X POST "http://localhost:8000/api/process" \
  -F "file=@calendar.png" \
  -o calendar.ics

# 导入到日历应用
open calendar.ics
```

### 示例 2: 多语言 OCR

#### 中文 + 英文识别

```bash
curl -X POST "http://localhost:8000/api/ocr/upload" \
  -F "file=@mixed_language.png" \
  -F "lang=chi_sim+eng"
```

#### 仅英文识别

```bash
curl -X POST "http://localhost:8000/api/ocr/upload" \
  -F "file=@english.png" \
  -F "lang=eng"
```

#### 日文识别

```bash
curl -X POST "http://localhost:8000/api/ocr/upload" \
  -F "file=@japanese.png" \
  -F "lang=jpn"
```

---

## 前端集成指南

### JavaScript/Fetch API

#### 上传图片

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('lang', 'chi_sim+eng');

fetch('http://localhost:8000/api/ocr/upload', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('识别结果:', data.text);
})
.catch(error => console.error('错误:', error));
```

#### 检查 OCR 健康状态

```javascript
fetch('http://localhost:8000/api/ocr/health')
  .then(response => response.json())
  .then(data => {
    if (data.status === 'healthy') {
      console.log('OCR 服务正常');
    } else {
      console.log('OCR 服务异常');
    }
  });
```

### React 示例

```jsx
import { useState } from 'react';

function OcrUploader() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('lang', 'chi_sim+eng');

    try {
      const response = await fetch(
        'http://localhost:8000/api/ocr/upload',
        { method: 'POST', body: formData }
      );
      const data = await response.json();
      setResult(data.text);
    } catch (error) {
      console.error('上传失败:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        accept="image/*"
      />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? '处理中...' : '上传识别'}
      </button>
      {result && <pre>{result}</pre>}
    </div>
  );
}

export default OcrUploader;
```

---

## 开发路线图

### Phase 1: 基础功能 (已完成)
- \u2713 OCR 图片上传和识别
- \u2713 OCR 服务健康检查
- \u2713 错误处理和日志记录

### Phase 2: 核心功能 (开发中)
- 🚧 文本解析和事件提取
- 🚧 ICS 文件生成
- 🚧 完整处理流程

### Phase 3: 高级功能 (计划中)
- 📅 时区支持
- 📝 文本编辑和预览
- 🔄 重复事件处理
- 👥 多人事件管理

---

## 性能指标

| 操作 | 平均时间 | 说明 |
|------|--------|------|
| OCR 识别 | 1-3秒 | 取决于图片大小和清晰度 |
| 文本解析 | <1秒 | 待实现 |
| ICS 生成 | <0.5秒 | 待实现 |
| 完整流程 | 2-4秒 | 所有步骤合计 |

---

## 常见问题

### Q1: 支持多大的图片文件？
A: 建议图片大小不超过 10MB。更大的文件可能导致处理时间增加。

### Q2: OCR 识别准确度如何？
A: 识别准确度取决于图片质量：
- 清晰、黑底白字的图片：>95%
- 普通质量的图片：80-90%
- 模糊或倾斜的图片：<80%

### Q3: 支持哪些日历格式？
A: 目前仅支持 ICS (iCalendar) 格式，可导入到：
- Google Calendar
- Outlook
- Apple Calendar
- Thunderbird
- 其他标准日历应用

### Q4: API 是否支持批量处理？
A: 目前不支持，但可以通过循环调用单个端点来实现。

### Q5: 上传的图片会被保存吗？
A: 不会。上传的图片仅用于临时处理，处理完成后立即删除。

---

## 相关资源

- [快速开始指南](../README.md)
- [时区支持文档](../app/models/TIMEZONE_GUIDE.md)
- [事件模型文档](../app/models/EVENT_GUIDE.md)
- [OCR 服务文档](../app/services/README.md)

---

## 反馈和支持

如有问题或建议，请提交 Issue 或 Pull Request。

最后更新: 2024-10-31
