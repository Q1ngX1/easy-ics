import { useState, useEffect, useRef} from 'react'
import '../styles/pages.css'
import { uploadImage, uploadText, downloadICS, triggerDownload } from '../services/apiService'

export default function Home() {
    const [image, setImage] = useState(null)
    const [text, setText] = useState('')
    const [dragActive, setDragActive] = useState(false)
    const [contextMenu, setContextMenu] = useState(null) // {x, y}
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null) // parsed events
    const [error, setError] = useState(null)
    const fileInputRef = useRef(null)

    const handleImageChange = (e) => {
        const file = e.target.files?.[0]
        if (file && file.type.startsWith('image/')) {
            setImage(file)
            setText('')
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

    const handleClear = (e) => {
        setError(null)
        setImage(null)
        setText('')
        setResult(null)
        if (fileInputRef.current) {
            fileInputRef.current.value = ''
        }
    }

    const handleStart = async (e) => {
        e.preventDefault()
        setError(null)
        setResult(null)
        setLoading(true)

        try {
            let events = []
            // Upload image and extract text via OCR
            if (image) {
                const uploadRes = await uploadImage(image)
                if (!uploadRes.success) {
                    throw new Error(uploadRes.message || 'Image upload failed')
                }
                // If text extracted, parse it to events
                if (uploadRes.text && uploadRes.text.trim().length > 0) {
                    const parseRes = await uploadText(uploadRes.text)
                    if (!parseRes.success) {
                        throw new Error(parseRes.message || 'Text parsing failed')
                    }
                    events = parseRes.events || []
                } else {
                    setError('No text detected in the image. Please try a clearer image.')
                    setLoading(false)
                    return
                }
            }
            // Parse text directly
            else if (text) {
                const parseRes = await uploadText(text)
                if (!parseRes.success) {
                    throw new Error(parseRes.message || 'Text parsing failed')
                }
                events = parseRes.events || []
            } else {
                throw new Error('No input provided')
            }

            if (!events || events.length === 0) {
                setError('No events were parsed from the input. Please try different content.')
                setLoading(false)
                return
            }

            setResult(events)
        } catch (err) {
            console.error('Processing error:', err)
            setError(err.message || 'An error occurred during processing')
        } finally {
            setLoading(false)
        }
    }

    const handleDownloadICS = async () => {
        if (!result || result.length === 0) return

        setLoading(true)
        setError(null)
        try {
            const icsBlob = await downloadICS(result)
            triggerDownload(icsBlob, 'calendar.ics')
        } catch (err) {
            console.error('Download error:', err)
            setError(err.message || 'Failed to download ICS file')
        } finally {
            setLoading(false)
        }
    }

    const hasImage = !!image
    const hasText = text.trim().length > 0

    // handle paste events so user can paste an image from clipboard (Ctrl+V)
    useEffect(() => {
        const onPaste = (e) => {
            try {
                const items = e.clipboardData?.items
                if (!items) return

                for (let i = 0; i < items.length; i++) {
                    const item = items[i]
                    if (item.type && item.type.startsWith('image/')) {
                        const file = item.getAsFile()
                        if (file) {
                            setImage(file)
                            // clear text to keep inputs exclusive
                            setText('')
                            // prevent default so the image isn't inserted into editable areas
                            e.preventDefault()
                            break
                        }
                    }
                }
            } catch (err) {
                // ignore paste errors
                console.error('paste handling error', err)
            }
        }

        window.addEventListener('paste', onPaste)
        return () => window.removeEventListener('paste', onPaste)
    }, [])

    // hide context menu when clicking elsewhere
    useEffect(() => {
        const onClick = () => setContextMenu(null)
        window.addEventListener('click', onClick)
        return () => window.removeEventListener('click', onClick)
    }, [])

    const handleContextMenu = (e) => {
        // only show custom menu when image input is enabled
        if (text.trim().length > 0) return
        e.preventDefault()
        setContextMenu({ x: e.clientX + 2, y: e.clientY + 2 })
    }

    const pasteFromClipboard = async () => {
        setContextMenu(null)
        try {
            if (navigator.clipboard && navigator.clipboard.read) {
                const items = await navigator.clipboard.read()
                for (const item of items) {
                    for (const type of item.types) {
                        if (type.startsWith('image/')) {
                            const blob = await item.getType(type)
                            const file = new File([blob], 'pasted-image.' + type.split('/')[1], { type: blob.type })
                            setImage(file)
                            setText('')
                            return
                        }
                    }
                }
                alert('No image found in clipboard.')
            } else {
                // Fallback: instruct user to use keyboard paste
                alert('Paste from clipboard is not supported in this browser via right-click. Please focus the page and press Ctrl+V to paste the image.')
            }
        } catch (err) {
            console.error('clipboard.read error', err)
            alert('Unable to read clipboard. Please try pressing Ctrl+V or check browser permissions.')
        }
    }

    return (
        <div className="page-content home-form">
            <h1>Get Started</h1>

            {/* Error message */}
            {error && (
                <div className="message-box error-box">
                    <span className="message-icon">✘</span>
                    <p>{error}</p>
                    <button 
                        type="button" 
                        className="message-close" 
                        onClick={() => setError(null)}
                    >
                        ✕
                    </button>
                </div>
            )}

            {/* Success message with result preview and download */}
            {result && result.length > 0 && (
                <div className="message-box success-box">
                    <span className="message-icon">\u2713</span>
                    <div className="result-content">
                        <p>Successfully parsed <strong>{result.length}</strong> event(s)!</p>
                        <button 
                            type="button" 
                            className="cta-button secondary" 
                            onClick={handleDownloadICS}
                            disabled={loading}
                        >
                            {loading ? 'Downloading...' : '⬇ Download ICS'}
                        </button>
                    </div>
                    <button 
                        type="button" 
                        className="message-close" 
                        onClick={() => {
                            setResult(null)
                            setImage(null)
                            setText('')
                        }}
                    >
                        ✕
                    </button>
                </div>
            )}

            <form onSubmit={handleStart} className="simple-form">
                {/* Image drag and drop area */}
                <div
                    className={`form-row drag-drop-area ${dragActive ? 'active' : ''} ${hasText ? 'disabled' : ''}`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    onContextMenu={handleContextMenu}
                >
                    <input
                        ref={fileInputRef}
                        type="file"
                        id="image-input"
                        accept="image/*"
                        onChange={handleImageChange}
                        className="file-input"
                        disabled={hasText || loading}
                    />
                    <label htmlFor="image-input" className="drag-drop-label">
                        {image ? (
                            <>
                                <span className="file-name">✓ {image.name}</span>
                            </>
                        ) : (
                            <>
                                <span className="drag-drop-icon">📁</span>
                                <span className="drag-drop-text">{hasText ? 'Text input already selected' : 'Drag image here, paste (Ctrl+V/Command+V) or click to select'}</span>
                            </>
                        )}
                    </label>

                    {contextMenu && (
                        <div className="context-menu" style={{ left: contextMenu.x, top: contextMenu.y }}>
                            <div className="context-menu-item" onClick={pasteFromClipboard}>Paste image</div>
                        </div>
                    )}
                </div>

                {/* Text input field */}
                <label className="form-row text-input-label">
                    <span className="label-text">Enter text or description</span>
                    <textarea
                        value={text}
                        onChange={(e) => {
                            const v = e.target.value
                            setText(v)
                            // if user starts typing text, clear any selected image to enforce exclusivity
                            if (v.trim().length > 0) setImage(null)
                        }}
                        placeholder="Enter the text you want to recognize, dates, or any related information..."
                        className={`text-input ${hasImage ? 'disabled' : ''}`}
                        rows="4"
                        disabled={hasImage || loading}
                    />
                </label>

                {/* Start and Clear button */}
                <div className="form-row button-row">
                    <button 
                        type="submit" 
                        className="cta-button" 
                        disabled={(!hasImage && !hasText) || loading}
                    >
                        {loading ? 'Processing...' : 'Convert'}
                    </button>
                    <button 
                        type="button"
                        className="cta-button secondary"
                        onClick={handleClear}
                        disabled={loading}
                        aria-label="Clear all inputs and results"
                    >
                        Clear all
                    </button>
                </div>

            </form>
        </div>
    )
}