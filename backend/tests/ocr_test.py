"""
OCR Service Unit Tests

测试 OCRService 的核心功能，包括：
- Tesseract 可用性检查
- 语言支持检查
- 图片文件验证
- 字节流处理
"""

import pytest
import logging
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO
from PIL import Image

from app.services.ocr_service import (
    OCRService,
    get_ocr_service,
    extract_text_from_image,
    extract_text_from_bytes,
)

logger = logging.getLogger(__name__)


class TestOCRServiceInitialization:
    """OCR 服务初始化测试"""

    def test_ocr_service_init_default_language(self):
        """测试 OCRService 初始化时的默认语言"""
        service = OCRService()
        assert service.lang == 'chi_sim+eng'

    def test_ocr_service_init_custom_language(self):
        """测试 OCRService 初始化时的自定义语言"""
        service = OCRService(lang='eng')
        assert service.lang == 'eng'

    def test_get_ocr_service_singleton(self):
        """测试 OCRService 单例模式"""
        service1 = get_ocr_service()
        service2 = get_ocr_service()
        assert service1 is service2


class TestTesseractAvailability:
    """Tesseract 可用性测试"""

    @patch('pytesseract.get_tesseract_version')
    def test_is_tesseract_available_true(self, mock_version):
        """测试 Tesseract 可用的情况"""
        mock_version.return_value = 'tesseract 5.3.4'
        
        service = OCRService()
        result = service.is_tesseract_available()
        
        assert result is True
        mock_version.assert_called_once()

    @patch('pytesseract.get_tesseract_version')
    def test_is_tesseract_available_false(self, mock_version):
        """测试 Tesseract 不可用的情况"""
        mock_version.side_effect = Exception('Tesseract not found')
        
        service = OCRService()
        result = service.is_tesseract_available()
        
        assert result is False


class TestLanguageSupport:
    """语言支持测试"""

    @patch('pytesseract.get_languages')
    def test_get_available_languages_success(self, mock_langs):
        """测试获取支持的语言列表"""
        mock_langs.return_value = ['chi_sim', 'chi_tra', 'eng', 'jpn']
        
        service = OCRService()
        languages = service.get_available_languages()
        
        assert isinstance(languages, list)
        assert 'chi_sim' in languages
        assert 'eng' in languages

    @patch('pytesseract.get_languages')
    def test_get_available_languages_error(self, mock_langs):
        """测试获取语言列表失败时返回空列表"""
        mock_langs.side_effect = Exception('Error getting languages')
        
        service = OCRService()
        languages = service.get_available_languages()
        
        assert languages == []


class TestExtractTextFromImage:
    """从图片文件提取文本测试"""

    @patch('pytesseract.image_to_string')
    @patch('app.services.ocr_service.Image.open')
    def test_extract_text_from_image_success(self, mock_image_open, mock_ocr):
        """测试成功从图片提取文本"""
        # Mock 图片和 OCR 结果
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        mock_ocr.return_value = '  Test OCR Result  '
        
        # 创建临时测试文件
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService()
            result = service.extract_text_from_image('test.png')
        
        assert result == 'Test OCR Result'
        mock_ocr.assert_called_once()

    def test_extract_text_from_image_file_not_found(self):
        """测试文件不存在的情况"""
        service = OCRService()
        
        with pytest.raises(FileNotFoundError):
            service.extract_text_from_image('/nonexistent/file.png')

    @patch('pytesseract.image_to_string')
    @patch('app.services.ocr_service.Image.open')
    def test_extract_text_from_image_with_config(self, mock_image_open, mock_ocr):
        """测试带有 Tesseract 配置参数的提取"""
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        mock_ocr.return_value = 'Result'
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService()
            result = service.extract_text_from_image('test.png', config='--psm 6')
        
        # 验证 config 参数被正确传递
        mock_ocr.assert_called_once()
        assert mock_ocr.call_args[1]['config'] == '--psm 6'

    @patch('pytesseract.image_to_string')
    @patch('app.services.ocr_service.Image.open')
    def test_extract_text_from_image_ocr_error(self, mock_image_open, mock_ocr):
        """测试 OCR 识别失败的情况"""
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        mock_ocr.side_effect = Exception('OCR Error')
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService()
            with pytest.raises(Exception) as exc_info:
                service.extract_text_from_image('test.png')
            
            assert 'OCR 识别失败' in str(exc_info.value)


