import { useState } from 'react'
import '../styles/pages.css'

export default function Home() {
    const [image, setImage] = useState(null)
    const [text, setText] = useState('')
    const [dragActive, setDragActive] = useState(false)

    const handleImageChange = (e) => {
        const file = e.target.files?.[0]
        if (file && file.type.startsWith('image/')) {
            setImage(file)
        }
    }

    const handleDrag = (e) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true)
        } else if (e.type === 'dragleave') {
            setDragActive(false)
        }
    }

    const handleDrop = (e) => {
        e.preventDefault()
        e.stopPropagation()
        setDragActive(false)

        const files = e.dataTransfer.files
        if (files && files.length > 0) {
            const file = files[0]
            if (file.type.startsWith('image/')) {
                setImage(file)
            }
        }
    }

    const handleStart = (e) => {
        e.preventDefault()
        // Placeholder: will be replaced with backend API call
        console.log('start', { image, text })
        alert('Processing started (in development)')
    }

    const hasImage = !!image
    const hasText = text.trim().length > 0

    return (
        <div className="page-content home-form">
            <h1>Get Started</h1>

            <form onSubmit={handleStart} className="simple-form">
                {/* Image drag and drop area */}
                <div
                    className={`form-row drag-drop-area ${dragActive ? 'active' : ''} ${hasText ? 'disabled' : ''}`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                >
                    <input
                        type="file"
                        id="image-input"
                        accept="image/*"
                        onChange={handleImageChange}
                        className="file-input"
                        disabled={hasText}
                    />
                    <label htmlFor="image-input" className="drag-drop-label">
                        {image ? (
                            <>
                                <span className="file-name">✓ {image.name}</span>
                            </>
                        ) : (
                            <>
                                <span className="drag-drop-icon">📁</span>
                                <span className="drag-drop-text">{hasText ? 'Text input already selected' : 'Drag image here or click to select'}</span>
                            </>
                        )}
                    </label>
                </div>

                {/* Text input field */}
                <label className="form-row text-input-label">
                    <span className="label-text">Enter text or description</span>
                    <textarea
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="Enter the text you want to recognize, dates, or any related information..."
                        className={`text-input ${hasImage ? 'disabled' : ''}`}
                        rows="4"
                        disabled={hasImage}
                    />
                </label>

                {/* Start button */}
                <div className="form-row button-row">
                    <button type="submit" className="cta-button" disabled={!hasImage && !hasText}>Start</button>
                </div>
            </form>
        </div>
    )
}