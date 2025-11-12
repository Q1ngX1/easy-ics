import { useState } from 'react'
import '../styles/pages.css'

export default function About(){
    const [copiedEmail, setCopiedEmail] = useState(null)
    
    const handleCopyEmail = (email) => {
        navigator.clipboard.writeText(email)
        setCopiedEmail(email)
        setTimeout(() => setCopiedEmail(null), 2000)
    }

    return (
        <div className="page-content">
            <h1>About Easy ICS</h1>
            
            <div className="about-section">
                <h2>Project Overview</h2>
                <p>
                    Easy ICS is a lightweight application that converts schedule information from images and natural language text into standard ICS (iCalendar) file(s), 
                    eliminating the hassle of manually entering screenshots or paper schedules into your calendar one by one. 
                    It supports extracting text from PNG/JPG/JPEG/BMP/TIFF images, then parsing event titles, dates/times, locations, 
                    and descriptions to generate fully RFC 5545-compliant .ics files. These files import seamlessly into Google Calendar, Outlook, Apple Calendar, and other platforms. 
                    It also directly parses schedule information from free-form text.
                     Future plans encompass enhanced text parsing, integration testing, Dockerization, performance optimization, 
                     and adding recurring events, multi-user calendar export, authentication, event history, and mobile apps in v1.0.0.
                      The project is licensed under MIT, open-source, cross-platform, and privacy-friendly. 
                      It is suitable for direct personal use and easily integrates into existing systems.
                </p>
            </div>

            <div className="about-section">
                <h2>Core Features</h2>
                <ul className="feature-list">
                    <li>📄 <strong>ICS File Processing</strong> - Support for reading and processing standard ICS format files</li>
                    <li>🖼️ <strong>OCR Image Recognition</strong> - Advanced OCR technology to recognize calendar information from images</li>
                    <li>🤖 <strong>Intelligent Parsing</strong> - Automatically parse and extract key dates and event information</li>
                    <li>🔄 <strong>Data Conversion</strong> - Support for conversion between multiple calendar formats</li>
                </ul>
            </div>
            <div className="about-section">
                <h2>Tech Stack</h2>
                <div className="tech-stack">
                    <span className="tech-badge">React</span>
                    <span className="tech-badge">Python</span>
                    <span className="tech-badge">OCR</span>
                    <span className="tech-badge">ICS Parser</span>
                </div>
            </div>

            <div className="about-section">
                <h2>Contact Us</h2>
                <p>
                    If you have any questions or suggestions, feel free to reach out to us:
                </p>
                <div className="contact-info">
                    <p>  GitHub: <a href="https://github.com/Q1ngX1/easy-ics" className="link">github.com/easyics</a></p>
                    <p style={{ cursor: 'pointer' }} onClick={() => handleCopyEmail('zgeng5@illinois.edu')} className="copy-email">
                        Email: zgeng5@illinois.edu {copiedEmail === 'zgeng5@illinois.edu' && <span className="copy-hint"> ✓ Copied</span>}
                    </p>
                    <p style={{ cursor: 'pointer' }} onClick={() => handleCopyEmail('zanshuhan2029@ucla.edu')} className="copy-email">
                        Email: zanshuhan2029@ucla.edu {copiedEmail === 'zanshuhan2029@ucla.edu' && <span className="copy-hint"> ✓ Copied</span>}
                    </p>       
                </div>
            </div>
        </div>
    )
}