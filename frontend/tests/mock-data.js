/**
 * Mock Data for Frontend Tests
 * Contains realistic test fixtures for backend responses
 */

/**
 * Sample single event from backend
 */
export const MOCK_SINGLE_EVENT = {
  title: "Team Weekly Standup",
  start_time: "2025-11-07T09:30:00",
  end_time: "2025-11-07T10:00:00",
  location: "Conference Room A",
  description: "Weekly team synchronization meeting",
};

/**
 * Sample multiple events from backend
 */
export const MOCK_MULTIPLE_EVENTS = [
  {
    title: "Morning Standup",
    start_time: "2025-11-07T09:00:00",
    end_time: "2025-11-07T09:30:00",
    location: "Slack",
    description: "Daily team standup via Slack",
  },
  {
    title: "Project Planning Meeting",
    start_time: "2025-11-07T10:00:00",
    end_time: "2025-11-07T11:30:00",
    location: "Conference Room B",
    description: "Q4 project planning and resource allocation",
  },
  {
    title: "Lunch Break",
    start_time: "2025-11-07T12:00:00",
    end_time: "2025-11-07T13:00:00",
    location: "Cafeteria",
    description: "",
  },
  {
    title: "Client Call",
    start_time: "2025-11-07T14:00:00",
    end_time: "2025-11-07T15:00:00",
    location: "Virtual - Zoom",
    description: "Monthly status update with client",
  },
  {
    title: "Code Review",
    start_time: "2025-11-07T15:30:00",
    end_time: "2025-11-07T16:30:00",
    location: "GitHub PR Review",
    description: "Review pull requests for feature branch",
  },
];

/**
 * Sample successful upload text response
 */
export const MOCK_UPLOAD_TEXT_SUCCESS_RESPONSE = {
  success: true,
  events: [MOCK_SINGLE_EVENT],
  count: 1,
  timezone: "UTC",
  message: "Text parsing success",
};

/**
 * Sample successful multiple events response
 */
export const MOCK_UPLOAD_TEXT_MULTIPLE_SUCCESS_RESPONSE = {
  success: true,
  events: MOCK_MULTIPLE_EVENTS,
  count: 5,
  timezone: "America/New_York",
  message: "Text parsing success",
};

/**
 * Sample response with Asia/Shanghai timezone
 */
export const MOCK_UPLOAD_TEXT_SHANGHAI_TIMEZONE_RESPONSE = {
  success: true,
  events: [
    {
      title: "下午会议",
      start_time: "2025-11-07T14:00:00",
      end_time: "2025-11-07T15:00:00",
      location: "会议室A",
      description: "",
    },
  ],
  count: 1,
  timezone: "Asia/Shanghai",
  message: "Text parsing success",
};

/**
 * Sample response with no events found
 */
export const MOCK_UPLOAD_TEXT_EMPTY_RESPONSE = {
  success: true,
  events: [],
  count: 0,
  timezone: "UTC",
  message: "No events found in text",
};

/**
 * Sample error response for invalid content
 */
export const MOCK_UPLOAD_TEXT_ERROR_EMPTY_CONTENT = {
  detail: "Content cannot be empty",
};

/**
 * Sample error response for parsing failure
 */
export const MOCK_UPLOAD_TEXT_ERROR_PARSE_FAILED = {
  detail: "Text parsing failed",
};

/**
 * Sample error response for server error
 */
export const MOCK_UPLOAD_TEXT_ERROR_SERVER = {
  detail: "Internal server error",
};

/**
 * Sample image upload response
 */
export const MOCK_UPLOAD_IMAGE_SUCCESS_RESPONSE = {
  success: true,
  text: "Team meeting tomorrow at 2pm in Conference Room A.\nDuration: 1 hour.",
  filename: "schedule.png",
  length: 67,
  message: "OCR success",
};

/**
 * Sample image upload error response
 */
export const MOCK_UPLOAD_IMAGE_ERROR_UNSUPPORTED = {
  detail: "Unsupported file type",
};

/**
 * Sample health check response
 */
export const MOCK_HEALTH_CHECK_RESPONSE = {
  status: "healthy",
  tesseract_available: true,
  message: "All service normal",
};

/**
 * Sample health check response with Tesseract unavailable
 */
export const MOCK_HEALTH_CHECK_TESSERACT_UNAVAILABLE = {
  status: "healthy",
  tesseract_available: false,
  message: "Tesseract not available",
};

/**
 * Sample download ICS response data
 */
export const MOCK_ICS_BLOB_CONTENT = `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//easy-ics//easy-ics//EN
BEGIN:VEVENT
UID:1@example.com
DTSTART:20251107T093000Z
DTEND:20251107T100000Z
SUMMARY:Team Weekly Standup
LOCATION:Conference Room A
DESCRIPTION:Weekly team synchronization meeting
END:VEVENT
END:VCALENDAR`;

