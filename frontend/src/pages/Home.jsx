import '../styles/pages.css'

export default function Home(){
    return (
        <div className="page-content">
            <div className="hero-section">
                <h1>欢迎使用 Easy ICS</h1>
                <p className="hero-subtitle">轻松处理日历文件，支持 OCR 识别和智能解析</p>
            </div>

            <div className="features-grid">
                <div className="feature-card">
                    <div className="feature-icon">📅</div>
                    <h3>日历管理</h3>
                    <p>支持 ICS 文件的读取和处理，轻松管理你的日程</p>
                </div>

                <div className="feature-card">
                    <div className="feature-icon">🔍</div>
                    <h3>OCR 识别</h3>
                    <p>强大的 OCR 功能，识别图片中的日历信息</p>
                </div>

                <div className="feature-card">
                    <div className="feature-icon">⚡</div>
                    <h3>智能解析</h3>
                    <p>智能解析日历内容，自动提取关键信息</p>
                </div>

                <div className="feature-card">
                    <div className="feature-icon">🎨</div>
                    <h3>简洁界面</h3>
                    <p>清爽易用的用户界面设计，上手即用</p>
                </div>
            </div>

            <div className="cta-section">
                <button className="cta-button">开始使用</button>
                <button className="cta-button secondary">了解更多</button>
            </div>
        </div>
    )
}