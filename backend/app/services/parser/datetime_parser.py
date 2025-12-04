"""Unified datetime parser combining date extraction and time parsing.

This module provides comprehensive date and time parsing capabilities:
- Text preprocessing and normalization
- Regex-based date/time extraction
- Multi-language support (English, Chinese)
- Integration with dateparser library
"""

from __future__ import annotations

import logging
import datetime
import re
from typing import Optional, Iterable

try:
    import dateparser
    DATEPARSER_AVAILABLE = True
except ImportError:
    DATEPARSER_AVAILABLE = False


logger = logging.getLogger(__name__)


# Constants for date parsing
MONTH_NAME_LOOKUP = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}

MONTH_NAME_PATTERN = (
    "Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
    "Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?"
)

# Precompile regex patterns for date formats
DATE_PATTERNS: Iterable[re.Pattern[str]] = (
    # ISO like: 2025-11-22 or 2025/11/22 14:30
    re.compile(
        r"(?P<year>\d{4})[-/](?P<month>\d{1,2})[-/](?P<day>\d{1,2})"
        r"(?:[ T](?P<hour>\d{1,2})(?::(?P<minute>\d{1,2}))?)?"
    ),
    # Day first: 22-11-2025 or 22/11/2025 14:30
    re.compile(
        r"(?P<day>\d{1,2})[-/](?P<month>\d{1,2})[-/](?P<year>\d{4})"
        r"(?:[ T](?P<hour>\d{1,2})(?::(?P<minute>\d{1,2}))?)?"
    ),
    # Month first (US style): 11/22/2025 14:30
    re.compile(
        r"(?P<month>\d{1,2})[-/](?P<day>\d{1,2})[-/](?P<year>\d{4})"
        r"(?:[ T](?P<hour>\d{1,2})(?::(?P<minute>\d{1,2}))?)?"
    ),
    # English month names: November 22 2025 or 22 November 2025 14:30
    re.compile(
        fr"(?P<month_name>{MONTH_NAME_PATTERN})\s+(?P<day>\d{{1,2}})(?:st|nd|rd|th)?"
        fr"(?:,?\s+(?P<year>\d{{4}}))?(?:\s+(?P<hour>\d{{1,2}})(?::(?P<minute>\d{{1,2}}))?)?",
        re.IGNORECASE,
    ),
    re.compile(
        fr"(?P<day>\d{{1,2}})(?:st|nd|rd|th)?\s+(?P<month_name>{MONTH_NAME_PATTERN})"
        fr"(?:,?\s+(?P<year>\d{{4}}))?(?:\s+(?P<hour>\d{{1,2}})(?::(?P<minute>\d{{1,2}}))?)?",
        re.IGNORECASE,
    ),
    # Chinese full date: 2025年11月22日 14:30
    re.compile(
        r"(?P<year>\d{2,4})年(?P<month>\d{1,2})月(?P<day>\d{1,2})日?"
        r"(?:\s*(?P<hour>\d{1,2})(?:[:：](?P<minute>\d{1,2}))?)?"
    ),
    # Chinese month/day without explicit year: 11月22日 14:30
    re.compile(
        r"(?P<month>\d{1,2})月(?P<day>\d{1,2})日?"
        r"(?:\s*(?P<hour>\d{1,2})(?:[:：](?P<minute>\d{1,2}))?)?"
    ),
)


# ============================================================================
# Helper Functions for Date Parsing
# ============================================================================

def _build_datetime_from_match(
    match: re.Match[str],
    default_year: Optional[int] = None,
) -> Optional[datetime.datetime]:
    """
    Convert a regex match with day/time groups into a datetime instance.
    
    Args:
        match: Regex match object with named groups
        default_year: Year to use if not found in match
        
    Returns:
        datetime object if valid, None otherwise
    """
    groups = match.groupdict()
    try:
        year_str = groups.get("year")
        year = int(year_str) if year_str else (default_year or datetime.date.today().year)
        
        month: Optional[int] = None
        if groups.get("month"):
            month = int(groups["month"])
        elif groups.get("month_name"):
            month = MONTH_NAME_LOOKUP.get(groups["month_name"].lower())
        
        if month is None:
            return None
        
        day = int(groups["day"])
        hour = int(groups.get("hour") or 0)
        minute = int(groups.get("minute") or 0)
        
        return datetime.datetime(year, month, day, hour, minute)
    except (ValueError, KeyError) as e:
        logger.debug(f"Error building datetime from match: {e}")
        return None


