import { useState } from "react";

/**
 * Hook for managing image upload and manipulation
 * Handles: file selection, drag-drop, removal, clearing
 */
export function useImageUpload() {
  const [images, setImages] = useState([]);
  const [dragActive, setDragActive] = useState(false);

  const hasImages = images.length > 0;

  /**
   * Handle image selection from file input
   */
  const handleImageChange = (newFiles) => {
    const filesToAdd = Array.isArray(newFiles) ? newFiles : [newFiles];
    const validImages = filesToAdd.filter((f) => f.type.startsWith("image/"));
    if (validImages.length > 0) {
      setImages([...images, ...validImages]);
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
   * Handle file drop on drag-drop area
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
      }
    }
  };

  return {
    images,
    dragActive,
    hasImages,
    handleImageChange,
    removeImage,
    clearImages,
    handleDrag,
    handleDrop,
    setImages,
  };
}
