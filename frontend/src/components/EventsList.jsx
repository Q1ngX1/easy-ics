import { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import { downloadICS, triggerDownload } from '../services/api'

export default function EventsList({
    events,
    loading,
    onClose,
}) {
    const [editedEvents, setEditedEvents] = useState([])
    const [downloading, setDownloading] = useState(false)
    const [expandedIndex, setExpandedIndex] = useState(null) // Track which event is expanded
    const [collapsing, setCollapsing] = useState(null) // Track which event is collapsing for animation

    // Sync editedEvents whenever events prop changes
    useEffect(() => {
        if (events && events.length > 0) {
            setEditedEvents(events)
        } else {
            setEditedEvents([])
        }
    }, [events])

    if (!events || events.length === 0) return null

    const handleEditChange = (index, field, value) => {
        const updated = [...editedEvents]
        updated[index] = {
            ...updated[index],
            [field]: value,
        }
        setEditedEvents(updated)
    }

    const handleRemoveEvent = (index) => {
        const updatedEvents = editedEvents.filter((_, i) => i !== index)
        setEditedEvents(updatedEvents)
        
        // If this was the last event, close the EventsList
        if (updatedEvents.length === 0) {
            onClose()
        }
    }

    const handleToggleExpand = (index) => {
        if (expandedIndex === index) {
            // Trigger collapse animation
            setCollapsing(index)
            // Wait for animation to complete before actually collapsing
            setTimeout(() => {
                setExpandedIndex(null)
                setCollapsing(null)
            }, 400)
        } else {
            // Expand immediately
            setExpandedIndex(index)
            setCollapsing(null)
        }
    }

    const handleDownloadSingle = async (event) => {
        setDownloading(true)
        try {
            const icsBlob = await downloadICS([event])
            triggerDownload(icsBlob, `event-${event.title || 'calendar'}.ics`)
        } catch (err) {
            console.error('Download error:', err)
            alert('Failed to download event')
        } finally {
            setDownloading(false)
        }
    }

    const handleDownloadAll = async () => {
        if (editedEvents.length === 0) {
            alert('No events to download')
            return
        }
        setDownloading(true)
        try {
            const icsBlob = await downloadICS(editedEvents)
            triggerDownload(icsBlob, 'calendar.ics')
        } catch (err) {
            console.error('Download error:', err)
            alert('Failed to download events')
        } finally {
            setDownloading(false)
        }
    }

    return (
        <div className="events-list-container">
            <div className="events-list-header">
                <h3>Parsed Events ({editedEvents.length})</h3>
                <button
                    type="button"
                    className="message-close"
                    onClick={onClose}
                    aria-label="Close events list"
                    title="Close"
                >
                    ✕
                </button>
            </div>

            <div className="events-list">
                {editedEvents.map((event, index) => (
                    <div 
                        key={index} 
                        className={`event-card ${expandedIndex === index ? 'expanded' : 'collapsed'}`}
                    >
                        {/* Collapsed Header - Always Visible */}
                        <div className="event-card-collapsed">
                            <button
                                type="button"
                                className="event-expand-btn"
                                onClick={() => handleToggleExpand(index)}
                                title={expandedIndex === index ? 'Collapse' : 'Expand'}
                                aria-label={`${expandedIndex === index ? 'Collapse' : 'Expand'} event ${index + 1}`}
                            >
                                {expandedIndex === index ? '▼' : '▶'}
                            </button>
                            <h4 className="event-title">{event.title || 'Untitled Event'}</h4>
                            <div className="event-collapsed-actions">
                                <button
                                    type="button"
                                    className="event-download-btn"
                                    onClick={() => handleDownloadSingle(editedEvents[index])}
                                    disabled={downloading || loading}
                                    title="Download this event"
                                >
                                    ⬇
                                </button>
                                <button
                                    type="button"
                                    className="event-remove-btn"
                                    onClick={() => handleRemoveEvent(index)}
                                    title="Remove event"
                                    aria-label={`Remove event ${index + 1}`}
                                >
                                    ✕
                                </button>
                            </div>
                        </div>

                        {/* Expanded Content - Only when expanded */}
                        {(expandedIndex === index || collapsing === index) && (
                            <div 
                                className={`event-card-expanded ${collapsing === index ? 'collapsing' : ''}`}
                            >
                                <div className="event-fields">
                                    {/* Title */}
                                    <div className="event-field">
                                        <label>Title</label>
                                        <input
                                            type="text"
                                            value={event.title || ''}
                                            onChange={(e) =>
                                                handleEditChange(index, 'title', e.target.value)
                                            }
                                            placeholder="Event title"
                                        />
                                    </div>

                                    {/* Start Date */}
                                    <div className="event-field">
                                        <label>Start Date</label>
                                        <input
                                            type="date"
                                            value={event.startDate || ''}
                                            onChange={(e) =>
                                                handleEditChange(index, 'startDate', e.target.value)
                                            }
                                        />
                                    </div>

                                    {/* Start Time */}
                                    {!event.isFullDay && (
                                        <div className="event-field">
                                            <label>Start Time</label>
                                            <input
                                                type="time"
                                                value={event.startTime || ''}
                                                onChange={(e) =>
                                                    handleEditChange(index, 'startTime', e.target.value)
                                                }
                                            />
                                        </div>
                                    )}

                                    {/* End Date */}
                                    <div className="event-field">
                                        <label>End Date</label>
                                        <input
                                            type="date"
                                            value={event.endDate || ''}
                                            onChange={(e) =>
                                                handleEditChange(index, 'endDate', e.target.value)
                                            }
                                        />
                                    </div>

                                    {/* End Time */}
                                    {!event.isFullDay && (
                                        <div className="event-field">
                                            <label>End Time</label>
                                            <input
                                                type="time"
                                                value={event.endTime || ''}
                                                onChange={(e) =>
                                                    handleEditChange(index, 'endTime', e.target.value)
                                                }
                                            />
                                        </div>
                                    )}

                                    {/* Location */}
                                    <div className="event-field">
                                        <label>Location</label>
                                        <input
                                            type="text"
                                            value={event.location || ''}
                                            onChange={(e) =>
                                                handleEditChange(index, 'location', e.target.value)
                                            }
                                            placeholder="Event location"
                                        />
                                    </div>

                                    {/* Description */}
                                    <div className="event-field">
                                        <label>Description</label>
                                        <textarea
                                            value={event.description || ''}
                                            onChange={(e) =>
                                                handleEditChange(index, 'description', e.target.value)
                                            }
                                            placeholder="Event description"
                                            rows="3"
                                        />
                                    </div>

                                    {/* Full Day Event Checkbox */}
                                    <div className="event-field checkbox-field">
                                        <label className="checkbox-label">
                                            <input
                                                type="checkbox"
                                                checked={event.isFullDay || false}
                                                onChange={(e) =>
                                                    handleEditChange(
                                                        index,
                                                        'isFullDay',
                                                        e.target.checked
                                                    )
                                                }
                                            />
                                            <span>Full day event</span>
                                        </label>
                                    </div>

                                    {/* Reminder */}
                                    <div className="event-field">
                                        <label>Reminder (minutes before)</label>
                                        <select
                                            value={event.remindMinutes || 15}
                                            onChange={(e) =>
                                                handleEditChange(
                                                    index,
                                                    'remindMinutes',
                                                    parseInt(e.target.value)
                                                )
                                            }
                                        >
                                            <option value="0">No reminder</option>
                                            <option value="5">5 minutes</option>
                                            <option value="15">15 minutes</option>
                                            <option value="30">30 minutes</option>
                                            <option value="60">1 hour</option>
                                            <option value="1440">1 day</option>
                                        </select>
                                    </div>
                                </div>

                                {/* Single Event Download Button */}
                                <button
                                    type="button"
                                    className="cta-button primary"
                                    onClick={() => handleDownloadSingle(editedEvents[index])}
                                    disabled={downloading || loading}
                                    title="Download this event as ICS"
                                >
                                    ⬇ Download Event
                                </button>
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {/* Download All Button */}
            {editedEvents.length > 0 && (
                <div className="events-list-footer">
                    <button
                        type="button"
                        className="cta-button primary large"
                        onClick={handleDownloadAll}
                        disabled={downloading || loading}
                        title="Download all events as ICS"
                    >
                        {downloading ? 'Downloading...' : `⬇ Download All (${editedEvents.length})`}
                    </button>
                </div>
            )}
        </div>
    )
}

EventsList.propTypes = {
    events: PropTypes.arrayOf(PropTypes.object),
    loading: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
}