# ============================================================================
# Core Parsing Functions
# ============================================================================

def parse_simple_date(text: str) -> Optional[datetime.datetime]:
    """
    Parse the first simple date found in text using regex patterns.

    Supports common numeric formats such as:
    - YYYY-MM-DD, YYYY/MM/DD
    - DD/MM/YYYY, DD-MM-YYYY
    - MM/DD/YYYY (US style)
    - English month names (November 22, 22 November, etc.)
    - Chinese dates (2025年11月22日, 11月22日)
    
    Optional HH:MM or HH:MM:SS time suffix is also supported.
    
    Args:
        text: Text to parse for date patterns
        
    Returns:
        datetime object if found, None otherwise
    """
    if not text:
        return None

    current_year = datetime.date.today().year
    for pattern in DATE_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue
        parsed = _build_datetime_from_match(match, default_year=current_year)
        if parsed:
            return parsed
    return None


def parse_date_with_dateparser(
    text: str,
    languages: Optional[list[str]] = None,
    default_year: Optional[int] = None,
) -> Optional[datetime.datetime]:
    """
    Parse date using the dateparser library with multi-language support.

    This is a more robust parser that supports a wider variety of date formats
    and localization. It falls back to regex parsing if dateparser is unavailable
    or fails to parse the date.

    Args:
        text: The text to parse.
        languages: List of language codes (e.g., ["en", "zh"]) to help with parsing.
            Defaults to ["en", "zh"] if not provided.
        default_year: Year to use when parsing dates without an explicit year.

    Returns:
        A datetime object if a date is found, otherwise None.
    """
    if not text:
        return None

    if not DATEPARSER_AVAILABLE:
        return parse_simple_date(text)

    if languages is None:
        languages = ["en", "zh"]

    settings = {
        "LANGUAGES": languages,
        "RETURN_AS_TIMEZONE_AWARE": False,
    }

    if default_year:
        settings["PREFER_DATES_FROM"] = (
            "future" if default_year >= datetime.date.today().year else "past"
        )

    try:
        parsed = dateparser.parse(text, settings=settings)
        if parsed:
            return parsed
    except Exception as e:
        logger.debug(f"Error parsing date with dateparser: {e}")

    # Fallback to regex parsing
    return parse_simple_date(text)


# ============================================================================
# DateTimeParser Class
# ============================================================================

