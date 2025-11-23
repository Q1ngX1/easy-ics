/**
 * API Service - handles all backend communication
 * Base URL: http://localhost:8000 (update as needed for production)
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Health check endpoint
 * Returns: { status, tesseract_available, message }
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
 * Args:
 *   files: Single File object OR Array of File objects
 *   lang: Optional OCR language (default: 'chi_sim+eng')
 *
 * Returns:
 *   Single file: { success, text, filename, length, message }
 *   Multiple files: { success, results, total, successful, failed, combined_text, combined_length }
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
 * Upload text and parse events
 * Args:
 *   text: Plain text content to parse
 *   timezone: Optional timezone (default: null, use server default)
 *   lang: Optional OCR language (default: 'chi_sim+eng')
 * Returns: { success, events, count, timezone, message }
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
 * Download ICS file from events
 * Args:
 *   events: Array of event objects
 * Returns: Blob object for download
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

    return await response.blob();
  } catch (error) {
    console.error("Download ICS error:", error);
    throw error;
  }
};
