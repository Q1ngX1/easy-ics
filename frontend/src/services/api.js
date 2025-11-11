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

export const uploadTime = async (timezone, time) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/upload/base_time`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        timezone: "Asia/Shanghai",
        datetime,
      }),
    });

    if (!response.ok) {
      throw new Error(
        `Upload time failed: ${response.status} ${response.statusText}`
      );
    }
  } catch (error) {
    console.error("Unable to upload time");
  }
  throw error;
};

/**
 * Upload image and extract text via OCR
 * Args:
 *   file: File object from input
 *   lang: Optional OCR language (default: 'chi_sim+eng')
 * Returns: { success, text, filename, length, message }
 */
export const uploadImage = async (file, lang = "chi_sim+eng") => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
      `${API_BASE_URL}/api/upload/img?lang=${encodeURIComponent(lang)}`,
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
    console.error("Upload image error:", error);
    throw error;
  }
};

/**
 * Upload multiple images and extract text via OCR (batch)
 * Args:
 *   files: Array of File objects
 *   lang: Optional OCR language (default: 'chi_sim+eng')
 * Returns: {
 *   success,
 *   results: [{ filename, success, text, length, message }],
 *   total,
 *   successful,
 *   failed,
 *   combined_text,
 *   combined_length
 * }
 */
export const uploadImages = async (files, lang = "chi_sim+eng") => {
  try {
    if (!files || files.length === 0) {
      throw new Error("No files provided");
    }

    const formData = new FormData();
    for (const file of files) {
      formData.append("files", file);
    }

    const response = await fetch(
      `${API_BASE_URL}/api/upload/imgs?lang=${encodeURIComponent(lang)}`,
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `Batch upload failed: ${response.status}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Upload images error:", error);
    throw error;
  }
};

/**
 * Upload text and parse events
 * Args:
 *   text: Plain text content to parse
 *   timezone: Optional timezone (default: null, use server default)
 *   lang: Optional OCR language (default: 'chi_sim+eng')
 * Returns: { success, events, count, message }
 */
export const uploadText = async (
  text,
  timezone = null,
  lang = "chi_sim+eng"
) => {
  try {
    let url = `${API_BASE_URL}/api/upload/text?text=${encodeURIComponent(
      text
    )}&lang=${encodeURIComponent(lang)}`;

    if (timezone) {
      url += `&timezone=${encodeURIComponent(timezone)}`;
    }

    const response = await fetch(url, {
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
 *   events: Array of event objects with: title, start_time, end_time, location, description
 * Returns: Blob (ICS file)
 */
export const downloadICS = async (events) => {
  try {
    if (!events || events.length === 0) {
      throw new Error("Events list cannot be empty");
    }

    const response = await fetch(`${API_BASE_URL}/api/download_ics`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "text/calendar",
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
