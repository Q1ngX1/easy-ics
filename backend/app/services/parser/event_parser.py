"""Event title and description parser."""

import re
import logging
from typing import Optional, List
from app.models.event import Event

logger = logging.getLogger(__name__)


class EventParser:
    """Parser for extracting event titles and descriptions from text."""


    @staticmethod
    def extract_event_number(text: str) -> List[str]:
        """
        Parse and separate individual events from text.
        
        Heuristics:
        1. Split by common event delimiters (line breaks with pattern, numbers)
        2. Each separated text block is treated as a single event
        3. Returns list of individual event texts
        
        Args:
            text: Raw input text that may contain multiple events
            
        Returns:
            List of individual event strings, each representing one event
        """
        try:
            if not text or not text.strip():
                return []
            
            # Attempt to split by common patterns:
            # 1. Lines starting with numbers (1., 2., etc.)
            # 2. Double newlines (blank line separator)
            # 3. If no clear separators, treat whole text as single event
            
            events = []
            
            # Pattern 1: Split by numbered items (1., 2., etc.)
            if re.search(r'\n\s*\d+\.', text):
                parts = re.split(r'\n\s*\d+\.', text)
                # Remove empty first part if exists
                parts = [p.strip() for p in parts if p.strip()]
                events.extend(parts)
            
            # Pattern 2: Split by double newlines (paragraph breaks)
            elif '\n\n' in text:
                parts = re.split(r'\n\n+', text)
                parts = [p.strip() for p in parts if p.strip()]
                events.extend(parts)
            
            # If no separators found, treat as single event
            if not events:
                events = [text.strip()]
            
            return events
            
        except Exception as e:
            logger.warning(f"Error extracting event numbers: {e}")
            # Fallback: return the whole text as single event
            return [text] if text else []
    
    @staticmethod
    def extract_title(text: str) -> Optional[str]:
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
                    title = re.sub(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}', '', first_line).strip()
                    if title:
                        return title
            
            # Try to extract text before first date pattern
            match = re.search(r'([^:。.!\n?]{5,100}?)[\s:：]*\d{4}[-/年]', text)
            if match:
                title = match.group(1).strip()
                if title:
                    return title
            
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting title: {e}")
            return None
    
    @staticmethod
    def extract_description(text: str) -> Optional[str]:
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