/**
 * Sample event with all optional fields empty
 */
export const MOCK_MINIMAL_EVENT = {
  title: "Event",
  start_time: "2025-11-07T10:00:00",
  end_time: "2025-11-07T11:00:00",
  location: "",
  description: "",
};

/**
 * Sample event with special characters
 */
export const MOCK_EVENT_WITH_SPECIAL_CHARS = {
  title: 'Meeting & Discussion: "Q4 Review" (Important!)',
  start_time: "2025-11-07T14:00:00",
  end_time: "2025-11-07T15:00:00",
  location: "Room A & B",
  description: "Review Q4 metrics & KPIs (70% target)",
};

/**
 * Sample event with very long title
 */
export const MOCK_EVENT_WITH_LONG_TITLE = {
  title:
    "This is a very long event title that contains multiple words and might wrap to several lines in the display component depending on the width of the container and the font size used",
  start_time: "2025-11-07T16:00:00",
  end_time: "2025-11-07T17:00:00",
  location: "Building A",
  description: "Description of the long titled event",
};

/**
 * Sample all-day event
 */
export const MOCK_ALL_DAY_EVENT = {
  title: "Company Holiday",
  start_time: "2025-11-07T00:00:00",
  end_time: "2025-11-07T23:59:59",
  location: "",
  description: "All day company holiday",
};

/**
 * Sample events spanning multiple days
 */
export const MOCK_MULTI_DAY_EVENT = {
  title: "Conference",
  start_time: "2025-11-07T09:00:00",
  end_time: "2025-11-09T17:00:00",
  location: "Convention Center",
  description: "3-day annual conference",
};

/**
 * Sample events with different timezones
 */
export const MOCK_EVENTS_DIFFERENT_TIMEZONES = [
  {
    title: "New York Meeting",
    start_time: "2025-11-07T14:00:00",
    end_time: "2025-11-07T15:00:00",
    location: "NYC Office",
    description: "",
  },
  {
    title: "Shanghai Meeting",
    start_time: "2025-11-08T02:00:00",
    end_time: "2025-11-08T03:00:00",
    location: "Shanghai Office",
    description: "",
  },
  {
    title: "London Meeting",
    start_time: "2025-11-07T19:00:00",
    end_time: "2025-11-07T20:00:00",
    location: "London Office",
    description: "",
  },
];

/**
 * Helper function to create a mock event with custom properties
 * @param {Object} overrides - Properties to override the defaults
 * @returns {Object} Mock event object
 */
export function createMockEvent(overrides = {}) {
  return {
    title: "Event Title",
    start_time: "2025-11-07T10:00:00",
    end_time: "2025-11-07T11:00:00",
    location: "",
    description: "",
    ...overrides,
  };
}

/**
 * Helper function to create a mock upload text response
 * @param {Array} events - Array of events to include in response
 * @param {Object} options - Additional options (timezone, message, etc.)
 * @returns {Object} Mock response object
 */
export function createMockUploadTextResponse(
  events = [MOCK_SINGLE_EVENT],
  options = {}
) {
  return {
    success: true,
    events,
    count: events.length,
    timezone: options.timezone || "UTC",
    message: options.message || "Text parsing success",
    ...options,
  };
}

/**
 * Helper function to create a mock error response
 * @param {String} detail - Error message detail
 * @returns {Object} Mock error response object
 */
export function createMockErrorResponse(detail = "An error occurred") {
  return {
    detail,
  };
}

/**
 * Sample realistic user input for text parsing
 */
export const MOCK_USER_INPUTS = [
  "Team meeting tomorrow at 2pm",
  "Lunch at 12:30pm in the cafeteria",
  "Conference from November 7 to 9 at Convention Center",
  "Call with John at 3:00 PM (1 hour)",
  "Monday 9am standup in Conference Room A",
  "Birthday party Friday 8pm at home",
  "Doctor appointment next Wednesday 10:30am",
  "Project deadline: Friday 5pm",
  "All day event: Company holiday on November 11",
  "Meeting every Monday at 10am",
];

/**
 * Sample real-world OCR text (extracted from image)
 */
export const MOCK_OCR_TEXT_SAMPLES = [
  `NOVEMBER 7, 2025 SCHEDULE

09:00 AM - Team Standup
Conference Room A

10:30 AM - Client Meeting
Virtual - Zoom Link: xyz

12:00 PM - Lunch Break
Cafeteria

02:00 PM - Project Review
Conference Room B`,

  `TO-DO List
[ ] Team meeting 2pm - Room A
[ ] Review code - PR #42
[ ] Send report 3:30pm
[ ] Dentist appointment Friday 10am`,

  `Conference Schedule
Day 1: Nov 7, 9am-5pm - Grand Hotel
Day 2: Nov 8, 9am-5pm - Grand Hotel
Day 3: Nov 9, 9am-3pm - Grand Hotel
Lunch: 12-1pm daily`,
];
