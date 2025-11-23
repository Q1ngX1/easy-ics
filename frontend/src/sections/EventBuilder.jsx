import { useState } from 'react'
import { downloadICS } from '../services/api'

export default function EventBuilder() {
	const [event, setEvent] = useState({
		title: '',
		startTime: '',
		startDate: '',
		endTime: '',
		endDate: '',
		location: '',
		description: '',
		remindMinutes: 15,
		isFullDay: false,
	})
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState(null)
	const [success, setSuccess] = useState(null)

	/**
	 * Calculate end time by adding 30 minutes to start time
	 */
	const calculateEndTime = (startTime) => {
		if (!startTime) return ''
		const [hours, minutes] = startTime.split(':').map(Number)
		const startDate = new Date()
		startDate.setHours(hours, minutes, 0)
		
		// Add 30 minutes
		const endDate = new Date(startDate.getTime() + 30 * 60000)
		const endHours = String(endDate.getHours()).padStart(2, '0')
		const endMinutes = String(endDate.getMinutes()).padStart(2, '0')
		
		return `${endHours}:${endMinutes}`
	}

	const handleInputChange = (e) => {
		const { name, value, type, checked } = e.target
		const inputValue = type === 'checkbox' ? checked : value

		setEvent((prev) => {
			const updated = {
				...prev,
				[name]: inputValue,
			}

			// Auto-calculate end time when start time is set
			if (name === 'startTime' && !prev.isFullDay) {
				updated.endTime = calculateEndTime(value)
			}

			// Handle full-day event toggle
			if (name === 'isFullDay' && inputValue) {
				// When enabling full-day, set times to 00:00 and 23:59
				updated.startTime = '00:00'
				updated.endTime = '23:59'
			} else if (name === 'isFullDay' && !inputValue) {
				// When disabling full-day, reset to calculated times
				updated.startTime = ''
				updated.endTime = ''
			}

			return updated
		})
	}

	const validateForm = () => {
		if (!event.title.trim()) {
			setError('Event title is required')
			return false
		}
		if (!event.startDate) {
			setError('Start date is required')
			return false
		}
		if (!event.isFullDay && !event.startTime) {
			setError('Start time is required')
			return false
		}
		if (!event.endDate) {
			setError('End date is required')
			return false
		}
		if (!event.isFullDay && !event.endTime) {
			setError('End time is required')
			return false
		}

		if (!event.isFullDay) {
			const startDateTime = new Date(`${event.startDate}T${event.startTime}`)
			const endDateTime = new Date(`${event.endDate}T${event.endTime}`)

			if (endDateTime <= startDateTime) {
				setError('End time must be after start time')
				return false
			}
		}

		return true
	}

	const handleDownload = async () => {
		setError(null)
		setSuccess(null)

		if (!validateForm()) {
			return
		}

		setLoading(true)

		try {
			const startDateTime = `${event.startDate}T${event.startTime}:00`
			const endDateTime = `${event.endDate}T${event.endTime}:00`

			const events = [
				{
					title: event.title,
					start_time: startDateTime,
					end_time: endDateTime,
					location: event.location || undefined,
					description: event.description || undefined,
				},
			]

			await downloadICS(events)
			setSuccess('ICS file downloaded successfully!')

			// Reset form after success
			setTimeout(() => {
				setEvent({
					title: '',
					startTime: '',
					startDate: '',
					endTime: '',
					endDate: '',
					location: '',
					description: '',
					remindMinutes: 15,
					isFullDay: false,
				})
				setSuccess(null)
			}, 2000)
		} catch (err) {
			setError(err.message || 'Failed to download ICS file')
		} finally {
			setLoading(false)
		}
	}

	const handleClear = () => {
		setEvent({
			title: '',
			startTime: '',
			startDate: '',
			endTime: '',
			endDate: '',
			location: '',
			description: '',
			remindMinutes: 15,
			isFullDay: false,
		})
		setError(null)
		setSuccess(null)
	}

	return (
		<div className="event-builder">
			<h2>Create Event</h2>

			{error && (
				<div className="message error-message">
					<p>{error}</p>
					<button
						type="button"
						className="message-close"
						onClick={() => setError(null)}
					>
						✕
					</button>
				</div>
			)}

			{success && (
				<div className="message success-message">
					<p>{success}</p>
					<button
						type="button"
						className="message-close"
						onClick={() => setSuccess(null)}
					>
						✕
					</button>
				</div>
			)}

			<form className="event-form">
				{/* Event Title */}
				<div className="form-group">
					<label htmlFor="title">Event Title *</label>
					<input
						type="text"
						id="title"
						name="title"
						value={event.title}
						onChange={handleInputChange}
						placeholder="Enter event title"
						maxLength="100"
						required
					/>
				</div>

				{/* Full-day Event Checkbox */}
				<div className="form-group checkbox-group">
					<label htmlFor="isFullDay" className="checkbox-label">
						<input
							type="checkbox"
							id="isFullDay"
							name="isFullDay"
							checked={event.isFullDay}
							onChange={handleInputChange}
						/>
						<span>Full day event</span>
					</label>
				</div>

				{/* Start Date & Time */}
				<div className="form-row">
					<div className="form-group">
						<label htmlFor="startDate">Start Date *</label>
						<input
							type="date"
							id="startDate"
							name="startDate"
							value={event.startDate}
							onChange={handleInputChange}
							required
						/>
					</div>
					{!event.isFullDay && (
						<div className="form-group">
							<label htmlFor="startTime">Start Time *</label>
							<input
								type="time"
								id="startTime"
								name="startTime"
								value={event.startTime}
								onChange={handleInputChange}
								required
							/>
						</div>
					)}
				</div>

				{/* End Date & Time */}
				<div className="form-row">
					<div className="form-group">
						<label htmlFor="endDate">End Date *</label>
						<input
							type="date"
							id="endDate"
							name="endDate"
							value={event.endDate}
							onChange={handleInputChange}
							required
						/>
					</div>
					{!event.isFullDay && (
						<div className="form-group">
							<label htmlFor="endTime">End Time *</label>
							<input
								type="time"
								id="endTime"
								name="endTime"
								value={event.endTime}
								onChange={handleInputChange}
								required
							/>
						</div>
					)}
				</div>

				{/* Location */}
				<div className="form-group">
					<label htmlFor="location">Location</label>
					<input
						type="text"
						id="location"
						name="location"
						value={event.location}
						onChange={handleInputChange}
						placeholder="Enter event location"
						maxLength="200"
					/>
				</div>

				{/* Description */}
				<div className="form-group">
					<label htmlFor="description">Description</label>
					<textarea
						id="description"
						name="description"
						value={event.description}
						onChange={handleInputChange}
						placeholder="Enter event description (optional)"
						maxLength="500"
						rows="4"
					/>
				</div>

				{/* Reminder */}
				<div className="form-group">
					<label htmlFor="remindMinutes">Reminder (minutes before)</label>
					<select
						id="remindMinutes"
						name="remindMinutes"
						value={event.remindMinutes}
						onChange={handleInputChange}
					>
						<option value="0">No reminder</option>
						<option value="5">5 minutes</option>
						<option value="15">15 minutes</option>
						<option value="30">30 minutes</option>
						<option value="60">1 hour</option>
						<option value="1440">1 day</option>
					</select>
				</div>

				{/* Form Actions */}
				<div className="form-actions">
					<button
						type="button"
						className="btn btn-primary"
						onClick={handleDownload}
						disabled={loading}
					>
						{loading ? 'Downloading...' : 'Download ICS'}
					</button>
					<button
						type="button"
						className="btn btn-secondary"
						onClick={handleClear}
						disabled={loading}
					>
						Clear
					</button>
				</div>
			</form>
		</div>
	)
}
