from typing import List, Optional
import logging
from datetime import datetime, timedelta
from app.models.event import Event, EventPriority
from app.services.parser import re_parser

logger = logging.getLogger(__name__)


class ParserService:
    def __init__(self):
        self.dateparser_service = None

    def parse(self, text: str, timezone: Optional[str] = None) -> List[Event]:
        """
        Parse text content and extract event information.
        
        Processing pipeline:
        1. Text normalization (trim, clean)
        2. Date/time extraction
        3. Event title extraction
        4. Location extraction (if available)
        5. Create Event objects
        
        Args:
            text: Plain text content to parse
            timezone: Optional IANA timezone string (e.g., 'Asia/Shanghai')
            
        Returns:
            List of Event objects extracted from text
            
        Raises:
            ValueError: If text is empty or invalid
        """
        events = []
        
        try:
            # Step 1: Validate input
            if not text or text.strip() == "":
                raise ValueError("Text content cannot be empty")
            
            # Step 2: Normalize and clean text
            cleaned_text = re_parser.trim_text(text)
            logger.debug(f"Cleaned text: {cleaned_text}")
            
            # Step 3: Extract date/time information
            parsed_date = self._extract_datetime(cleaned_text)
            if not parsed_date:
                logger.warning("No date found in text, using current date as fallback")
                parsed_date = datetime.now()
            
            # Step 4: Extract title (first sentence or first line)
            title = self._extract_title(cleaned_text)
            if not title:
                title = "Untitled Event"
            
            # Step 5: Extract location (if available)
            location = self._extract_location(cleaned_text)
            
            # Step 6: Extract description or additional details
            description = self._extract_description(cleaned_text)
            
            # Step 7: Determine end time (default: 1 hour after start)
            end_time = parsed_date + timedelta(hours=1)
            
            # Step 8: Determine priority (if mentioned in text)
            priority = self._extract_priority(cleaned_text)
            
            # Step 9: Create Event object
            event = Event(
                title=title,
                start_time=parsed_date,
                end_time=end_time,
                location=location,
                description=description,
                priority=priority,
                reminder_minutes=15  # Default: 15 minutes before
            )
            events.append(event)
            
            logger.info(f"Successfully parsed 1 event: {event}")
            
        except ValueError as e:
            logger.error(f"Validation error in parser service: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in parser service: {e}", exc_info=True)
            raise
        
        return events

    def _extract_datetime(self, text: str) -> Optional[datetime]:
        """
        Extract date and time from text using multiple strategies.
        
        Tries in order:
        1. dateparser with language support
        2. Simple regex patterns
        
        Args:
            text: Cleaned text to parse
            
        Returns:
            datetime object if found, None otherwise
        """
        try:
            # Try dateparser first (more robust for natural language)
            dt = re_parser.parse_date_with_dateparser(text, languages=["en", "zh"])
            if dt:
                return dt
            
            # Fallback to simple regex parsing
            dt = re_parser.parse_simple_date(text)
            return dt
            
        except Exception as e:
            logger.warning(f"Error extracting datetime: {e}")
            return None

    def _extract_title(self, text: str) -> Optional[str]:
        """
        Extract event title from text.
        
        Heuristics:
        1. First line if it's short (< 100 chars) and doesn't contain numbers
        2. First sentence if separated by punctuation
        3. Text before first date mention
        
        Args:
            text: Cleaned text
            
        Returns:
            Extracted title or None
        """
        try:
            lines = text.split('\n')
            if lines:
                first_line = lines[0].strip()
                # If first line is reasonably short, use as title
                if first_line and len(first_line) < 100:
                    # Remove date-like content from title
                    title = re_parser.re.sub(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}', '', first_line).strip()
                    if title:
                        return title
            
            # Try to extract text before first date pattern
            import re as regex_module
            match = regex_module.search(r'([^:。.!\n?]{5,100}?)[\s:：]*\d{4}[-/年]', text)
            if match:
                title = match.group(1).strip()
                if title:
                    return title
            
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting title: {e}")
            return None

    def _extract_location(self, text: str) -> Optional[str]:
        """
        Extract location from text.
        
        Looks for patterns like:
        - "地点: xxx" / "Location: xxx"
        - "会议室" / "Conference Room"
        - Common location keywords
        
        Args:
            text: Cleaned text
            
        Returns:
            Extracted location or None
        """
        try:
            import re as regex_module
            
            # Pattern 1: "地点: xxx" or "Location: xxx"
            patterns = [
                r'地点[:：]\s*([^\n,，。;；]*)',
                r'location[:：]\s*([^\n,，。;；]*)',
                r'地址[:：]\s*([^\n,，。;；]*)',
                r'会议地点[:：]\s*([^\n,，。;；]*)',
            ]
            
            for pattern in patterns:
                match = regex_module.search(pattern, text, regex_module.IGNORECASE)
                if match:
                    location = match.group(1).strip()
                    if location and len(location) < 200:
                        return location
            
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting location: {e}")
            return None

    def _extract_description(self, text: str) -> Optional[str]:
        """
        Extract description or additional details from text.
        
        Args:
            text: Cleaned text
            
        Returns:
            Description or None
        """
        try:
            # For now, return the full text as description
            # In future, could extract specific sections
            if len(text) > 500:
                return text[:500]  # Limit to 500 chars
            return text if text else None
            
        except Exception as e:
            logger.warning(f"Error extracting description: {e}")
            return None

    def _extract_priority(self, text: str) -> EventPriority:
        """
        Extract priority from text.
        
        Looks for keywords:
        - High: urgent, 紧急, ASAP, important, 重要
        - Low: optional, 可选, when available
        - Medium: default
        
        Args:
            text: Cleaned text
            
        Returns:
            EventPriority enum value
        """
        try:
            import re as regex_module
            
            text_lower = text.lower()
            
            # High priority keywords
            high_keywords = [
                'urgent', 'asap', 'important', 'emergency',
                '紧急', '重要', '立即', '紧'
            ]
            for keyword in high_keywords:
                if keyword in text_lower:
                    return EventPriority.HIGH
            
            # Low priority keywords
            low_keywords = [
                'optional', 'whenever', 'when available', 'flexible',
                '可选', '随意', '灵活'
            ]
            for keyword in low_keywords:
                if keyword in text_lower:
                    return EventPriority.LOW
            
            # Default to medium
            return EventPriority.MEDIUM
            
        except Exception as e:
            logger.warning(f"Error extracting priority: {e}")
            return EventPriority.MEDIUM
        
_parser_service_instance: Optional[ParserService] = None


def get_parser_service() -> ParserService:
    global _parser_service_instance
    if _parser_service_instance is None:
        _parser_service_instance = ParserService()
    return _parser_service_instance
