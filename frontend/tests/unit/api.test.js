/**
 * API Service Unit Tests
 * Test all API communication functions
 */

import { describe, it, expect, beforeEach, vi } from "vitest";
import {
  checkHealth,
  uploadImage,
  uploadText,
  downloadICS,
  triggerDownload,
} from "../../src/services/api";

describe("API Service", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    global.fetch.mockClear();
  });

  describe("checkHealth", () => {
    it("should return health status successfully", async () => {
      const mockResponse = {
        status: "healthy",
        tesseract_available: true,
        message: "All service normal",
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await checkHealth();
      expect(result).toEqual(mockResponse);
      expect(result.status).toBe("healthy");
    });

    it("should throw error when health check fails", async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 503,
        statusText: "Service Unavailable",
      });

      await expect(checkHealth()).rejects.toThrow();
    });
  });

  describe("uploadImage", () => {
    it("should upload image and return OCR result", async () => {
      const mockFile = new File(["test"], "test.png", { type: "image/png" });
      const mockResponse = {
        success: true,
        text: "Recognized text from image",
        filename: "test.png",
        length: 23,
        message: "OCR success",
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await uploadImage(mockFile);
      expect(result).toEqual(mockResponse);
      expect(result.success).toBe(true);
      expect(result.text).toBeTruthy();
    });

    it("should handle image upload error", async () => {
      const mockFile = new File(["test"], "test.png", { type: "image/png" });
      const mockError = {
        detail: "Unsupported file type",
      };

      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => mockError,
      });

      await expect(uploadImage(mockFile)).rejects.toThrow(
        "Unsupported file type"
      );
    });

    it("should pass lang parameter correctly", async () => {
      const mockFile = new File(["test"], "test.png", { type: "image/png" });
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, text: "" }),
      });

      await uploadImage(mockFile, "eng");

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("lang=eng"),
        expect.any(Object)
      );
    });
  });

  describe("uploadText", () => {
    it("should parse text and return events", async () => {
      const mockResponse = {
        success: true,
        events: [
          {
            title: "Meeting",
            start_time: "2025-11-07T14:00:00",
            end_time: "2025-11-07T15:00:00",
            location: "Conference Room",
            description: "Team sync",
          },
        ],
        count: 1,
        timezone: "Asia/Shanghai",
        message: "Text parsing success",
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await uploadText("Tomorrow at 2pm meeting");
      expect(result).toEqual(mockResponse);
      expect(result.events).toHaveLength(1);
      expect(result.events[0].title).toBe("Meeting");
    });

    it("should include timezone parameter when provided", async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, events: [] }),
      });

      await uploadText("Test text", "Asia/Shanghai");

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("timezone=Asia%2FShanghai"),
        expect.any(Object)
      );
    });

    it("should handle empty text error", async () => {
      const mockError = {
        detail: "Content cannot be empty",
      };

      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => mockError,
      });

      await expect(uploadText("")).rejects.toThrow("Content cannot be empty");
    });

    it("should handle parsing failure", async () => {
      const mockError = {
        detail: "Text parsing failed",
      };

      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => mockError,
      });

      await expect(uploadText("Some text")).rejects.toThrow(
        "Text parsing failed"
      );
    });
  });

  describe("downloadICS", () => {
    it("should download ICS file successfully", async () => {
      const mockEvents = [
        {
          title: "Meeting",
          start_time: "2025-11-07T14:00:00",
          end_time: "2025-11-07T15:00:00",
          location: "Room A",
          description: "",
        },
      ];

      const mockBlob = new Blob(["ICS content"], { type: "text/calendar" });

      global.fetch.mockResolvedValueOnce({
        ok: true,
        blob: async () => mockBlob,
      });

      const result = await downloadICS(mockEvents);
      expect(result).toBeInstanceOf(Blob);
    });

    it("should throw error when events list is empty", async () => {
      await expect(downloadICS([])).rejects.toThrow(
        "Events list cannot be empty"
      );
    });

    it("should throw error when events is null", async () => {
      await expect(downloadICS(null)).rejects.toThrow(
        "Events list cannot be empty"
      );
    });

    it("should handle download error", async () => {
      const mockEvents = [
        {
          title: "Meeting",
          start_time: "2025-11-07T14:00:00",
          end_time: "2025-11-07T15:00:00",
          location: "Room A",
          description: "",
        },
      ];

      const mockError = {
        detail: "ICS generation failed",
      };

      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => mockError,
      });

      await expect(downloadICS(mockEvents)).rejects.toThrow(
        "ICS generation failed"
      );
    });
  });

  describe("triggerDownload", () => {
    it("should trigger file download in browser", () => {
      const mockBlob = new Blob(["test content"], { type: "text/calendar" });

      // Mock DOM methods
      const createElementSpy = vi.spyOn(document, "createElement");
      const appendChildSpy = vi.spyOn(document.body, "appendChild");
      const removeChildSpy = vi.spyOn(document.body, "removeChild");

      triggerDownload(mockBlob, "calendar.ics");

      expect(createElementSpy).toHaveBeenCalledWith("a");
      expect(appendChildSpy).toHaveBeenCalled();
      expect(removeChildSpy).toHaveBeenCalled();

      createElementSpy.mockRestore();
      appendChildSpy.mockRestore();
      removeChildSpy.mockRestore();
    });

    it("should use default filename when not provided", () => {
      const mockBlob = new Blob(["test"], { type: "text/calendar" });
      const createElementSpy = vi.spyOn(document, "createElement");

      triggerDownload(mockBlob);

      // Check that the link element was created (which is used for download)
      expect(createElementSpy).toHaveBeenCalledWith("a");

      createElementSpy.mockRestore();
    });
  });
});
