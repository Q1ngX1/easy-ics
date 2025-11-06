import { useState, useEffect } from 'react'
import '../styles/pages.css'

export default function Home() {
    const [image, setImage] = useState(null)
    const [text, setText] = useState('')
    const [dragActive, setDragActive] = useState(false)
    const [contextMenu, setContextMenu] = useState(null) // {x, y}

    const handleImageChange = (e) => {
        const file = e.target.files?.[0]
        if (file && file.type.startsWith('image/')) {
            setImage(file)
            // clear text when an image is selected to enforce one-of-two input rule
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

    const handleStart = (e) => {
        e.preventDefault()
        // Placeholder: will be replaced with backend API call
        console.log('start', { image, text })
        alert('Processing started (in development)')
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
                        disabled={hasImage}
                    />
                </label>

                {/* Start button */}
                <div className="form-row button-row">
                    <button type="submit" className="cta-button" disabled={!hasImage && !hasText}>Convert</button>
                </div>
            </form>
        </div>
    )
}