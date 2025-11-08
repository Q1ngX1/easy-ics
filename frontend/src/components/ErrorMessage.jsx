import PropTypes from 'prop-types'

export default function ErrorMessage({ error, onClose }) {
    if (!error) return null

    return (
        <div className="message-box error-box">
            <span className="message-icon">✘</span>
            <p>{error}</p>
            <button
                type="button"
                className="message-close"
                onClick={onClose}
                aria-label="Close error message"
            >
                ✕
            </button>
        </div>
    )
}

ErrorMessage.propTypes = {
    error: PropTypes.string,
    onClose: PropTypes.func.isRequired,
}
