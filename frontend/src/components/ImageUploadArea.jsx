import { useRef } from 'react'
import PropTypes from 'prop-types'

export default function ImageUploadArea({
    image,
    hasText,
    loading,
    dragActive,
    onDragEnter,
    onDragLeave,
    onDragOver,
    onDrop,
    onImageChange,
    onContextMenu,
    contextMenu,
    onPasteFromClipboard,
}) {
    const fileInputRef = useRef(null)

    return (
        <div
            className={`form-row drag-drop-area ${dragActive ? 'active' : ''} ${hasText ? 'disabled' : ''}`}
            onDragEnter={onDragEnter}
            onDragLeave={onDragLeave}
            onDragOver={onDragOver}
            onDrop={onDrop}
            onContextMenu={onContextMenu}
        >
            <input
                ref={fileInputRef}
                type="file"
                id="image-input"
                accept="image/*"
                onChange={(e) => {
                    const file = e.target.files?.[0]
                    if (file && file.type.startsWith('image/')) {
                        onImageChange(file)
                    }
                }}
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
                        <span className="drag-drop-text">
                            {hasText ? 'Text input already selected' : 'Drag image here, paste (Ctrl+V/Command+V) or click to select'}
                        </span>
                    </>
                )}
            </label>

            {contextMenu && (
                <div className="context-menu" style={{ left: contextMenu.x, top: contextMenu.y }}>
                    <div className="context-menu-item" onClick={onPasteFromClipboard}>
                        Paste image
                    </div>
                </div>
            )}
        </div>
    )
}

ImageUploadArea.propTypes = {
    image: PropTypes.object,
    hasText: PropTypes.bool.isRequired,
    loading: PropTypes.bool.isRequired,
    dragActive: PropTypes.bool.isRequired,
    onDragEnter: PropTypes.func.isRequired,
    onDragLeave: PropTypes.func.isRequired,
    onDragOver: PropTypes.func.isRequired,
    onDrop: PropTypes.func.isRequired,
    onImageChange: PropTypes.func.isRequired,
    onContextMenu: PropTypes.func.isRequired,
    contextMenu: PropTypes.object,
    onPasteFromClipboard: PropTypes.func.isRequired,
}
