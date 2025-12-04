"""Priority parser for extracting event priority from text."""

import logging
from typing import Optional
from app.models.event import EventPriority

logger = logging.getLogger(__name__)


class PriorityParser:
    """Parser for extracting priority information from text."""
    
    @staticmethod
    def extract_priority(text: str) -> EventPriority:
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