class TestExtractTextFromBytes:
    """从字节流提取文本测试"""

    @patch('pytesseract.image_to_string')
    def test_extract_text_from_bytes_success(self, mock_ocr):
        """测试成功从字节流提取文本"""
        # 创建一个简单的图片字节流
        img = Image.new('RGB', (100, 100), color='white')
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        image_bytes = img_bytes.getvalue()
        
        mock_ocr.return_value = '  Test Result  '
        
        service = OCRService()
        result = service.extract_text_from_bytes(image_bytes)
        
        assert result == 'Test Result'
        mock_ocr.assert_called_once()

    def test_extract_text_from_bytes_empty(self):
        """测试空字节流的处理"""
        service = OCRService()
        
        with pytest.raises(Exception):
            service.extract_text_from_bytes(b'')

    @patch('pytesseract.image_to_string')
    def test_extract_text_from_bytes_invalid_image(self, mock_ocr):
        """测试无效的图片数据"""
        service = OCRService()
        
        with pytest.raises(Exception):
            service.extract_text_from_bytes(b'invalid image data')

    @patch('pytesseract.image_to_string')
    def test_extract_text_from_bytes_with_config(self, mock_ocr):
        """测试带有配置参数的字节流提取"""
        img = Image.new('RGB', (100, 100), color='white')
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        image_bytes = img_bytes.getvalue()
        
        mock_ocr.return_value = 'Result'
        
        service = OCRService()
        result = service.extract_text_from_bytes(image_bytes, config='--psm 6')
        
        # 验证 config 参数被正确传递
        assert mock_ocr.call_args[1]['config'] == '--psm 6'

    @patch('pytesseract.image_to_string')
    def test_extract_text_from_bytes_ocr_error(self, mock_ocr):
        """测试字节流 OCR 识别失败"""
        img = Image.new('RGB', (100, 100), color='white')
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        image_bytes = img_bytes.getvalue()
        
        mock_ocr.side_effect = Exception('OCR Error')
        
        service = OCRService()
        with pytest.raises(Exception) as exc_info:
            service.extract_text_from_bytes(image_bytes)
        
        assert 'OCR 识别失败' in str(exc_info.value)


class TestGetImageInfo:
    """获取图片信息测试"""

    @patch('pytesseract.image_to_data')
    @patch('app.services.ocr_service.Image.open')
    def test_get_image_info_success(self, mock_image_open, mock_data):
        """测试成功获取图片信息"""
        mock_img = MagicMock()
        mock_img.size = (100, 100)
        mock_img.format = 'PNG'
        mock_img.mode = 'RGB'
        mock_image_open.return_value = mock_img
        
        mock_data.return_value = {
            'level': [1, 2],
            'page_num': [1, 1],
            'block_num': [0, 1],
            'par_num': [0, 0],
            'line_num': [0, 1],
            'word_num': [0, 1],
            'left': [0, 10],
            'top': [0, 20],
            'width': [100, 50],
            'height': [100, 30],
            'conf': [0, 95],
            'text': ['', 'test']
        }
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService()
            info = service.get_image_info('test.png')
        
        assert 'image_size' in info
        assert 'image_format' in info
        assert 'image_mode' in info
        assert 'ocr_data' in info
        assert info['image_size'] == (100, 100)
        assert info['image_format'] == 'PNG'
        assert info['image_mode'] == 'RGB'

    def test_get_image_info_file_not_found(self):
        """测试文件不存在的情况"""
        service = OCRService()
        
        with pytest.raises(Exception) as exc_info:
            service.get_image_info('/nonexistent/file.png')
        
        assert '图片文件不存在' in str(exc_info.value)

    @patch('pytesseract.image_to_data')
    @patch('app.services.ocr_service.Image.open')
    def test_get_image_info_error(self, mock_image_open, mock_data):
        """测试获取图片信息失败"""
        mock_image_open.side_effect = Exception('Image Error')
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService()
            with pytest.raises(Exception) as exc_info:
                service.get_image_info('test.png')
            
            assert '获取图片信息失败' in str(exc_info.value)


