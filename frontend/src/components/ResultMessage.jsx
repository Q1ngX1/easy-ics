import PropTypes from 'prop-types'

export default function ResultMessage({
    result,
    loading,
    onDownload,
    onClose,
}) {
    if (!result || result.length === 0) return null

    return (
        <div className="message-box success-box">
            <span className="message-icon">✓</span>
            <div className="result-content">
                <p>
                    Successfully parsed <strong>{result.length}</strong> event(s)!
                </p>
                <button
                    type="button"
                    className="cta-button secondary"
                    onClick={onDownload}
                    disabled={loading}
                    aria-label="Download ICS file"
                >
                    {loading ? 'Downloading...' : '⬇ Download ICS'}
                </button>
            </div>
            <button
                type="button"
                className="message-close"
                onClick={onClose}
                aria-label="Close result message"
            >
                ✕
            </button>
        </div>
    )
}

ResultMessage.propTypes = {
    result: PropTypes.array,
    loading: PropTypes.bool.isRequired,
    onDownload: PropTypes.func.isRequired,
    onClose: PropTypes.func.isRequired,
}
