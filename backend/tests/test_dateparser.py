"""
Test script for DateParserService
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.services.parser.dateparser_parser import DateParserService
from datetime import datetime


def test_dateparser_service():
    """Test the DateParserService"""
    
    service = DateParserService(timezone='Asia/Shanghai')
    
    print("\n" + "="*60)
    print("DateParserService Test")
    print("="*60 + "\n")
    
    # Test cases
    test_cases = [
        "明天下午2点开会",
        "下周一上午10点在会议室A讨论项目",
        "后天2点半在楼下咖啡厅1小时的讨论会",
        "今天晚上7点吃饭",
        "下周三下午3点，在会议室B，讨论下个月的计划，预计1.5小时",
        "明年元旦上午10点跨年聚餐",
    ]
    
    for text in test_cases:
        print(f"📝 Input: {text}")
        try:
            result = service.parse_event(text)
            print(f"✅ Title: {result['title']}")
            print(f"   Start: {result['start_time']}")
            print(f"   End: {result['end_time']}")
            print(f"   Location: {result['location'] or '(未指定)'}")
            print(f"   Duration: {result['duration_minutes']} minutes")
            print(f"   Confidence: {result['confidence']:.0%}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        print()


def test_multiple_events():
    """Test parsing multiple events"""
    
    service = DateParserService(timezone='Asia/Shanghai')
    
    print("\n" + "="*60)
    print("Multiple Events Test")
    print("="*60 + "\n")
    
    text = """
    明天下午2点开会讨论项目。
    后天上午10点在会议室A开站会。
    下周一晚上6点聚餐。
    """
    
    print(f"📝 Input text:\n{text}")
    print("\n✅ Parsed events:\n")
    
    events = service.parse_multiple_events(text)
    
    for i, event in enumerate(events, 1):
        print(f"{i}. {event['title']}")
        print(f"   📅 {event['start_time']} - {event['end_time']}")
        print(f"   📍 {event['location'] or '(未指定)'}")
        print()


def test_parser_service():
    """Test the ParserService integration"""
    
    from app.services.parser_service import ParserService
    
    print("\n" + "="*60)
    print("ParserService Integration Test")
    print("="*60 + "\n")
    
    parser = ParserService()
    
    test_texts = [
        "明天下午2点在会议室A开会",
        "下周一上午10点讨论项目，预计1小时",
    ]
    
    for text in test_texts:
        print(f"📝 Input: {text}")
        try:
            event = parser.parse(text, timezone='Asia/Shanghai')
            print(f"✅ Event created:")
            print(f"   Title: {event.title}")
            print(f"   Start: {event.start_time}")
            print(f"   End: {event.end_time}")
            print(f"   Location: {event.location}")
            print(f"   Duration: {event.duration_hours():.1f} hours")
            print()
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")


if __name__ == "__main__":
    print("\n🚀 Running DateParserService Tests...\n")
    
    try:
        test_dateparser_service()
        test_multiple_events()
        test_parser_service()
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("="*60 + "\n")
        
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("\nPlease install required packages:")
        print("  pip install dateparser")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
