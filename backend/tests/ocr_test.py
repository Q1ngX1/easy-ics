"""
OCR Service Unit Tests
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
    """OCR Service Initialization Tests"""

    def test_ocr_service_init_default_language(self):
        service = OCRService()
        assert service.lang == 'chi_sim+eng'

    def test_ocr_service_init_custom_language(self):
        service = OCRService(lang='eng')
        assert service.lang == 'eng'

    def test_get_ocr_service_singleton(self):
        service1 = get_ocr_service()
        service2 = get_ocr_service()
        assert service1 is service2


class TestTesseractAvailability:
    """Tesseract Availability Tests"""
    
    @patch('pytesseract.get_tesseract_version')
    def test_is_tesseract_available_true(self, mock_version):
        """Test Tesseract availability"""
        mock_version.return_value = 'tesseract 5.3.4'
        
        service = OCRService()
        result = service.is_tesseract_available()
        
        assert result is True
        mock_version.assert_called_once()

    @patch('pytesseract.get_tesseract_version')
    def test_is_tesseract_available_false(self, mock_version):
        """Test Tesseract unavailability"""
        mock_version.side_effect = Exception('Tesseract not found')
        
        service = OCRService()
        result = service.is_tesseract_available()
        
        assert result is False


class TestLanguageSupport:
    """Language Support Tests"""

    @patch('pytesseract.get_languages')
    def test_get_available_languages_success(self, mock_langs):
        """Test retrieving supported languages list"""
        mock_langs.return_value = ['chi_sim', 'chi_tra', 'eng', 'jpn']
        
        service = OCRService()
        languages = service.get_available_languages()
        
        assert isinstance(languages, list)
        assert 'chi_sim' in languages
        assert 'eng' in languages

    @patch('pytesseract.get_languages')
    def test_get_available_languages_error(self, mock_langs):
        """Test retrieving language list returns empty when error occurs"""
        mock_langs.side_effect = Exception('Error getting languages')
        
        service = OCRService()
        languages = service.get_available_languages()
        
        assert languages == []


class TestExtractTextFromImage:
    """Extract Text From Image File Tests"""

    @patch('pytesseract.image_to_string')
    @patch('app.services.ocr_service.Image.open')
    def test_extract_text_from_image_success(self, mock_image_open, mock_ocr):
        """Test successfully extracting text from image"""
        # Mock image and OCR result
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        mock_ocr.return_value = '  Test OCR Result  '
        
        # Create temporary test file
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService()
            result = service.extract_text_from_image('test.png')
        
        assert result == 'Test OCR Result'
        mock_ocr.assert_called_once()

    def test_extract_text_from_image_file_not_found(self):
        """Test file not found scenario"""
        service = OCRService()
        
        with pytest.raises(FileNotFoundError):
            service.extract_text_from_image('/nonexistent/file.png')

    @patch('pytesseract.image_to_string')
    @patch('app.services.ocr_service.Image.open')
    def test_extract_text_from_image_with_config(self, mock_image_open, mock_ocr):
        """Test extraction with Tesseract config parameters"""
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        mock_ocr.return_value = 'Result'
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService()
            result = service.extract_text_from_image('test.png', config='--psm 6')
        
        # Verify config parameter is passed correctly
        mock_ocr.assert_called_once()
        assert mock_ocr.call_args[1]['config'] == '--psm 6'

    @patch('pytesseract.image_to_string')
    @patch('app.services.ocr_service.Image.open')
    def test_extract_text_from_image_ocr_error(self, mock_image_open, mock_ocr):
        """Test OCR recognition failure scenario"""
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        mock_ocr.side_effect = Exception('OCR Error')
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService()
            with pytest.raises(Exception) as exc_info:
                service.extract_text_from_image('test.png')
            
            assert 'OCR recognition failed' in str(exc_info.value)


class TestExtractTextFromBytes:
    """Extract Text From Bytes Stream Tests"""

    @patch('pytesseract.image_to_string')
    def test_extract_text_from_bytes_success(self, mock_ocr):
        """Test successfully extracting text from bytes stream"""
        # Create a simple image bytes stream
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
        """Test handling of empty bytes stream"""
        service = OCRService()
        
        with pytest.raises(Exception):
            service.extract_text_from_bytes(b'')

    @patch('pytesseract.image_to_string')
    def test_extract_text_from_bytes_invalid_image(self, mock_ocr):
        """Test invalid image data"""
        service = OCRService()
        
        with pytest.raises(Exception):
            service.extract_text_from_bytes(b'invalid image data')

    @patch('pytesseract.image_to_string')
    def test_extract_text_from_bytes_with_config(self, mock_ocr):
        """Test extraction from bytes with config parameters"""
        img = Image.new('RGB', (100, 100), color='white')
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        image_bytes = img_bytes.getvalue()
        
        mock_ocr.return_value = 'Result'
        
        service = OCRService()
        result = service.extract_text_from_bytes(image_bytes, config='--psm 6')
        
        # Verify config parameter is passed correctly
        assert mock_ocr.call_args[1]['config'] == '--psm 6'

    @patch('pytesseract.image_to_string')
    def test_extract_text_from_bytes_ocr_error(self, mock_ocr):
        """Test bytes extraction OCR recognition failure"""
        img = Image.new('RGB', (100, 100), color='white')
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        image_bytes = img_bytes.getvalue()
        
        mock_ocr.side_effect = Exception('OCR Error')
        
        service = OCRService()
        with pytest.raises(Exception) as exc_info:
            service.extract_text_from_bytes(image_bytes)
        
        assert 'OCR recognition failed' in str(exc_info.value)


class TestGetImageInfo:
    """Get Image Info Tests"""

    @patch('pytesseract.image_to_data')
    @patch('app.services.ocr_service.Image.open')
    def test_get_image_info_success(self, mock_image_open, mock_data):
        """Test successfully retrieving image info"""
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
        """Test file not found scenario"""
        service = OCRService()
        
        with pytest.raises(Exception) as exc_info:
            service.get_image_info('/nonexistent/file.png')
        
        assert 'Image file not found' in str(exc_info.value)

    @patch('pytesseract.image_to_data')
    @patch('app.services.ocr_service.Image.open')
    def test_get_image_info_error(self, mock_image_open, mock_data):
        """Test getting image info failure"""
        mock_image_open.side_effect = Exception('Image Error')
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService()
            with pytest.raises(Exception) as exc_info:
                service.get_image_info('test.png')
            
            assert 'Failed to get image info' in str(exc_info.value)


class TestModuleLevelFunctions:
    """Module Level Functions Tests"""

    @patch('app.services.ocr_service.OCRService.extract_text_from_image')
    @patch('app.services.ocr_service.get_ocr_service')
    def test_module_extract_text_from_image(self, mock_get_service, mock_extract):
        """Test module level extract_text_from_image function"""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_extract.return_value = 'Test'
        
        result = extract_text_from_image('test.png')
        
        mock_get_service.assert_called_once()
        mock_service.extract_text_from_image.assert_called_once_with('test.png')

    @patch('app.services.ocr_service.OCRService.extract_text_from_bytes')
    @patch('app.services.ocr_service.get_ocr_service')
    def test_module_extract_text_from_bytes(self, mock_get_service, mock_extract):
        """Test module level extract_text_from_bytes function"""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service
        mock_extract.return_value = 'Test'
        
        image_bytes = b'test'
        result = extract_text_from_bytes(image_bytes)
        
        mock_get_service.assert_called_once()
        mock_service.extract_text_from_bytes.assert_called_once_with(image_bytes)


class TestLanguageHandling:
    """Language Handling Tests"""

    @patch('pytesseract.image_to_string')
    @patch('app.services.ocr_service.Image.open')
    def test_chinese_language_recognition(self, mock_image_open, mock_ocr):
        """Test Chinese language recognition"""
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        mock_ocr.return_value = 'Hello World'
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService(lang='chi_sim')
            result = service.extract_text_from_image('test.png')
        
        assert result == 'Hello World'
        assert mock_ocr.call_args[1]['lang'] == 'chi_sim'

    @patch('pytesseract.image_to_string')
    @patch('app.services.ocr_service.Image.open')
    def test_english_language_recognition(self, mock_image_open, mock_ocr):
        """Test English language recognition"""
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
        """Test multi-language recognition"""
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        mock_ocr.return_value = '会议 Meeting'
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService(lang='chi_sim+eng')
            result = service.extract_text_from_image('test.png')
        
        assert result == '会议 Meeting'
        assert mock_ocr.call_args[1]['lang'] == 'chi_sim+eng'


class TestErrorHandling:
    """Error Handling Tests"""

    @patch('pytesseract.image_to_string')
    @patch('app.services.ocr_service.Image.open')
    def test_image_open_exception(self, mock_image_open, mock_ocr):
        """Test image opening exception"""
        mock_image_open.side_effect = Exception('Cannot open image')
        
        with patch('pathlib.Path.exists', return_value=True):
            service = OCRService()
            with pytest.raises(Exception) as exc_info:
                service.extract_text_from_image('test.png')
            
            assert 'OCR recognition failed' in str(exc_info.value)

    def test_extract_with_corrupted_bytes(self):
        """Test corrupted image bytes stream"""
        service = OCRService()
        corrupted_bytes = b'\x89PNG\r\n\x1a\n' + b'corrupted'
        
        with pytest.raises(Exception):
            service.extract_text_from_bytes(corrupted_bytes)

class TestRealImageRecognition:
    """Real Image Recognition Tests"""
    
    def test_recognize_real_image_from_file(self):
        """Test real image recognition from file"""
        # Get test image path
        test_image_dir = Path(__file__).parent / "image"
        
        # Find all PNG or JPG files
        image_files = list(test_image_dir.glob("*.png")) + list(test_image_dir.glob("*.jpg"))
        
        if not image_files:
            pytest.skip("No test image files found")
        
        # Check if Tesseract is available
        service = OCRService()
        if not service.is_tesseract_available():
            pytest.skip("Tesseract OCR not installed, cannot run this test")
        
        print(f"\n\n{'='*60}")
        print(f"Testing {len(image_files)} image(s) from file")
        print(f"{'='*60}\n")
        
        successful_count = 0
        failed_files = []
        
        for idx, image_path in enumerate(image_files, 1):
            print(f"\n[{idx}/{len(image_files)}] Processing: {image_path.name}")
            print(f"Full path: {image_path}")
            
            try:
                # Execute OCR recognition
                print("⏳ Recognizing text...")
                text = service.extract_text_from_image(str(image_path))
                
                # Print recognition result
                print(f"✓ Recognition successful!")
                print(f"Text (first 100 chars): {text[:100]}...")
                
                # Print text statistics
                lines = text.strip().split('\n')
                print(f"📊 Statistics:")
                print(f"  - Total characters: {len(text)}")
                print(f"  - Total lines: {len(lines)}")
                print(f"  - Average line length: {len(text) // len(lines) if lines else 0}")
                
                # Assert text was recognized
                assert len(text) > 0, "OCR did not recognize any text"
                successful_count += 1
                
            except Exception as e:
                print(f"✘ Recognition failed: {str(e)}")
                failed_files.append((image_path.name, str(e)))
        
        print(f"\n{'='*60}")
        print(f"Summary: {successful_count}/{len(image_files)} files processed successfully")
        if failed_files:
            print(f"\nFailed files:")
            for filename, error in failed_files:
                print(f"  - {filename}: {error}")
        print(f"{'='*60}\n")
        
        # Assert at least one file was processed successfully
        assert successful_count > 0, f"No files were successfully processed. Failed: {len(failed_files)}"
    
    def test_recognize_real_image_from_bytes(self):
        """
        Test real image recognition from bytes stream
        
        This test reads all real images from tests/image directory and converts to bytes stream
        """
        # Get test image path
        test_image_dir = Path(__file__).parent / "image"
        
        # Find all PNG or JPG files
        image_files = list(test_image_dir.glob("*.png")) + list(test_image_dir.glob("*.jpg"))
        
        if not image_files:
            pytest.skip("No test image files found")
        
        # Check if Tesseract is available
        service = OCRService()
        if not service.is_tesseract_available():
            pytest.skip("Tesseract OCR not installed, cannot run this test")
        
        print(f"\n\n{'='*60}")
        print(f"Testing {len(image_files)} image(s) from bytes stream")
        print(f"{'='*60}\n")
        
        successful_count = 0
        failed_files = []
        
        for idx, image_path in enumerate(image_files, 1):
            print(f"\n[{idx}/{len(image_files)}] Processing: {image_path.name}")
            
            try:
                # Read image file as bytes stream
                with open(image_path, 'rb') as f:
                    image_bytes = f.read()
                
                print(f"📁 File size: {len(image_bytes)} bytes")
                print(f"⏳ Recognizing text...")
                
                # Execute OCR recognition
                text = service.extract_text_from_bytes(image_bytes)
                
                # Print recognition result
                print(f"✓ Recognition successful!")
                print(f"Text (first 100 chars): {text[:100]}...")
                
                # Assert text was recognized
                assert len(text) > 0, "OCR did not recognize any text"
                successful_count += 1
                
            except Exception as e:
                print(f"✘ Recognition failed: {str(e)}")
                failed_files.append((image_path.name, str(e)))
        
        print(f"\n{'='*60}")
        print(f"Summary: {successful_count}/{len(image_files)} files processed successfully")
        if failed_files:
            print(f"\nFailed files:")
            for filename, error in failed_files:
                print(f"  - {filename}: {error}")
        print(f"{'='*60}\n")
        
        # Assert at least one file was processed successfully
        assert successful_count > 0, f"No files were successfully processed. Failed: {len(failed_files)}"
    
    def test_recognize_real_image_get_info(self):
        """
        Get detailed information and OCR data for real images
        
        This test retrieves and prints detailed image information and OCR recognition data for all images
        """
        # Get test image path
        test_image_dir = Path(__file__).parent / "image"
        
        # Find all PNG or JPG files
        image_files = list(test_image_dir.glob("*.png")) + list(test_image_dir.glob("*.jpg"))
        
        if not image_files:
            pytest.skip("No test image files found")
        
        # Check if Tesseract is available
        service = OCRService()
        if not service.is_tesseract_available():
            pytest.skip("Tesseract OCR not installed, cannot run this test")
        
        print(f"\n\n{'='*60}")
        print(f"Getting detailed info for {len(image_files)} image(s)")
        print(f"{'='*60}\n")
        
        successful_count = 0
        failed_files = []
        
        for idx, image_path in enumerate(image_files, 1):
            print(f"\n[{idx}/{len(image_files)}] Processing: {image_path.name}")
            
            try:
                # Get image info
                print("⏳ Getting image information...")
                info = service.get_image_info(str(image_path))
                
                # Print image info
                print(f"✓ Success!")
                print(f"📷 Image information:")
                print(f"  - Size: {info['image_size']}")
                print(f"  - Format: {info['image_format']}")
                print(f"  - Color mode: {info['image_mode']}")
                
                # Print OCR data summary
                ocr_data = info['ocr_data']
                print(f"🔍 OCR data summary:")
                
                if 'text' in ocr_data and ocr_data['text']:
                    # Filter non-empty text
                    texts = [t for t in ocr_data['text'] if t.strip()]
                    print(f"  - Words recognized: {len(texts)}")
                    if texts:
                        print(f"  - First 5 words: {texts[:5]}")
                
                if 'conf' in ocr_data:
                    confs = [c for c in ocr_data['conf'] if c > 0]
                    if confs:
                        avg_conf = sum(confs) / len(confs)
                        print(f"  - Average confidence: {avg_conf:.2f}%")
                
                successful_count += 1
                
            except Exception as e:
                print(f"✘ Failed to get info: {str(e)}")
                failed_files.append((image_path.name, str(e)))
        
        print(f"\n{'='*60}")
        print(f"Summary: {successful_count}/{len(image_files)} files processed successfully")
        if failed_files:
            print(f"\nFailed files:")
            for filename, error in failed_files:
                print(f"  - {filename}: {error}")
        print(f"{'='*60}\n")
        
        # Assert at least one file was processed successfully
        assert successful_count > 0, f"No files were successfully processed. Failed: {len(failed_files)}"