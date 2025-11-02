import { Link } from 'react-router-dom'
import '../styles/pages.css'

export default function NotFound() {
    return (
        <div className="page-content not-found">
            <div className="not-found-container">
                <h1 className="not-found-code">404</h1>
                <h2 className="not-found-title">Page Not Found</h2>
                <p className="not-found-description">
                    Sorry, the page you are looking for doesn't exist or has been moved.
                </p>
                <div className="not-found-actions">
                    <Link to="/" className="not-found-button">
                        ← Back to Home
                    </Link>
                    <a 
                        href="https://www.youtube.com/watch?v=dQw4w9WgXcQ" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="not-found-button secondary"
                    >
                        Help?
                    </a>
                </div>
            </div>
        </div>
    )
}