class TestModuleLevelFunctions:
    """模块级函数测试"""

    @patch('app.services.ocr_service.OCRService.extract_text_from_image')
    @patch('app.services.ocr_service.get_ocr_service')
    def test_module_extract_text_from_image(self, mock_get_service, mock_extract):
        """测试模块级 extract_text_from_image 函数"""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_extract.return_value = 'Test'
        
        result = extract_text_from_image('test.png')
        
        mock_get_service.assert_called_once()
        mock_service.extract_text_from_image.assert_called_once_with('test.png')

    @patch('app.services.ocr_service.OCRService.extract_text_from_bytes')
    @patch('app.services.ocr_service.get_ocr_service')
    def test_module_extract_text_from_bytes(self, mock_get_service, mock_extract):
        """测试模块级 extract_text_from_bytes 函数"""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_extract.return_value = 'Test'
        
        image_bytes = b'test'
        result = extract_text_from_bytes(image_bytes)
        
        mock_get_service.assert_called_once()
        mock_service.extract_text_from_bytes.assert_called_once_with(image_bytes)


class TestLanguageHandling:
    """语言处理测试"""

    @patch('pytesseract.image_to_string')
    @patch('app.services.ocr_service.Image.open')
    def test_chinese_language_recognition(self, mock_image_open, mock_ocr):
        """测试中文识别"""
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        mock_ocr.return_value = '你好世界'
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService(lang='chi_sim')
            result = service.extract_text_from_image('test.png')
        
        assert result == '你好世界'
        assert mock_ocr.call_args[1]['lang'] == 'chi_sim'

    @patch('pytesseract.image_to_string')
    @patch('app.services.ocr_service.Image.open')
    def test_english_language_recognition(self, mock_image_open, mock_ocr):
        """测试英文识别"""
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        mock_ocr.return_value = 'Hello World'
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService(lang='eng')
            result = service.extract_text_from_image('test.png')
        
        assert result == 'Hello World'
        assert mock_ocr.call_args[1]['lang'] == 'eng'

    @patch('pytesseract.image_to_string')
    @patch('app.services.ocr_service.Image.open')
    def test_multilanguage_recognition(self, mock_image_open, mock_ocr):
        """测试多语言识别"""
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        mock_ocr.return_value = '会议 Meeting'
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService(lang='chi_sim+eng')
            result = service.extract_text_from_image('test.png')
        
        assert result == '会议 Meeting'
        assert mock_ocr.call_args[1]['lang'] == 'chi_sim+eng'


class TestErrorHandling:
    """错误处理测试"""

    @patch('pytesseract.image_to_string')
    @patch('app.services.ocr_service.Image.open')
    def test_image_open_exception(self, mock_image_open, mock_ocr):
        """测试图片打开异常"""
        mock_image_open.side_effect = Exception('Cannot open image')
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService()
            with pytest.raises(Exception) as exc_info:
                service.extract_text_from_image('test.png')
            
            assert 'OCR 识别失败' in str(exc_info.value)

    def test_extract_with_corrupted_bytes(self):
        """测试损坏的图片字节流"""
        service = OCRService()
        corrupted_bytes = b'\x89PNG\r\n\x1a\n' + b'corrupted'
        
        with pytest.raises(Exception):
            service.extract_text_from_bytes(corrupted_bytes)


