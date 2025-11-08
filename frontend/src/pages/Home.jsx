import '../styles/pages.css'
import '../styles/checkbox.css'
import { useHome } from '../hooks/useHome'
import {
    ImageUploadArea,
    TextInputField,
    ErrorMessage,
    ResultMessage,
    LocationTimezoneSettings,
    FormActions,
} from '../components'

export default function Home() {
    const {
        image,
        text,
        dragActive,
        contextMenu,
        loading,
        result,
        error,
        useLocation,
        locationInfo,
        useTimezone,
        timezoneInfo,
        hasImage,
        hasText,
        hasInput,
        handleImageChange,
        handleDrag,
        handleDrop,
        handleClear,
        handleStart,
        handleDownloadICS,
        handleContextMenu,
        pasteFromClipboard,
        handleLocationChange,
        handleTimezoneChange,
        setText,
        setImage,
        setError,
        setResult,
    } = useHome()

    return (
        <div className="page-content home-form">
            <h1>Get Started</h1>

            {/* Error Message Component */}
            <ErrorMessage
                error={error}
                onClose={() => setError(null)}
            />

            {/* Location & Timezone Settings Component */}
            <LocationTimezoneSettings
                useLocation={useLocation}
                locationInfo={locationInfo}
                useTimezone={useTimezone}
                timezoneInfo={timezoneInfo}
                onLocationChange={handleLocationChange}
                onTimezoneChange={handleTimezoneChange}
            />

            {/* Result Message Component */}
            <ResultMessage
                result={result}
                loading={loading}
                onDownload={handleDownloadICS}
                onClose={() => {
                    setResult(null)
                    setImage(null)
                    setText('')
                }}
            />

            <form onSubmit={handleStart} className="simple-form">
                {/* Image Upload Area Component */}
                <ImageUploadArea
                    image={image}
                    hasText={hasText}
                    loading={loading}
                    dragActive={dragActive}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    onImageChange={handleImageChange}
                    onContextMenu={handleContextMenu}
                    contextMenu={contextMenu}
                    onPasteFromClipboard={pasteFromClipboard}
                />

                {/* Text Input Field Component */}
                <TextInputField
                    text={text}
                    hasImage={hasImage}
                    loading={loading}
                    onChange={(e) => {
                        const v = e.target.value
                        setText(v)
                        if (v.trim().length > 0) {
                            setImage(null)
                        }
                    }}
                />

                {/* Form Actions Component */}
                <FormActions
                    hasInput={hasInput}
                    loading={loading}
                    onClear={handleClear}
                />
            </form>
        </div>
    )
}