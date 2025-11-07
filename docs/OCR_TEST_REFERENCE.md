# 运行所有测试
## 基础运行
pytest tests/ocr_test.py -v

## 显示详细信息和打印输出
pytest tests/ocr_test.py -v -s

## 显示测试覆盖率
pytest tests/ocr_test.py --cov=app.services.ocr_service --cov-report=html

# 运行特定的测试类
## 只运行初始化测试
pytest tests/ocr_test.py::TestOCRServiceInitialization -v

## 只运行 Tesseract 可用性测试
pytest tests/ocr_test.py::TestTesseractAvailability -v

## 只运行语言支持测试
pytest tests/ocr_test.py::TestLanguageSupport -v

## 只运行错误处理测试
pytest tests/ocr_test.py::TestErrorHandling -v

# 运行特定的测试函数
## 运行单个测试
pytest tests/ocr_test.py::TestOCRServiceInitialization::test_ocr_service_init_default_language -v

## 运行多个特定测试
pytest tests/ocr_test.py::TestExtractTextFromImage::test_extract_text_from_image_success -v

# 运行真实照片识别测试
## 首先将测试图片放在 tests/image 目录下
## 然后运行真实图片测试（需要 Tesseract 安装）
pytest tests/ocr_test.py::TestRealImageRecognition -v -s

## 只运行真实图片文件识别测试
pytest tests/ocr_test.py::TestRealImageRecognition::test_recognize_real_image_from_file -v -s

## 只运行字节流识别测试
pytest tests/ocr_test.py::TestRealImageRecognition::test_recognize_real_image_from_bytes -v -s

## 只运行图片信息获取测试
pytest tests/ocr_test.py::TestRealImageRecognition::test_recognize_real_image_get_info -v -s

# 高级运行选项
## 并行运行测试（需要 pytest-xdist）
pip install pytest-xdist
pytest tests/ocr_test.py -n auto -v

## 显示最慢的 10 个测试
pytest tests/ocr_test.py --durations=10 -v

## 只运行失败的测试
pytest tests/ocr_test.py --lf -v

## 失败时立即停止
pytest tests/ocr_test.py -x -v

## 显示本地变量信息
pytest tests/ocr_test.py -v --tb=long

## 生成 HTML 报告
pytest tests/ocr_test.py --html=report.html --self-contained-html


# 完整的测试流程
## 1. 进入项目目录
cd c:\000\Code\easy-ics

## 2. 创建测试图片目录
mkdir backend\tests\image

## 3. 将测试图片放入 backend\tests\image 目录

## 4. 运行所有测试（包括模拟测试和真实图片测试）
pytest tests/ocr_test.py -v -s --cov=app.services.ocr_service

## 5. 查看 HTML 覆盖率报告
## 报告会生成在 htmlcov/index.html
start htmlcov\index.html