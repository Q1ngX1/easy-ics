import PropTypes from 'prop-types'

export default function TextInputField({
    text,
    hasImage,
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
                className={`text-input ${hasImage ? 'disabled' : ''}`}
                rows="4"
                disabled={hasImage || loading}
            />
        </label>
    )
}

TextInputField.propTypes = {
    text: PropTypes.string.isRequired,
    hasImage: PropTypes.bool.isRequired,
    loading: PropTypes.bool.isRequired,
    onChange: PropTypes.func.isRequired,
}
