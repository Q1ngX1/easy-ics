"""Utility helpers for regex based date parsing."""

from __future__ import annotations

import datetime
import re
from typing import Iterable, Optional

try:
	import dateparser
	DATEPARSER_AVAILABLE = True
except ImportError:
	DATEPARSER_AVAILABLE = False



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


# Precompile a broader set of commonly seen date formats to keep parsing fast.
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

def trim_text(text: str) -> str:
	"""
	Clean and normalize input text for parsing:
	- Removes leading/trailing whitespace
	- Optionally collapses multiple spaces/newlines into single spaces
	- Removes common OCR artifacts and special characters
	- Normalizes punctuation

	"""

	if not text:
		return ""

	# Remove leading/trailing whitespace
	text = text.strip()

	# Normalize different types of whitespace and newlines

	text = re.sub(r" +", " ", text)
	text = re.sub(r"[\n\r\t]+", " ", text)

	# Remove common OCR artifacts and isolated symbols that likely are OCR errors
	text = re.sub(r"(?<!\w)[|¦ॉ][|\s]", " ", text)

	# Normalize Chinese punctuation to ASCII equivalents if needed
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


def _build_datetime_from_match(
	match: re.Match[str],
	default_year: Optional[int] = None,
) -> Optional[datetime.datetime]:
	"""Convert a regex match with day/time groups into a ``datetime`` instance."""

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
	except (ValueError, KeyError):
		return None


def parse_simple_date(text: str) -> Optional[datetime.datetime]:
	"""Parse the first simple date found inside *text*.

	The parser supports common numeric formats such as ``YYYY-MM-DD`` and
	``DD/MM/YYYY`` with an optional ``HH:MM`` time suffix. Returns ``None`` when
	no supported date can be detected.
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
	"""Parse date using the dateparser library with multi-language support.

	This is a more robust parser that supports a wider variety of date formats
	and localization. It falls back to regex parsing if dateparser is unavailable
	or fails to parse the date.

	Args:
		text: The text to parse.
		languages: List of language codes (e.g., ["en", "zh"]) to help with parsing.
			Defaults to ["en", "zh"] if not provided.
		default_year: Year to use when parsing dates without an explicit year.

	Returns:
		A ``datetime`` object if a date is found, otherwise ``None``.
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
		settings["PREFER_DATES_FROM"] = "future" if default_year >= datetime.date.today().year else "past"

	try:
		parsed = dateparser.parse(text, settings=settings)
		if parsed:
			return parsed
	except Exception:
		pass

	# Fallback to regex parsing
	return parse_simple_date(text)

