import { useState } from "react";
import {
  uploadImages,
  uploadText,
  downloadICS,
  triggerDownload,
} from "../services/api";

/**
 * Hook for managing OCR and text processing workflow
 * Orchestrates: image OCR, text parsing, ICS download
 */
export function useProcessing() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  /**
   * Main processing function - handles image OCR and text parsing
   */
  const handleStart = async (
    images,
    text,
    timezoneInfo,
    onLocationRequest,
    onTimezoneRequest
  ) => {
    setError(null);
    setResult(null);
    setLoading(true);

    try {
      let events = [];

      // Get user location if needed
      if (onLocationRequest) {
        try {
          await onLocationRequest();
        } catch (err) {
          console.warn("Location permission denied:", err);
        }
      }

      // Get user timezone if needed
      if (onTimezoneRequest) {
        onTimezoneRequest();
      }

      // Upload images and extract text via OCR
      if (images && images.length > 0) {
        let allExtractedText = "";
        let failedFiles = [];

        try {
          const uploadRes = await uploadImages(images);
          if (!uploadRes.success) {
            throw new Error(uploadRes.message || "Upload failed");
          }

          // Handle response based on file count
          if (images.length === 1) {
            if (uploadRes.text && uploadRes.text.trim().length > 0) {
              allExtractedText = uploadRes.text;
            }
          } else {
            for (const result of uploadRes.results) {
              if (
                result.success &&
                result.text &&
                result.text.trim().length > 0
              ) {
                allExtractedText +=
                  (allExtractedText ? "\n" : "") + result.text;
              } else if (!result.success) {
                failedFiles.push(`${result.filename}: ${result.message}`);
              }
            }

            if (failedFiles.length > 0) {
              console.warn("Some files failed to process:", failedFiles);
            }
          }
        } catch (err) {
          throw new Error(`Upload failed: ${err.message}`);
        }

        // If text extracted, parse it to events
        if (allExtractedText.trim().length > 0) {
          const parseRes = await uploadText(
            allExtractedText,
            timezoneInfo?.timezone
          );
          if (!parseRes.success) {
            throw new Error(parseRes.message || "Text parsing failed");
          }
          events = parseRes.events || [];
        } else {
          const msg =
            failedFiles.length > 0
              ? `Failed to extract text from images. Failed files: ${failedFiles.join(
                  "; "
                )}`
              : "No text detected in the images. Please try clearer images.";
          setError(msg);
          setLoading(false);
          return;
        }
      }
      // Parse text directly
      else if (text && text.trim()) {
        const parseRes = await uploadText(text, timezoneInfo?.timezone);
        if (!parseRes.success) {
          throw new Error(parseRes.message || "Text parsing failed");
        }
        events = parseRes.events || [];
      } else {
        throw new Error("No input provided");
      }

      if (!events || events.length === 0) {
        setError(
          "No events were parsed from the input. Please try different content."
        );
        setLoading(false);
        return;
      }

      setResult(events);
    } catch (err) {
      console.error("Processing error:", err);
      setError(err.message || "An error occurred during processing");
    } finally {
      setLoading(false);
    }
  };

  /**
   * Download ICS file from parsed events
   */
  const handleDownloadICS = async () => {
    if (!result || result.length === 0) return;

    setLoading(true);
    setError(null);
    try {
      const icsBlob = await downloadICS(result);
      triggerDownload(icsBlob, "calendar.ics");
    } catch (err) {
      console.error("Download error:", err);
      setError(err.message || "Failed to download ICS file");
    } finally {
      setLoading(false);
    }
  };

  /**
   * Clear all results and errors
   */
  const clear = () => {
    setError(null);
    setResult(null);
  };

  return {
    loading,
    result,
    error,
    handleStart,
    handleDownloadICS,
    setResult,
    setError,
    clear,
  };
}
