/**
 * API Service - handles all backend communication
 * Base URL: http://localhost:8000 (update as needed for production)
 *
 * Endpoints:
 * - GET  /api/check_health - Health check
 * - POST /api/upload - OCR image upload (single or multiple)
 * - POST /api/upload/text - Parse text and extract events
 * - POST /api/download_ics - Generate and download ICS file
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Health check endpoint
 * Verifies backend service availability and Tesseract OCR status
 *
 * Returns:
 * {
 *   status: 'healthy' | 'unhealthy',
 *   tesseract_available: boolean,
 *   message: string
 * }
 *
 * @throws {Error} If health check fails
 */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/check_health`, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(
        `Health check failed: ${response.status} ${response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Health check error:", error);
    throw error;
  }
};

/**
 * Upload image(s) and extract text via OCR
 * Unified endpoint that automatically handles both single and multiple file uploads
 *
 * @param {File|File[]} files - Single File object OR Array of File objects
 * @param {string} [lang='chi_sim+eng'] - OCR language (supports multiple: 'chi_sim+eng', 'chi_tra', 'eng', etc.)
 *
 * @returns {Promise<Object>}
 * Single file response:
 * {
 *   success: boolean,
 *   text: string,
 *   filename: string,
 *   length: number,
 *   message: string
 * }
 *
 * Multiple files response:
 * {
 *   success: boolean,
 *   results: Array,           // Result for each file
 *   total: number,            // Total files uploaded
 *   successful: number,       // Successfully processed
 *   failed: number,           // Failed to process
 *   combined_text: string,    // All extracted text combined
 *   combined_length: number,  // Total characters
 *   message: string
 * }
 *
 * @throws {Error} If upload fails or files are invalid
 */
export const uploadImages = async (files, lang = "chi_sim+eng") => {
  try {
    if (!files) {
      throw new Error("No files provided");
    }

    const fileArray = Array.isArray(files) ? files : [files];

    if (fileArray.length === 0) {
      throw new Error("No files provided");
    }

    const formData = new FormData();

    // For single file, use 'file' field; for multiple, use 'files' field
    if (fileArray.length === 1) {
      formData.append("file", fileArray[0]);
    } else {
      for (const file of fileArray) {
        formData.append("files", file);
      }
    }

    // Use unified /api/upload endpoint
    const response = await fetch(
      `${API_BASE_URL}/api/upload?lang=${encodeURIComponent(lang)}`,
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Upload failed: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Upload error:", error);
    throw error;
  }
};

/**
 * Trigger ICS file download in browser
 * Args:
 *   icsBlob: Blob object from downloadICS
 *   filename: Optional filename (default: 'calendar.ics')
 */
/**
 * Trigger browser download for ICS file
 * Creates an object URL and programmatically triggers download
 *
 * @param {Blob} icsBlob - ICS file content as Blob
 * @param {string} [filename='calendar.ics'] - Downloaded filename
 *
 * @throws {Error} If download trigger fails
 */
export const triggerDownload = (icsBlob, filename = "calendar.ics") => {
  try {
    const url = URL.createObjectURL(icsBlob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Download trigger error:", error);
    throw error;
  }
};

/**
 * Parse text content and extract calendar events
 * Supports multi-language text parsing (English, Chinese, etc.)
 *
 * @param {string} text - Plain text content to parse (required)
 * @param {string} [timezone=null] - IANA timezone string (e.g., 'Asia/Shanghai', 'UTC')
 * @param {string} [lang='chi_sim+eng'] - OCR language setting (not used in text parsing, kept for compatibility)
 *
 * @returns {Promise<Object>}
 * {
 *   success: boolean,
 *   events: Array<{
 *     title: string,
 *     start_time: string (ISO format),
 *     end_time: string (ISO format),
 *     location: string | null,
 *     description: string | null,
 *     duration_hours: number,
 *     priority: 'low' | 'medium' | 'high'
 *   }>,
 *   count: number,            // Number of events extracted
 *   timezone: string,
 *   message: string
 * }
 *
 * @throws {Error} If text parsing fails or text is empty
 */
export const uploadText = async (
  text,
  timezone = null,
  lang = "chi_sim+eng"
) => {
  try {
    if (!text || text.trim().length === 0) {
      throw new Error("Text content cannot be empty");
    }

    const params = new URLSearchParams();
    params.append("text", text);
    if (timezone) {
      params.append("timezone", timezone);
    }

    const response = await fetch(`${API_BASE_URL}/api/upload/text?${params}`, {
      method: "POST",
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `Text parsing failed: ${response.status}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Upload text error:", error);
    throw error;
  }
};

/**
 * Generate and download ICS calendar file
 * Converts event objects to ICS format and triggers download
 *
 * @param {Array<Object>} events - Array of event objects with required fields:
 * {
 *   title: string,
 *   start_time: string (ISO 8601 format: 'YYYY-MM-DDTHH:mm:ss'),
 *   end_time: string (ISO 8601 format: 'YYYY-MM-DDTHH:mm:ss'),
 *   location?: string,
 *   description?: string
 * }
 *
 * @returns {Promise<Blob>} ICS file blob
 *
 * @example
 * const events = [{
 *   title: 'Team Meeting',
 *   start_time: '2025-11-22T14:00:00',
 *   end_time: '2025-11-22T15:00:00',
 *   location: 'Conference Room A',
 *   description: 'Weekly team sync'
 * }];
 * const blob = await downloadICS(events);
 *
 * @throws {Error} If no events provided or download fails
 */
export const downloadICS = async (events) => {
  try {
    if (!events || events.length === 0) {
      throw new Error("No events provided");
    }

    const response = await fetch(`${API_BASE_URL}/api/download_ics`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ events }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `Download failed: ${response.status}`
      );
    }

    const blob = await response.blob();

    // Trigger download
    triggerDownload(blob, "calendar.ics");

    return blob;
  } catch (error) {
    console.error("Download ICS error:", error);
    throw error;
  }
};
