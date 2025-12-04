"""Location parser for extracting locations from text."""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class LocationParser:
    """Parser for extracting location information from text."""
    
    @staticmethod
    def extract_location(text: str) -> Optional[str]:
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
            # Pattern 1: "地点: xxx" or "Location: xxx"
            patterns = [
                r'地点[:：]\s*([^\n,，。;；]*)',
                r'location[:：]\s*([^\n,，。;；]*)',
                r'地址[:：]\s*([^\n,，。;；]*)',
                r'会议地点[:：]\s*([^\n,，。;；]*)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    location = match.group(1).strip()
                    if location and len(location) < 200:
                        return location
            
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting location: {e}")
            return None
