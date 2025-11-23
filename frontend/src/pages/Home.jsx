import '../styles/pages.css'
import '../styles/checkbox.css'
import '../styles/layout.css'
import OCRPanel from '../sections/OCRPanel'
import EventBuilder from '../sections/EventBuilder'

export default function Home() {
    return (
        <div className="home-container">
            {/* Left Column - OCR Panel */}
            <div className="home-column left-column">
                <OCRPanel />
            </div>

            {/* Right Column - Event Builder */}
            <div className="home-column right-column">
                <EventBuilder />
            </div>
        </div>
    )
}