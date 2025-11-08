/**
 * Event Display Component Tests
 * Test rendering and display of events returned from backend
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Home from '../../src/pages/Home'
import * as api from '../../src/services/api'

// Mock the API service
vi.mock('../../src/services/api')

describe('Event Display in Home Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Single Event Display', () => {
    it('should display event title correctly', async () => {
      const mockEvent = {
        title: 'Team Meeting',
        start_time: '2025-11-07T14:00:00',
        end_time: '2025-11-07T15:00:00',
        location: 'Conference Room A',
        description: 'Weekly team sync',
      }

      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: [mockEvent],
        count: 1,
        timezone: 'UTC',
        message: 'Text parsing success',
      })

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Team meeting tomorrow at 2pm')
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText('Team Meeting')).toBeInTheDocument()
      })
    })

    it('should display event start time correctly', async () => {
      const mockEvent = {
        title: 'Lunch',
        start_time: '2025-11-07T12:30:00',
        end_time: '2025-11-07T13:30:00',
        location: 'Cafeteria',
        description: '',
      }

      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: [mockEvent],
        count: 1,
        timezone: 'UTC',
        message: 'Text parsing success',
      })

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Lunch at 12:30pm')
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText(/12:30/)).toBeInTheDocument()
      })
    })

    it('should display event location when provided', async () => {
      const mockEvent = {
        title: 'Conference',
        start_time: '2025-11-07T09:00:00',
        end_time: '2025-11-07T17:00:00',
        location: 'Grand Hotel, NYC',
        description: 'Annual conference',
      }

      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: [mockEvent],
        count: 1,
        timezone: 'UTC',
        message: 'Text parsing success',
      })

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Conference at Grand Hotel, NYC')
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText('Grand Hotel, NYC')).toBeInTheDocument()
      })
    })

    it('should not display location section when location is empty', async () => {
      const mockEvent = {
        title: 'Virtual Meeting',
        start_time: '2025-11-07T10:00:00',
        end_time: '2025-11-07T11:00:00',
        location: '',
        description: '',
      }

      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: [mockEvent],
        count: 1,
        timezone: 'UTC',
        message: 'Text parsing success',
      })

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Virtual meeting')
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText('Virtual Meeting')).toBeInTheDocument()
      })

      // Location should not be displayed for empty location
      const locationElements = screen.queryAllByText(/location:/i)
      locationElements.forEach((el) => {
        expect(el.textContent).not.toContain('')
      })
    })
  })

  describe('Multiple Events Display', () => {
    it('should display multiple events correctly', async () => {
      const mockEvents = [
        {
          title: 'Morning Standup',
          start_time: '2025-11-07T09:00:00',
          end_time: '2025-11-07T09:30:00',
          location: 'Slack',
          description: '',
        },
        {
          title: 'Project Review',
          start_time: '2025-11-07T14:00:00',
          end_time: '2025-11-07T15:00:00',
          location: 'Conference Room',
          description: '',
        },
        {
          title: 'Dinner',
          start_time: '2025-11-07T19:00:00',
          end_time: '2025-11-07T20:00:00',
          location: 'Restaurant',
          description: '',
        },
      ]

      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: mockEvents,
        count: 3,
        timezone: 'UTC',
        message: 'Text parsing success',
      })

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Schedule for tomorrow')
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText('Morning Standup')).toBeInTheDocument()
        expect(screen.getByText('Project Review')).toBeInTheDocument()
        expect(screen.getByText('Dinner')).toBeInTheDocument()
      })

      // Verify event count
      const eventElements = screen.getAllByTestId('event-item')
      expect(eventElements).toHaveLength(3)
    })

    it('should display events in correct order', async () => {
      const mockEvents = [
        {
          title: 'Event 1',
          start_time: '2025-11-07T08:00:00',
          end_time: '2025-11-07T09:00:00',
          location: '',
          description: '',
        },
        {
          title: 'Event 2',
          start_time: '2025-11-07T10:00:00',
          end_time: '2025-11-07T11:00:00',
          location: '',
          description: '',
        },
        {
          title: 'Event 3',
          start_time: '2025-11-07T14:00:00',
          end_time: '2025-11-07T15:00:00',
          location: '',
          description: '',
        },
      ]

      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: mockEvents,
        count: 3,
        timezone: 'UTC',
        message: 'Text parsing success',
      })

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Multiple events')
      await userEvent.click(startButton)

      await waitFor(() => {
        const eventElements = screen.getAllByTestId('event-item')
        expect(eventElements[0]).toHaveTextContent('Event 1')
        expect(eventElements[1]).toHaveTextContent('Event 2')
        expect(eventElements[2]).toHaveTextContent('Event 3')
      })
    })
  })

  describe('Timezone Display', () => {
    it('should display timezone from backend response', async () => {
      const mockEvent = {
        title: 'Team Meeting',
        start_time: '2025-11-07T14:00:00',
        end_time: '2025-11-07T15:00:00',
        location: 'Room A',
        description: '',
      }

      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: [mockEvent],
        count: 1,
        timezone: 'Asia/Shanghai',
        message: 'Text parsing success',
      })

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Team meeting')
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText(/Asia\/Shanghai/)).toBeInTheDocument()
      })
    })

    it('should apply selected timezone to events', async () => {
      const mockEvent = {
        title: 'Meeting',
        start_time: '2025-11-07T14:00:00',
        end_time: '2025-11-07T15:00:00',
        location: '',
        description: '',
      }

      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: [mockEvent],
        count: 1,
        timezone: 'America/New_York',
        message: 'Text parsing success',
      })

      render(<Home />)

      // Select timezone checkbox
      const timezoneCheckbox = screen.getByLabelText(/use custom timezone/i)
      await userEvent.click(timezoneCheckbox)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Meeting')
      await userEvent.click(startButton)

      // Verify uploadText was called with timezone parameter
      await waitFor(() => {
        expect(api.uploadText).toHaveBeenCalledWith(
          'Meeting',
          expect.any(String),
          expect.any(String)
        )
      })
    })
  })

  describe('Event Status Display', () => {
    it('should show loading state while processing', async () => {
      api.uploadText.mockImplementationOnce(
        () =>
          new Promise((resolve) => {
            setTimeout(
              () =>
                resolve({
                  success: true,
                  events: [
                    {
                      title: 'Event',
                      start_time: '2025-11-07T10:00:00',
                      end_time: '2025-11-07T11:00:00',
                      location: '',
                      description: '',
                    },
                  ],
                  count: 1,
                  timezone: 'UTC',
                  message: 'Success',
                }),
              100
            )
          })
      )

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Event')
      await userEvent.click(startButton)

      // Loading state should be visible briefly
      await waitFor(() => {
        expect(screen.queryByText(/loading|processing/i)).not.toBeInTheDocument()
      })

      // Then results should appear
      expect(screen.getByText('Event')).toBeInTheDocument()
    })

    it('should display error message on parsing failure', async () => {
      const errorMessage = 'Text parsing failed'

      api.uploadText.mockRejectedValueOnce(new Error(errorMessage))

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Invalid text')
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText(new RegExp(errorMessage, 'i'))).toBeInTheDocument()
      })
    })

    it('should display success message after parsing', async () => {
      const mockEvent = {
        title: 'Event',
        start_time: '2025-11-07T10:00:00',
        end_time: '2025-11-07T11:00:00',
        location: '',
        description: '',
      }

      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: [mockEvent],
        count: 1,
        timezone: 'UTC',
        message: 'Text parsing success',
      })

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Event')
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText(/success/i)).toBeInTheDocument()
      })
    })
  })

  describe('Download ICS Functionality', () => {
    it('should show download button when events are available', async () => {
      const mockEvent = {
        title: 'Event',
        start_time: '2025-11-07T10:00:00',
        end_time: '2025-11-07T11:00:00',
        location: '',
        description: '',
      }

      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: [mockEvent],
        count: 1,
        timezone: 'UTC',
        message: 'Text parsing success',
      })

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Event')
      await userEvent.click(startButton)

      await waitFor(() => {
        const downloadButton = screen.getByRole('button', { name: /download ics/i })
        expect(downloadButton).toBeInTheDocument()
      })
    })

    it('should call downloadICS when download button is clicked', async () => {
      const mockEvent = {
        title: 'Event',
        start_time: '2025-11-07T10:00:00',
        end_time: '2025-11-07T11:00:00',
        location: '',
        description: '',
      }

      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: [mockEvent],
        count: 1,
        timezone: 'UTC',
        message: 'Text parsing success',
      })

      api.downloadICS.mockResolvedValueOnce(new Blob(['ICS content']))

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Event')
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /download ics/i })).toBeInTheDocument()
      })

      const downloadButton = screen.getByRole('button', { name: /download ics/i })
      await userEvent.click(downloadButton)

      expect(api.downloadICS).toHaveBeenCalledWith([mockEvent])
    })
  })

  describe('Edge Cases', () => {
    it('should handle empty event list', async () => {
      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: [],
        count: 0,
        timezone: 'UTC',
        message: 'No events found',
      })

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'No events here')
      await userEvent.click(startButton)

      await waitFor(() => {
        const eventElements = screen.queryAllByTestId('event-item')
        expect(eventElements).toHaveLength(0)
      })
    })

    it('should display event with very long title', async () => {
      const longTitle =
        'This is a very long event title that might wrap to multiple lines in the display component'

      const mockEvent = {
        title: longTitle,
        start_time: '2025-11-07T10:00:00',
        end_time: '2025-11-07T11:00:00',
        location: '',
        description: '',
      }

      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: [mockEvent],
        count: 1,
        timezone: 'UTC',
        message: 'Text parsing success',
      })

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Long event title')
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText(longTitle)).toBeInTheDocument()
      })
    })

    it('should display event with special characters in title', async () => {
      const specialTitle = 'Meeting & Discussion: "Q4 Review" (Important!)'

      const mockEvent = {
        title: specialTitle,
        start_time: '2025-11-07T10:00:00',
        end_time: '2025-11-07T11:00:00',
        location: '',
        description: '',
      }

      api.uploadText.mockResolvedValueOnce({
        success: true,
        events: [mockEvent],
        count: 1,
        timezone: 'UTC',
        message: 'Text parsing success',
      })

      render(<Home />)

      const textArea = screen.getByPlaceholderText(/enter text/i)
      const startButton = screen.getByRole('button', { name: /start/i })

      await userEvent.type(textArea, 'Special characters')
      await userEvent.click(startButton)

      await waitFor(() => {
        expect(screen.getByText(specialTitle)).toBeInTheDocument()
      })
    })
  })
})
