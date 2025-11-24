import PropTypes from 'prop-types'

export default function TextInputField({
    text,
    hasImages,
    loading,
    onChange,
}) {
    return (
        <label className="form-row text-input-label">
            
            <span className="label-text">Enter text or description</span>
            <textarea
                value={text}
                onChange={onChange}
                placeholder="Enter the text you want to recognize, dates, or any related information..."
                className={`text-input ${hasImages ? 'disabled' : ''}`}
                rows="4"
                disabled={hasImages || loading}
            />
        </label>
    )
}

TextInputField.propTypes = {
    text: PropTypes.string.isRequired,
    hasImages: PropTypes.bool.isRequired,
    loading: PropTypes.bool.isRequired,
    onChange: PropTypes.func.isRequired,
}