class DateTimeParser:
    """
    Parser for extracting date and time information from text.
    
    This parser combines the dateparser library and regex-based parsing
    for robust date/time extraction with multi-language support.
    
    Example:
        >>> parser = DateTimeParser()
        >>> dt = parser.extract_datetime("Meeting on 2025-11-24 at 14:30")
        >>> print(dt)
        2025-11-24 14:30:00
    """
    
    @staticmethod
    def extract_datetime(text: str, timezone: Optional[str] = None) -> Optional[datetime.datetime]:
        """
        Extract date and time from text using multiple strategies.
        
        Tries parsing in order:
        1. dateparser with multi-language support (more flexible)
        2. Simple regex patterns for common formats (faster fallback)
        
        Args:
            text: Cleaned text to parse
            timezone: Optional timezone string (e.g., 'Asia/Shanghai')
                Currently not used but reserved for future enhancement
            
        Returns:
            datetime object if found, None otherwise
        """
        try:
            if not text:
                return None
            
            # Try dateparser first (more robust for natural language)
            dt = parse_date_with_dateparser(text, languages=["en", "zh"])
            if dt:
                return dt
            
            # Fallback to simple regex parsing
            dt = parse_simple_date(text)
            return dt
            
        except Exception as e:
            logger.warning(f"Error extracting datetime: {e}")
            return None

    @staticmethod
    def extract_datetime_range(text: str, timezone: Optional[str] = None) -> tuple[Optional[datetime.datetime], Optional[datetime.datetime]]:
        """
        Extract start and end datetime from text for a single event.
        
        Looks for patterns like:
        - "2025-11-24 14:30" -> start time, end time = None (will be handled by caller)
        - "2025-11-24 14:30-15:30" -> (start, end)
        - "2025-11-24-2025-11-25" -> (start on day 1, end on day 2)
        - "2025/11/24 - 2025/11/25, 14:30" -> (start, end with time)
        
        Args:
            text: Cleaned text to parse (single event)
            timezone: Optional timezone string (e.g., 'Asia/Shanghai')
            
        Returns:
            Tuple of (start_datetime, end_datetime). 
            end_datetime can be None if only one time is specified.
        """
        try:
            if not text:
                return None, None
            
            start_time = None
            end_time = None
            
            # Pattern 1: Look for date range separator patterns
            # Examples: "2025-11-24-2025-11-25" or "2025/11/24 - 2025/11/25"
            range_pattern = r"(\d{4}[-/]\d{1,2}[-/]\d{1,2})\s*(?:-|~|to)\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2})"
            range_match = re.search(range_pattern, text)
            
            if range_match:
                # Found date range
                start_date_str = range_match.group(1)
                end_date_str = range_match.group(2)
                
                # Parse both dates
                start_time = parse_simple_date(start_date_str)
                end_time = parse_simple_date(end_date_str)
                
                # If we have start time, look for times attached to the range
                if start_time:
                    # Look for time after the date range (e.g., "2025-11-24-2025-11-25 14:30")
                    time_pattern = r"(?:[-~]|到|至)\s*\d{1,2}:\d{1,2}"
                    time_match = re.search(r"(\d{1,2}):(\d{1,2})", text[range_match.end():range_match.end()+20])
                    if time_match:
                        hour = int(time_match.group(1))
                        minute = int(time_match.group(2))
                        start_time = start_time.replace(hour=hour, minute=minute)
                
                if end_time and start_time:
                    # If end_time is just a date, add the same time as start or keep as start of day
                    if end_time.hour == 0 and end_time.minute == 0:
                        # End time is start of day, set to end of day
                        end_time = end_time.replace(hour=23, minute=59)
                    
                    return start_time, end_time
            
            # Pattern 2: Look for time range in single date (e.g., "14:30-15:30" on same date)
            # First, find the date
            start_time = parse_date_with_dateparser(text, languages=["en", "zh"])
            if not start_time:
                start_time = parse_simple_date(text)
            
            if start_time:
                # Look for end time after the start time (e.g., "14:30-15:30" or "14:30~15:30")
                time_range_pattern = r"(\d{1,2}):(\d{1,2})\s*(?:-|~|到|至)\s*(\d{1,2}):(\d{1,2})"
                time_range_match = re.search(time_range_pattern, text)
                
                if time_range_match:
                    # Extract both times
                    start_hour = int(time_range_match.group(1))
                    start_min = int(time_range_match.group(2))
                    end_hour = int(time_range_match.group(3))
                    end_min = int(time_range_match.group(4))
                    
                    # Apply to the found date
                    start_time = start_time.replace(hour=start_hour, minute=start_min)
                    end_time = start_time.replace(hour=end_hour, minute=end_min)
                    
                    # Handle case where end time is on next day (e.g., 23:00-01:00)
                    if end_time < start_time:
                        end_time += datetime.timedelta(days=1)
                    
                    return start_time, end_time
            
            # Default: return just start time
            return start_time, None
            
        except Exception as e:
            logger.warning(f"Error extracting datetime range: {e}")
            return None, None
