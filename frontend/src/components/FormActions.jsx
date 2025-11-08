import PropTypes from 'prop-types'

export default function FormActions({
    hasInput,
    loading,
    onClear,
}) {
    return (
        <div className="form-row button-row">
            <button
                type="submit"
                className="cta-button"
                disabled={!hasInput || loading}
                aria-label="Convert selected input to ICS"
            >
                {loading ? 'Processing...' : 'Convert'}
            </button>
            <button
                type="button"
                className="cta-button secondary"
                onClick={onClear}
                disabled={loading}
                aria-label="Clear all inputs and results"
            >
                Clear all
            </button>
        </div>
    )
}

FormActions.propTypes = {
    hasInput: PropTypes.bool.isRequired,
    loading: PropTypes.bool.isRequired,
    onClear: PropTypes.func.isRequired,
}
