import { useRef } from 'react'
import PropTypes from 'prop-types'

export default function ImageUploadArea({
    images,
    hasText,
    loading,
    dragActive,
    onDragEnter,
    onDragLeave,
    onDragOver,
    onDrop,
    onImageChange,
    onRemoveImage,
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
                multiple
                onChange={(e) => {
                    const files = Array.from(e.target.files || [])
                    const validImages = files.filter((file) => file.type.startsWith('image/'))
                    if (validImages.length > 0) {
                        onImageChange(validImages)
                    }
                }}
                className="file-input"
                disabled={hasText || loading}
            />
            <label htmlFor="image-input" className="drag-drop-label">
                {images.length > 0 ? (
                    <>
                        <span className="file-count">✓ {images.length} image{images.length !== 1 ? 's' : ''} selected</span>
                        <div className="image-list">
                            {images.map((img, index) => (
                                <div key={index} className="image-item">
                                    <span className="image-name">{img.name}</span>
                                    <button
                                        type="button"
                                        className="remove-image-btn"
                                        onClick={(e) => {
                                            e.stopPropagation()
                                            onRemoveImage(index)
                                        }}
                                        title="Remove image"
                                    >
                                        ✕
                                    </button>
                                </div>
                            ))}
                        </div>
                    </>
                ) : (
                    <>
                        <span className="drag-drop-icon">📁</span>
                        <span className="drag-drop-text">
                            {hasText ? 'Text input already selected' : 'Drag images here, paste (Ctrl+V/Command+V) or click to select'}
                        </span>
                    </>
                )}
            </label>

            {contextMenu && (
                <div className="context-menu" style={{ left: contextMenu.x, top: contextMenu.y }}>
                    <div className="context-menu-item" onClick={onPasteFromClipboard}>
                        Paste image(s)
                    </div>
                </div>
            )}
        </div>
    )
}

ImageUploadArea.propTypes = {
    images: PropTypes.arrayOf(PropTypes.object).isRequired,
    hasText: PropTypes.bool.isRequired,
    loading: PropTypes.bool.isRequired,
    dragActive: PropTypes.bool.isRequired,
    onDragEnter: PropTypes.func.isRequired,
    onDragLeave: PropTypes.func.isRequired,
    onDragOver: PropTypes.func.isRequired,
    onDrop: PropTypes.func.isRequired,
    onImageChange: PropTypes.func.isRequired,
    onRemoveImage: PropTypes.func.isRequired,
    onContextMenu: PropTypes.func.isRequired,
    contextMenu: PropTypes.object,
    onPasteFromClipboard: PropTypes.func.isRequired,
}
