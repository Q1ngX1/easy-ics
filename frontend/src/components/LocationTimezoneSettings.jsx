import PropTypes from 'prop-types'

export default function LocationTimezoneSettings({
    useLocation,
    locationInfo,
    useTimezone,
    timezoneInfo,
    onLocationChange,
    onTimezoneChange,
}) {
    return (
        <div className="check-box">
            <label className="checkbox-label">
                <input
                    type="checkbox"
                    checked={useLocation}
                    onChange={(e) => onLocationChange(e.target.checked)}
                />
                <span>Use my location</span>
                {locationInfo && (
                    <span className="info-text">
                        ({locationInfo.latitude.toFixed(4)}, {locationInfo.longitude.toFixed(4)})
                    </span>
                )}
            </label>

            <label className="checkbox-label">
                <input
                    type="checkbox"
                    checked={useTimezone}
                    onChange={(e) => onTimezoneChange(e.target.checked)}
                />
                <span>Use my timezone</span>
                {timezoneInfo && (
                    <span className="info-text">({timezoneInfo.timezone})</span>
                )}
            </label>
        </div>
    )
}

LocationTimezoneSettings.propTypes = {
    useLocation: PropTypes.bool.isRequired,
    locationInfo: PropTypes.object,
    useTimezone: PropTypes.bool.isRequired,
    timezoneInfo: PropTypes.object,
    onLocationChange: PropTypes.func.isRequired,
    onTimezoneChange: PropTypes.func.isRequired,
}