class TestRealImageRecognition:
    """真实图片识别测试"""
    
    def test_recognize_real_image_from_file(self):
        """
        测试从真实图片文件识别文本
        
        此测试使用 tests/image 目录中的真实图片
        并将识别结果打印到控制台
        """
        # 获取测试图片路径
        test_image_dir = Path(__file__).parent / "image"
        
        # 查找第一个 PNG 或 JPG 文件
        image_files = list(test_image_dir.glob("*.png")) + list(test_image_dir.glob("*.jpg"))
        
        if not image_files:
            pytest.skip("没有找到测试图片文件")
        
        image_path = image_files[0]
        print(f"\n\n{'='*60}")
        print(f"测试图片: {image_path.name}")
        print(f"完整路径: {image_path}")
        print(f"{'='*60}\n")
        
        # 检查 Tesseract 是否可用
        service = OCRService()
        if not service.is_tesseract_available():
            pytest.skip("Tesseract OCR 未安装，无法运行此测试")
        
        try:
            # 执行 OCR 识别
            print("⏳ 正在识别文本...")
            text = service.extract_text_from_image(str(image_path))
            
            # 打印识别结果
            print(f"✅ 识别成功！")
            print(f"\n识别结果:")
            print(f"{'-'*60}")
            print(text)
            print(f"{'-'*60}\n")
            
            # 打印文本统计信息
            lines = text.strip().split('\n')
            print(f"📊 统计信息:")
            print(f"  - 总字符数: {len(text)}")
            print(f"  - 总行数: {len(lines)}")
            print(f"  - 平均行长: {len(text) // len(lines) if lines else 0}")
            print(f"\n{'='*60}\n")
            
            # 断言识别到了文本
            assert len(text) > 0, "OCR 未识别到任何文本"
            
        except Exception as e:
            print(f"\n❌ 识别失败: {str(e)}\n")
            raise
    
    def test_recognize_real_image_from_bytes(self):
        """
        测试从真实图片字节流识别文本
        
        此测试读取 tests/image 目录中的真实图片并转换为字节流
        """
        # 获取测试图片路径
        test_image_dir = Path(__file__).parent / "image"
        
        # 查找第一个 PNG 或 JPG 文件
        image_files = list(test_image_dir.glob("*.png")) + list(test_image_dir.glob("*.jpg"))
        
        if not image_files:
            pytest.skip("没有找到测试图片文件")
        
        image_path = image_files[0]
        print(f"\n\n{'='*60}")
        print(f"测试字节流识别: {image_path.name}")
        print(f"{'='*60}\n")
        
        # 检查 Tesseract 是否可用
        service = OCRService()
        if not service.is_tesseract_available():
            pytest.skip("Tesseract OCR 未安装，无法运行此测试")
        
        try:
            # 读取图片文件为字节流
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            print(f"📁 文件大小: {len(image_bytes)} bytes")
            print(f"⏳ 正在识别文本...\n")
            
            # 执行 OCR 识别
            text = service.extract_text_from_bytes(image_bytes)
            
            # 打印识别结果
            print(f"✅ 识别成功！")
            print(f"\n识别结果:")
            print(f"{'-'*60}")
            print(text)
            print(f"{'-'*60}\n")
            
            # 断言识别到了文本
            assert len(text) > 0, "OCR 未识别到任何文本"
            
        except Exception as e:
            print(f"\n❌ 识别失败: {str(e)}\n")
            raise
    
    def test_recognize_real_image_get_info(self):
        """
        获取真实图片的详细信息和 OCR 数据
        
        此测试获取并打印图片的详细信息和 OCR 识别的详细数据
        """
        # 获取测试图片路径
        test_image_dir = Path(__file__).parent / "image"
        
        # 查找第一个 PNG 或 JPG 文件
        image_files = list(test_image_dir.glob("*.png")) + list(test_image_dir.glob("*.jpg"))
        
        if not image_files:
            pytest.skip("没有找到测试图片文件")
        
        image_path = image_files[0]
        print(f"\n\n{'='*60}")
        print(f"获取图片详细信息: {image_path.name}")
        print(f"{'='*60}\n")
        
        # 检查 Tesseract 是否可用
        service = OCRService()
        if not service.is_tesseract_available():
            pytest.skip("Tesseract OCR 未安装，无法运行此测试")
        
        try:
            # 获取图片信息
            print("⏳ 正在获取图片信息...")
            info = service.get_image_info(str(image_path))
            
            # 打印图片信息
            print(f"\n✅ 获取成功！")
            print(f"\n📷 图片基本信息:")
            print(f"  - 尺寸: {info['image_size']}")
            print(f"  - 格式: {info['image_format']}")
            print(f"  - 色彩模式: {info['image_mode']}")
            
            # 打印 OCR 数据摘要
            ocr_data = info['ocr_data']
            print(f"\n🔍 OCR 识别数据摘要:")
            
            if 'text' in ocr_data and ocr_data['text']:
                # 过滤出非空的文本
                texts = [t for t in ocr_data['text'] if t.strip()]
                print(f"  - 识别的词数: {len(texts)}")
                print(f"  - 识别的词列表: {texts[:10]}")  # 显示前 10 个词
            
            if 'conf' in ocr_data:
                confs = [c for c in ocr_data['conf'] if c > 0]
                if confs:
                    avg_conf = sum(confs) / len(confs)
                    print(f"  - 平均置信度: {avg_conf:.2f}%")
            
            print(f"\n{'='*60}\n")
            
        except Exception as e:
            print(f"\n❌ 获取信息失败: {str(e)}\n")
            raise


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
