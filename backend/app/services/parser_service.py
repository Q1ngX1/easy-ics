"""Main parser service that orchestrates specialized parsers."""

from typing import List, Optional
import re
import logging
from datetime import datetime, timedelta
from app.models.event import Event
from app.services.parser import (
    DateTimeParser,
    EventParser,
    LocationParser,
    PriorityParser,
)

logger = logging.getLogger(__name__)



class ParserService:
    """
    Main parser service that orchestrates specialized parsers.
    
    Architecture:
    - DateTimeParser: Handles date/time extraction
    - EventParser: Handles event title and description extraction
    - LocationParser: Handles location extraction
    - PriorityParser: Handles priority extraction
    
    This design allows each parser to focus on a single responsibility,
    making the code more maintainable, testable, and extensible.

    util function: trim_text
    """
    
    def __init__(self):
        self.date_time_parser = DateTimeParser()
        self.event_parser = EventParser()
        self.location_parser = LocationParser()
        self.priority_parser = PriorityParser()

    
    # ============================================================================
    # Text Preprocessing Functions
    # ============================================================================

    @staticmethod
    def trim_text(text: str) -> str:
        """
        Clean and normalize input text for parsing.
        - Removes leading/trailing whitespace
        - Collapses multiple spaces/newlines into single spaces
        - Removes common OCR artifacts and special characters
        - Normalizes punctuation (Chinese to ASCII equivalents)
        """
        if not text:
            return ""

        # Remove leading/trailing whitespace
        text = text.strip()

        # Normalize different types of whitespace and newlines
        text = re.sub(r" +", " ", text)
        text = re.sub(r"[\n\r\t]+", " ", text)

        # Remove common OCR artifacts and isolated symbols
        text = re.sub(r"(?<!\w)[|¦ॉ][|\s]", " ", text)

        # Normalize Chinese punctuation to ASCII equivalents
        replacements = {
            "：": ":",
            "，": ",",
            "；": ";",
            "。": ".",
            "（": "(",
            "）": ")",
            """: '"',
            """: '"',
            "'": "'",
            "'": "'",
        }

        for cn_char, ascii_char in replacements.items():
            text = text.replace(cn_char, ascii_char)

        # Remove multiple consecutive punctuation marks
        text = re.sub(r"[.,;:!?]{2,}", lambda m: m.group(0)[0], text)

        # Final whitespace cleanup
        text = text.strip()

        return text

    def parse(self, text: str, timezone: Optional[str] = None) -> List[Event]:
        """
        Parse text content and extract event information.
        
        Processing pipeline:
        1. Text normalization (trim, clean)
        2. Separate individual events using EventParser.extract_event_number
        3. For each event:
           - Date/time extraction using DateTimeParser
           - Event title extraction using EventParser
           - Location extraction using LocationParser
           - Description extraction using EventParser
           - Priority extraction using PriorityParser
           - Create Event object
        
        Args:
            text: Plain text content to parse (may contain multiple events)
            timezone: Optional IANA timezone string (e.g., 'Asia/Shanghai')
            
        Returns:
            List of Event objects extracted from text
            
        Raises:
            ValueError: If text is empty or invalid
        """
        events = []
        
        try:
            if not text or text.strip() == "":
                raise ValueError("Text content cannot be empty")

            cleaned_text = self.trim_text(text)
            logger.debug(f"Cleaned text: {cleaned_text}")

            # Step 1: Extract individual event texts
            event_texts = self.event_parser.extract_event_number(cleaned_text)
            logger.debug(f"Found {len(event_texts)} event(s)")

            # Step 2: Process each event separately
            for event_text in event_texts:
                try:
                    if not event_text or event_text.strip() == "":
                        continue
                    
                    # Extract start and end date/time for this specific event
                    parsed_start_time, parsed_end_time = self.date_time_parser.extract_datetime_range(event_text, timezone)
                    
                    if not parsed_start_time:
                        logger.warning(f"No date found in event text: {event_text[:50]}..., using current date as fallback")
                        parsed_start_time = datetime.now()
                    
                    # If no end time specified, default to 1 hour after start
                    if not parsed_end_time:
                        parsed_end_time = parsed_start_time + timedelta(hours=1)

                    # Extract title from this event
                    title = self.event_parser.extract_title(event_text)
                    if not title:
                        title = "Untitled Event"

                    # Extract location from this event
                    location = self.location_parser.extract_location(event_text)

                    # Extract description from this event
                    description = self.event_parser.extract_description(event_text)

                    # Extract priority from this event
                    priority = self.priority_parser.extract_priority(event_text)
                    
                    # Create Event object
                    event = Event(
                        title=title,
                        start_time=parsed_start_time,
                        end_time=parsed_end_time,
                        location=location,
                        description=description,
                        priority=priority,
                        reminder_minutes=15  # Default: 15 minutes before
                    )
                    events.append(event)
                    logger.info(f"Successfully parsed event: {title}")
                    
                except Exception as e:
                    logger.error(f"Error parsing individual event: {e}", exc_info=True)
                    # Continue to next event instead of failing completely
                    continue
            
            if not events:
                logger.warning("No events were successfully parsed")
            
            logger.info(f"Successfully parsed {len(events)} event(s)")
            
        except ValueError as e:
            logger.error(f"Validation error in parser service: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in parser service: {e}", exc_info=True)
            raise
        
        return events


_parser_service_instance: Optional[ParserService] = None


def get_parser_service() -> ParserService:
    """Get or create the global ParserService instance."""
    global _parser_service_instance
    if _parser_service_instance is None:
        _parser_service_instance = ParserService()
    return _parser_service_instance
