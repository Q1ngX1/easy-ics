import { useState, useEffect } from "react";
import {
  uploadImage,
  uploadImages,
  uploadText,
  downloadICS,
  triggerDownload,
} from "../services/api";

/**
 * Custom hook to manage Home page logic
 * Handles image upload, text input, API calls, and state management
 */
export function useHome() {
  const [images, setImages] = useState([]);
  const [text, setText] = useState("");
  const [dragActive, setDragActive] = useState(false);
  const [contextMenu, setContextMenu] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [useLocation, setUseLocation] = useState(false);
  const [useTimezone, setUseTimezone] = useState(false);
  const [locationInfo, setLocationInfo] = useState(null);
  const [timezoneInfo, setTimezoneInfo] = useState(null);

  const hasImages = images.length > 0;
  const hasText = text.trim().length > 0;
  const hasInput = hasImages || hasText;

  /**
   * Handle image selection from file input (supports multiple files)
   */
  const handleImageChange = (newFiles) => {
    // newFiles can be a single File or an array of Files
    const filesToAdd = Array.isArray(newFiles) ? newFiles : [newFiles];
    const validImages = filesToAdd.filter((f) => f.type.startsWith("image/"));

    if (validImages.length > 0) {
      setImages([...images, ...validImages]);
      setText("");
    }
  };

  /**
   * Remove a specific image from the list
   */
  const removeImage = (index) => {
    setImages(images.filter((_, i) => i !== index));
  };

  /**
   * Clear all images
   */
  const clearImages = () => {
    setImages([]);
  };

  /**
   * Handle drag enter/over events
   */
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  /**
   * Handle file drop on drag-drop area (supports multiple files)
   */
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      const imageFiles = Array.from(files).filter((f) =>
        f.type.startsWith("image/")
      );
      if (imageFiles.length > 0) {
        setImages([...images, ...imageFiles]);
        setText("");
      }
    }
  };

  /**
   * Clear all inputs and results
   */
  const handleClear = () => {
    setError(null);
    setImages([]);
    setText("");
    setResult(null);
  };

  /**
   * Get user's geolocation via browser API
   */
  const getUserLocation = () => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error("Geolocation not supported"));
        return;
      }
      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy,
          });
        },
        (error) => reject(error)
      );
    });
  };

  /**
   * Main processing function - handles image OCR and text parsing
   */
  const handleStart = async (e) => {
    if (e && e.preventDefault) {
      e.preventDefault();
    }
    setError(null);
    setResult(null);
    setLoading(true);

    try {
      let events = [];

      // Get user location if checked
      if (useLocation && !locationInfo) {
        try {
          const location = await getUserLocation();
          setLocationInfo(location);
        } catch (err) {
          console.warn("Location permission denied:", err);
          setUseLocation(false);
        }
      }

      // Get user timezone if checked
      if (useTimezone && !timezoneInfo) {
        const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        const datetime = new Date().toISOString();
        setTimezoneInfo({ timezone, datetime });
      }

      // Upload images and extract text via OCR
      if (images.length > 0) {
        let allExtractedText = "";
        let failedFiles = [];

        // Use batch upload for multiple images
        if (images.length > 1) {
          try {
            const uploadRes = await uploadImages(images);
            if (!uploadRes.success) {
              throw new Error(uploadRes.message || "Batch upload failed");
            }

            // Process results
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

            // Show warning if some files failed
            if (failedFiles.length > 0) {
              console.warn("Some files failed to process:", failedFiles);
              logger.warning(`Upload warning: ${failedFiles.join("; ")}`);
            }
          } catch (err) {
            throw new Error(`Batch upload failed: ${err.message}`);
          }
        } else {
          // Single image: use traditional upload
          const uploadRes = await uploadImage(images[0]);
          if (!uploadRes.success) {
            throw new Error(uploadRes.message || "Image upload failed");
          }
          if (uploadRes.text && uploadRes.text.trim().length > 0) {
            allExtractedText = uploadRes.text;
          }
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
      else if (text) {
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
   * Handle right-click context menu
   */
  const handleContextMenu = (e) => {
    if (text.trim().length > 0) return;
    e.preventDefault();
    setContextMenu({ x: e.clientX + 2, y: e.clientY + 2 });
  };

  /**
   * Paste images from clipboard
   */
  const pasteFromClipboard = async () => {
    setContextMenu(null);
    try {
      if (navigator.clipboard && navigator.clipboard.read) {
        const items = await navigator.clipboard.read();
        const pastedFiles = [];
        for (const item of items) {
          for (const type of item.types) {
            if (type.startsWith("image/")) {
              const blob = await item.getType(type);
              const file = new File(
                [blob],
                "pasted-image." + type.split("/")[1],
                {
                  type: blob.type,
                }
              );
              pastedFiles.push(file);
            }
          }
        }
        if (pastedFiles.length > 0) {
          setImages((prevImages) => [...prevImages, ...pastedFiles]);
          setText("");
        } else {
          alert("No image found in clipboard.");
        }
      } else {
        alert(
          "Paste from clipboard is not supported in this browser via right-click. Please focus the page and press Ctrl+V to paste the image."
        );
      }
    } catch (err) {
      console.error("clipboard.read error", err);
      alert(
        "Unable to read clipboard. Please try pressing Ctrl+V or check browser permissions."
      );
    }
  };

  /**
   * Setup paste listener for Ctrl+V
   */
  useEffect(() => {
    const onPaste = (e) => {
      try {
        const items = e.clipboardData?.items;
        if (!items) return;

        const pastedFiles = [];
        for (let i = 0; i < items.length; i++) {
          const item = items[i];
          if (item.type && item.type.startsWith("image/")) {
            const file = item.getAsFile();
            if (file) {
              pastedFiles.push(file);
            }
          }
        }
        if (pastedFiles.length > 0) {
          setImages((prevImages) => [...prevImages, ...pastedFiles]);
          setText("");
          e.preventDefault();
        }
      } catch (err) {
        console.error("paste handling error", err);
      }
    };

    window.addEventListener("paste", onPaste);
    return () => window.removeEventListener("paste", onPaste);
  }, []);

  /**
   * Hide context menu when clicking elsewhere
   */
  useEffect(() => {
    const onClick = () => setContextMenu(null);
    window.addEventListener("click", onClick);
    return () => window.removeEventListener("click", onClick);
  }, []);

  /**
   * Handle location checkbox change
   */
  const handleLocationChange = (checked) => {
    setUseLocation(checked);
    if (!checked) {
      setLocationInfo(null);
    }
  };

  /**
   * Handle timezone checkbox change
   */
  const handleTimezoneChange = (checked) => {
    setUseTimezone(checked);
    if (checked) {
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      setTimezoneInfo({ timezone, datetime: new Date().toISOString() });
    } else {
      setTimezoneInfo(null);
    }
  };

  return {
    // State
    images,
    text,
    dragActive,
    contextMenu,
    loading,
    result,
    error,
    useLocation,
    locationInfo,
    useTimezone,
    timezoneInfo,
    hasImages,
    hasText,
    hasInput,
    // Handlers
    handleImageChange,
    removeImage,
    clearImages,
    handleDrag,
    handleDrop,
    handleClear,
    handleStart,
    handleDownloadICS,
    handleContextMenu,
    pasteFromClipboard,
    handleLocationChange,
    handleTimezoneChange,
    // State setters
    setText,
    setError,
    setResult,
  };
}
