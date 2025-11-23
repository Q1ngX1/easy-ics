import { useState, useEffect } from "react";

/**
 * Hook for managing clipboard operations
 * Handles: context menu, paste from clipboard, Ctrl+V listener
 */
export function useClipboard() {
  const [contextMenu, setContextMenu] = useState(null);

  /**
   * Handle right-click context menu
   */
  const handleContextMenu = (e, hasText) => {
    if (hasText) return;
    e.preventDefault();
    setContextMenu({ x: e.clientX + 2, y: e.clientY + 2 });
  };

  /**
   * Paste images from clipboard via right-click menu
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
          return pastedFiles;
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
    return [];
  };

  /**
   * Setup paste listener for Ctrl+V
   * Returns callback to handle pasted files
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
          e.preventDefault();
          // Return files via window event
          window.dispatchEvent(
            new CustomEvent("clipboardPaste", {
              detail: { files: pastedFiles },
            })
          );
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

  return {
    contextMenu,
    setContextMenu,
    handleContextMenu,
    pasteFromClipboard,
  };
}
