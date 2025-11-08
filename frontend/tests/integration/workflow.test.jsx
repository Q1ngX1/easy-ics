/**
 * Integration Tests
 * Test complete workflows from user input to event display
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Home from '../../src/pages/Home'
import * as api from '../../src/services/api'
import {
  MOCK_UPLOAD_TEXT_SUCCESS_RESPONSE,
  MOCK_UPLOAD_TEXT_MULTIPLE_SUCCESS_RESPONSE,
  MOCK_UPLOAD_TEXT_SHANGHAI_TIMEZONE_RESPONSE,
  MOCK_UPLOAD_TEXT_EMPTY_RESPONSE,
} from '../mock-data'

vi.mock('../../src/services/api')

describe('Integration Tests - Text Parsing to ICS Download', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('End-to-End Text Parsing Flow', () => {
    it('should complete full workflow: text input -> parse -> display -> download', async () => {
      const mockICSBlob = new Blob(['ICS content'], { type: 'text/calendar' })

      // Mock API calls
      api.uploadText.mockResolvedValueOnce(MOCK_UPLOAD_TEXT_SUCCESS_RESPONSE)
      api.downloadICS.mockResolvedValueOnce(mockICSBlob)

      render(<Home />)

      // Step 1: User enters text
      const textArea = screen.getByPlaceholderText(/enter text/i)
      await userEvent.type(textArea, 'Team meeting tomorrow at 2pm in Conference Room A')

      // Step 2: User clicks start button
      const startButton = screen.getByRole('button', { name: /start/i })
      await userEvent.click(startButton)

      // Step 3: Verify event is displayed
      await waitFor(() => {
        expect(screen.getByText('Team Weekly Standup')).toBeInTheDocument()
        expect(screen.getByText('Conference Room A')).toBeInTheDocument()
      })

      // Verify API was called correctly
      expect(api.uploadText).toHaveBeenCalled()

      // Step 4: User clicks download ICS button
      const downloadButton = screen.getByRole('button', { name: /download ics/i })
      await userEvent.click(downloadButton)

      // Step 5: Verify download was triggered
      await waitFor(() => {
        expect(api.downloadICS).toHaveBeenCalledWith([MOCK_UPLOAD_TEXT_SUCCESS_RESPONSE.events[0]])
      })
    })

    it('should handle multiple events in single input', async () => {
      api.uploadText.mockResolvedValueOnce(MOCK_UPLOAD_TEXT_MULTIPLE_SUCCESS_RESPONSE)

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      await userEvent.type(
        textArea,
        `Schedule for tomorrow:
        9am - Standup in Slack
        10am - Planning Meeting in Conference Room B
        12pm - Lunch in Cafeteria
        2pm - Client Call on Zoom
        3:30pm - Code Review`
      )

      const startButton = screen.getByRole('button', { name: /start/i })
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText('Morning Standup')).toBeInTheDocument()
        expect(screen.getByText('Project Planning Meeting')).toBeInTheDocument()
        expect(screen.getByText('Client Call')).toBeInTheDocument()
      })

      // Verify all events are present
      const eventItems = screen.getAllByTestId('event-item')
      expect(eventItems.length).toBeGreaterThan(1)
    })
  })

  describe('Timezone Handling Flow', () => {
    it('should apply timezone when checkbox is enabled', async () => {
      api.uploadText.mockResolvedValueOnce(MOCK_UPLOAD_TEXT_SHANGHAI_TIMEZONE_RESPONSE)

      render(<Home />)

      // Enable timezone checkbox
      const timezoneCheckbox = screen.getByLabelText(/use custom timezone/i)
      await userEvent.click(timezoneCheckbox)

      // Enter text
      const textArea = screen.getByPlaceholderText(/enter text/i)
      await userEvent.type(textArea, 'Meeting at 2pm')

      // Click start
      const startButton = screen.getByRole('button', { name: /start/i })
      await userEvent.click(startButton)

      // Verify timezone was passed to API
      await waitFor(() => {
        expect(api.uploadText).toHaveBeenCalledWith(
          expect.any(String),
          expect.stringContaining('/'),
          expect.any(String)
        )
      })

      // Verify timezone is displayed
      expect(screen.getByText(/Asia\/Shanghai/)).toBeInTheDocument()
    })

    it('should handle timezone changes between multiple parses', async () => {
      const response1 = MOCK_UPLOAD_TEXT_SUCCESS_RESPONSE
      const response2 = MOCK_UPLOAD_TEXT_SHANGHAI_TIMEZONE_RESPONSE

      api.uploadText
        .mockResolvedValueOnce(response1)
        .mockResolvedValueOnce(response2)

      render(<Home />)

      // First parse with UTC
      const textArea = screen.getByPlaceholderText(/enter text/i)
      await userEvent.type(textArea, 'First event')

      let startButton = screen.getByRole('button', { name: /start/i })
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText('Team Weekly Standup')).toBeInTheDocument()
      })

      // Clear and change timezone
      await userEvent.clear(textArea)
      const timezoneCheckbox = screen.getByLabelText(/use custom timezone/i)
      await userEvent.click(timezoneCheckbox)

      // Second parse with timezone
      await userEvent.type(textArea, 'Second event')
      startButton = screen.getByRole('button', { name: /start/i })
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(api.uploadText).toHaveBeenCalledTimes(2)
      })
    })
  })

  describe('Error Handling and Recovery', () => {
    it('should display error and allow retry', async () => {
      const errorMessage = 'Text parsing failed'

      // First call fails
      api.uploadText.mockRejectedValueOnce(new Error(errorMessage))

      // Second call succeeds
      api.uploadText.mockResolvedValueOnce(MOCK_UPLOAD_TEXT_SUCCESS_RESPONSE)

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      // First attempt - error
      await userEvent.type(textArea, 'First attempt')
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText(new RegExp(errorMessage, 'i'))).toBeInTheDocument()
      })

      // Clear and retry
      await userEvent.clear(textArea)
      await userEvent.type(textArea, 'Second attempt')
      await userEvent.click(startButton)

      // Should now succeed
      await waitFor(() => {
        expect(screen.getByText('Team Weekly Standup')).toBeInTheDocument()
      })
    })

    it('should handle empty events response gracefully', async () => {
      api.uploadText.mockResolvedValueOnce(MOCK_UPLOAD_TEXT_EMPTY_RESPONSE)

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Random text with no events')
      await userEvent.click(startButton)

      await waitFor(() => {
        const eventItems = screen.queryAllByTestId('event-item')
        expect(eventItems).toHaveLength(0)
      })
    })

    it('should prevent download when no events are available', async () => {
      api.uploadText.mockResolvedValueOnce(MOCK_UPLOAD_TEXT_EMPTY_RESPONSE)

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Text with no events')
      await userEvent.click(startButton)

      await waitFor(() => {
        const downloadButton = screen.queryByRole('button', { name: /download ics/i })
        expect(downloadButton).not.toBeInTheDocument()
      })
    })
  })

  describe('UI State Management', () => {
    it('should maintain form state during operations', async () => {
      api.uploadText.mockResolvedValueOnce(MOCK_UPLOAD_TEXT_SUCCESS_RESPONSE)

      render(<Home />)

      const textInput = 'Team meeting tomorrow at 2pm'
      const textArea = screen.getByPlaceholderText(/enter text/i)

      await userEvent.type(textArea, textInput)

      // Verify text is still in textarea after interaction
      expect(textArea.value).toBe(textInput)

      const startButton = screen.getByRole('button', { name: /start/i })
      await userEvent.click(startButton)

      // Text should remain in textarea
      await waitFor(() => {
        expect(textArea.value).toBe(textInput)
      })
    })

    it('should update checkbox states correctly', async () => {
      render(<Home />)

      const locationCheckbox = screen.getByLabelText(/use.*location/i)
      const timezoneCheckbox = screen.getByLabelText(/use custom timezone/i)

      // Both should be initially unchecked
      expect(locationCheckbox).not.toBeChecked()
      expect(timezoneCheckbox).not.toBeChecked()

      // Toggle location
      await userEvent.click(locationCheckbox)
      expect(locationCheckbox).toBeChecked()
      expect(timezoneCheckbox).not.toBeChecked()

      // Toggle timezone
      await userEvent.click(timezoneCheckbox)
      expect(locationCheckbox).toBeChecked()
      expect(timezoneCheckbox).toBeChecked()

      // Toggle both off
      await userEvent.click(locationCheckbox)
      await userEvent.click(timezoneCheckbox)
      expect(locationCheckbox).not.toBeChecked()
      expect(timezoneCheckbox).not.toBeChecked()
    })
  })

  describe('Data Validation', () => {
    it('should validate required fields before sending to API', async () => {
      render(<Home />)

      const startButton = screen.getByRole('button', { name: /start/i })

      // Try to start without input
      await userEvent.click(startButton)

      // Should show error or not call API
      expect(api.uploadText).not.toHaveBeenCalled()
    })

    it('should handle special characters in event data', async () => {
      const eventWithSpecialChars = {
        ...MOCK_UPLOAD_TEXT_SUCCESS_RESPONSE.events[0],
        title: 'Meeting: "Q4 Review" & Planning (Important!)',
        location: 'Room A & B',
      }

      api.uploadText.mockResolvedValueOnce({
        ...MOCK_UPLOAD_TEXT_SUCCESS_RESPONSE,
        events: [eventWithSpecialChars],
      })

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      await userEvent.type(textArea, 'Q4 Review meeting')

      const startButton = screen.getByRole('button', { name: /start/i })
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText(/Q4 Review/)).toBeInTheDocument()
      })
    })
  })

  describe('Accessibility and User Feedback', () => {
    it('should provide loading feedback during parsing', async () => {
      let resolveApi
      const apiPromise = new Promise((resolve) => {
        resolveApi = resolve
      })

      api.uploadText.mockReturnValueOnce(apiPromise)

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      await userEvent.type(textArea, 'Processing...')

      const startButton = screen.getByRole('button', { name: /start/i })
      await userEvent.click(startButton)

      // Allow loading state to appear
      await new Promise((resolve) => setTimeout(resolve, 100))

      // Resolve the API call
      resolveApi(MOCK_UPLOAD_TEXT_SUCCESS_RESPONSE)

      // Wait for results
      await waitFor(() => {
        expect(screen.getByText('Team Weekly Standup')).toBeInTheDocument()
      })
    })

    it('should show success feedback after parsing', async () => {
      api.uploadText.mockResolvedValueOnce(MOCK_UPLOAD_TEXT_SUCCESS_RESPONSE)

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      await userEvent.type(textArea, 'Test event')

      const startButton = screen.getByRole('button', { name: /start/i })
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText(/success/i)).toBeInTheDocument()
      })
    })

    it('should provide helpful error messages on failure', async () => {
      const errorMessage = 'Unable to parse text. Please check the format.'

      api.uploadText.mockRejectedValueOnce(new Error(errorMessage))

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      await userEvent.type(textArea, 'Invalid format')

      const startButton = screen.getByRole('button', { name: /start/i })
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText(new RegExp(errorMessage, 'i'))).toBeInTheDocument()
      })
    })
  })
})
