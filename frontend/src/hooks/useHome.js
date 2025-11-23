import { useEffect } from "react";
import { useImageUpload } from "./useImageUpload";
import { useClipboard } from "./useClipboard";
import { useLocationSettings } from "./useLocationSettings";
import { useProcessing } from "./useProcessing";

/**
 * Composite hook that combines all sub-hooks for OCR page
 * This is a lightweight composition layer that delegates to specialized hooks
 *
 * Architecture Benefits:
 * - Each hook has single responsibility (SRP)
 * - Hooks are independently testable and reusable
 * - Easier to maintain and extend
 * - Clean separation of concerns
 * - Can be used in different combinations by other components
 */
export function useHome() {
  const imageUpload = useImageUpload();
  const clipboard = useClipboard();
  const locationSettings = useLocationSettings();
  const processing = useProcessing();

  // Handle clipboard paste events
  useEffect(() => {
    const handleClipboardPaste = async (e) => {
      const files = e.detail?.files || [];
      if (files.length > 0) {
        imageUpload.handleImageChange(files);
      }
    };

    window.addEventListener("clipboardPaste", handleClipboardPaste);
    return () =>
      window.removeEventListener("clipboardPaste", handleClipboardPaste);
  }, []);

  // Unified clear handler
  const handleClear = () => {
    imageUpload.clearImages();
    processing.clear();
  };

  // Unified start handler with location/timezone integration
  const handleStart = async (e) => {
    if (e && e.preventDefault) {
      e.preventDefault();
    }

    await processing.handleStart(
      imageUpload.images,
      null, // text is managed separately in OCRPanel
      locationSettings.timezoneInfo,
      // Location request callback
      locationSettings.useLocation && !locationSettings.locationInfo
        ? async () => {
            try {
              const location = await locationSettings.getUserLocation();
              locationSettings.setLocationInfo(location);
            } catch (err) {
              console.warn("Location permission denied:", err);
              locationSettings.handleLocationChange(false);
            }
          }
        : null,
      // Timezone request callback
      locationSettings.useTimezone && !locationSettings.timezoneInfo
        ? () => {
            locationSettings.setTimezoneInfo(locationSettings.getTimezone());
          }
        : null
    );
  };

  return {
    // Image upload state & handlers
    images: imageUpload.images,
    dragActive: imageUpload.dragActive,
    hasImages: imageUpload.hasImages,
    handleImageChange: imageUpload.handleImageChange,
    removeImage: imageUpload.removeImage,
    clearImages: imageUpload.clearImages,
    handleDrag: imageUpload.handleDrag,
    handleDrop: imageUpload.handleDrop,

    // Clipboard state & handlers
    contextMenu: clipboard.contextMenu,
    handleContextMenu: (e) => clipboard.handleContextMenu(e, false),
    pasteFromClipboard: clipboard.pasteFromClipboard,

    // Location & timezone state & handlers
    useLocation: locationSettings.useLocation,
    locationInfo: locationSettings.locationInfo,
    useTimezone: locationSettings.useTimezone,
    timezoneInfo: locationSettings.timezoneInfo,
    handleLocationChange: locationSettings.handleLocationChange,
    handleTimezoneChange: locationSettings.handleTimezoneChange,

    // Processing state & handlers
    loading: processing.loading,
    result: processing.result,
    error: processing.error,
    handleStart,
    handleDownloadICS: processing.handleDownloadICS,
    handleClear,

    // Text management (for OCRPanel)
    // These are delegated to OCRPanel's own state
    setError: processing.setError,
    setResult: processing.setResult,
  };
}
