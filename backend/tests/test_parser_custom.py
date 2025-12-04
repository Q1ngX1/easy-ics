"""
Test suite for ParserService - Tests each field extraction independently.

Usage:
1. Modify the TEST_INPUT variable with your test text
2. Run the tests to verify each field extraction
"""

import pytest
from datetime import datetime
import sys
from pathlib import Path

# Add backend directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.parser_service import ParserService, get_parser_service

# Color output support
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class Fore:
        GREEN = ""
        BLUE = ""
        YELLOW = ""
        RED = ""
        CYAN = ""
    class Style:
        BRIGHT = ""
        RESET_ALL = ""


# ============================================================================
# Test Configuration - Modify this to test with your own input
# ============================================================================

TEST_INPUT = """
Team Meeting，Location: Conference Room A，Date: 2025/11/24-2025/11/25, 14:30，Important project discussion with urgent priority
"""


class TestParserServiceFields:
    """Test individual field extraction from ParserService."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test."""
        self.parser = get_parser_service()
    
    def test_title_extraction(self):
        """Test event title extraction."""
        events = self.parser.parse(TEST_INPUT)
        assert len(events) > 0
        assert events[0].title is not None
        print(f"{Fore.GREEN}✓ Title:{Style.RESET_ALL} {Fore.CYAN}{events[0].title}{Style.RESET_ALL}")
    
    def test_date_extraction(self):
        """Test event start date extraction."""
        events = self.parser.parse(TEST_INPUT)
        assert len(events) > 0
        assert events[0].start_time is not None
        assert isinstance(events[0].start_time, datetime)
        print(f"{Fore.GREEN}✓ Start Date:{Style.RESET_ALL} {Fore.CYAN}{events[0].start_time}{Style.RESET_ALL}")
    
    def test_end_date_extraction(self):
        """Test event end date extraction (default: 1 hour after start)."""
        events = self.parser.parse(TEST_INPUT)
        assert len(events) > 0
        assert events[0].end_time is not None
        assert isinstance(events[0].end_time, datetime)
        print(f"{Fore.GREEN}✓ End Date:{Style.RESET_ALL} {Fore.CYAN}{events[0].end_time}{Style.RESET_ALL}")
    
    def test_location_extraction(self):
        """Test location extraction."""
        events = self.parser.parse(TEST_INPUT)
        assert len(events) > 0
        location = events[0].location
        print(f"{Fore.GREEN}✓ Location:{Style.RESET_ALL} {Fore.CYAN}{location}{Style.RESET_ALL}")
    
    def test_description_extraction(self):
        """Test description/details extraction."""
        events = self.parser.parse(TEST_INPUT)
        assert len(events) > 0
        description = events[0].description
        print(f"{Fore.GREEN}✓ Description:{Style.RESET_ALL} {Fore.CYAN}{description}{Style.RESET_ALL}")
    
    def test_priority_extraction(self):
        """Test priority extraction."""
        events = self.parser.parse(TEST_INPUT)
        assert len(events) > 0
        assert events[0].priority is not None
        print(f"{Fore.GREEN}✓ Priority:{Style.RESET_ALL} {Fore.YELLOW}{events[0].priority}{Style.RESET_ALL}")
    
    def test_reminder_minutes(self):
        """Test reminder minutes (default: 15)."""
        events = self.parser.parse(TEST_INPUT)
        assert len(events) > 0
        assert events[0].reminder_minutes == 15
        print(f"{Fore.GREEN}✓ Reminder Minutes:{Style.RESET_ALL} {Fore.CYAN}{events[0].reminder_minutes}{Style.RESET_ALL}")
    
    def test_full_event_object(self):
        """Test complete event object creation."""
        events = self.parser.parse(TEST_INPUT)
        assert len(events) > 0
        event = events[0]
        
        # Verify all required fields exist
        assert hasattr(event, 'title')
        assert hasattr(event, 'start_time')
        assert hasattr(event, 'end_time')
        assert hasattr(event, 'location')
        assert hasattr(event, 'description')
        assert hasattr(event, 'priority')
        assert hasattr(event, 'reminder_minutes')
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ Full Event Object:{Style.RESET_ALL}")
        print(f"{Fore.BLUE}  Title:{Style.RESET_ALL} {Fore.CYAN}{event.title}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}  Start:{Style.RESET_ALL} {Fore.CYAN}{event.start_time}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}  End:{Style.RESET_ALL} {Fore.CYAN}{event.end_time}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}  Location:{Style.RESET_ALL} {Fore.CYAN}{event.location}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}  Description:{Style.RESET_ALL} {Fore.CYAN}{event.description}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}  Priority:{Style.RESET_ALL} {Fore.YELLOW}{event.priority}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}  Reminder:{Style.RESET_ALL} {Fore.CYAN}{event.reminder_minutes} minutes{Style.RESET_ALL}")


class TestTextPreprocessing:
    """Test text preprocessing functionality."""
    
    def test_trim_text_basic(self):
        """Test basic text trimming."""
        text = "  hello world  "
        result = ParserService.trim_text(text)
        assert result == "hello world"
        print(f"{Fore.GREEN}✓ Trim basic:{Style.RESET_ALL} {Fore.YELLOW}'{text}'{Style.RESET_ALL} -> {Fore.CYAN}'{result}'{Style.RESET_ALL}")
    
    def test_trim_text_newlines(self):
        """Test newline normalization."""
        text = "line1\nline2\nline3"
        result = ParserService.trim_text(text)
        assert "\n" not in result
        print(f"{Fore.GREEN}✓ Trim newlines:{Style.RESET_ALL} {Fore.YELLOW}'{text}'{Style.RESET_ALL} -> {Fore.CYAN}'{result}'{Style.RESET_ALL}")
    
    def test_trim_text_chinese_punctuation(self):
        """Test Chinese punctuation normalization."""
        text = "时间：下午3点，地址：会议室"
        result = ParserService.trim_text(text)
        assert "：" not in result
        assert "，" not in result
        print(f"{Fore.GREEN}✓ Trim Chinese punctuation:{Style.RESET_ALL} {Fore.YELLOW}'{text}'{Style.RESET_ALL} -> {Fore.CYAN}'{result}'{Style.RESET_ALL}")


if __name__ == "__main__":
    # Run with: pytest test_parser_custom.py -v -s
    print(f"{Fore.BLUE}{'=' * 80}")
    print(f"{Fore.GREEN}{Style.BRIGHT}ParserService Field Extraction Tests{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'=' * 80}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Test Input:{Style.RESET_ALL}\n{TEST_INPUT}\n")
    print(f"{Fore.BLUE}{'=' * 80}{Style.RESET_ALL}")
    pytest.main([__file__, "-v", "-s"])
