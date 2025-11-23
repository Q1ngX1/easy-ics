/**
 * OCRPanel - OCR image upload and text parsing section
 * 
 * Functionality:
 * - Upload single or multiple images for OCR
 * - Parse text content and extract events
 * - Display parsed results
 * - Download ICS calendar files
 */

import { useState } from 'react'
import { useImageUpload } from '../hooks/useImageUpload'
import { useClipboard } from '../hooks/useClipboard'
import { useLocationSettings } from '../hooks/useLocationSettings'
import { useProcessing } from '../hooks/useProcessing'
import {
    ImageUploadArea,
    TextInputField,
    ErrorMessage,
    ResultMessage,
    LocationTimezoneSettings,
    FormActions,
} from '../components'

export default function OCRPanel() {
    // Use specialized hooks instead of monolithic useHome
    const imageUpload = useImageUpload()
    const clipboard = useClipboard()
    const locationSettings = useLocationSettings()
    const processing = useProcessing()

    // Manage text state locally since it's OCRPanel-specific
    const [text, setText] = useState('')
    const hasText = text.trim().length > 0

    // Combined derived state
    const hasInput = imageUpload.hasImages || hasText

    // Unified clear handler
    const handleClear = () => {
        imageUpload.clearImages()
        setText('')
        processing.clear()
    }

    // Handle paste from clipboard
    const handlePasteFromClipboard = async () => {
        const files = await clipboard.pasteFromClipboard()
        if (files.length > 0) {
            imageUpload.handleImageChange(files)
        }
    }

    // Unified start handler with all integrations
    const handleStart = async (e) => {
        if (e && e.preventDefault) {
            e.preventDefault()
        }

        await processing.handleStart(
            imageUpload.images,
            text,
            locationSettings.timezoneInfo,
            // Location request callback
            locationSettings.useLocation && !locationSettings.locationInfo
                ? async () => {
                    try {
                        const location = await locationSettings.getUserLocation()
                        locationSettings.setLocationInfo(location)
                    } catch (err) {
                        console.warn('Location permission denied:', err)
                        locationSettings.handleLocationChange(false)
                    }
                }
                : null,
            // Timezone request callback
            locationSettings.useTimezone && !locationSettings.timezoneInfo
                ? () => {
                    locationSettings.setTimezoneInfo(locationSettings.getTimezone())
                }
                : null
        )
    }

    return (
        <div className="ocr-panel">
            <h2>Upload & Parse</h2>

            {/* Error Message Component */}
            <ErrorMessage
                error={processing.error}
                onClose={() => processing.setError(null)}
            />

            {/* Location & Timezone Settings Component */}
            <LocationTimezoneSettings
                useLocation={locationSettings.useLocation}
                locationInfo={locationSettings.locationInfo}
                useTimezone={locationSettings.useTimezone}
                timezoneInfo={locationSettings.timezoneInfo}
                onLocationChange={locationSettings.handleLocationChange}
                onTimezoneChange={locationSettings.handleTimezoneChange}
            />

            {/* Result Message Component */}
            <ResultMessage
                result={processing.result}
                loading={processing.loading}
                onDownload={processing.handleDownloadICS}
                onClose={() => {
                    processing.setResult(null)
                    imageUpload.clearImages()
                    setText('')
                }}
            />

            <form onSubmit={handleStart} className="simple-form">
                {/* Image Upload Area Component */}
                <ImageUploadArea
                    images={imageUpload.images}
                    hasText={hasText}
                    loading={processing.loading}
                    dragActive={imageUpload.dragActive}
                    onDragEnter={imageUpload.handleDrag}
                    onDragLeave={imageUpload.handleDrag}
                    onDragOver={imageUpload.handleDrag}
                    onDrop={imageUpload.handleDrop}
                    onImageChange={imageUpload.handleImageChange}
                    onRemoveImage={imageUpload.removeImage}
                    onContextMenu={(e) => clipboard.handleContextMenu(e, hasText)}
                    contextMenu={clipboard.contextMenu}
                    onPasteFromClipboard={handlePasteFromClipboard}
                />

                {/* Text Input Field Component */}
                <TextInputField
                    text={text}
                    hasImages={imageUpload.hasImages}
                    loading={processing.loading}
                    onChange={(e) => {
                        const v = e.target.value
                        setText(v)
                        if (v.trim().length > 0) {
                            imageUpload.clearImages()
                        }
                    }}
                />

                {/* Form Actions Component */}
                <FormActions
                    hasInput={hasInput}
                    loading={processing.loading}
                    onClear={handleClear}
                />
            </form>
        </div>
    )
}
