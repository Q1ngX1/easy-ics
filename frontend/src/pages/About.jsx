import '../styles/pages.css'

export default function About(){
    return (
        <div className="page-content">
            <h1>关于 Easy ICS</h1>
            
            <div className="about-section">
                <h2>项目简介</h2>
                <p>
                    Easy ICS 是一个强大而简洁的日历文件处理工具。它提供了一套完整的解决方案，
                    帮助用户轻松处理 ICS 日历文件，支持 OCR 识别和智能内容解析。
                </p>
            </div>

            <div className="about-section">
                <h2>核心功能</h2>
                <ul className="feature-list">
                    <li>📄 <strong>ICS 文件处理</strong> - 支持读取和处理标准 ICS 格式文件</li>
                    <li>🖼️ <strong>OCR 图片识别</strong> - 使用先进的 OCR 技术识别图片中的日历信息</li>
                    <li>🤖 <strong>智能解析</strong> - 自动解析和提取关键日期和事件信息</li>
                    <li>🔄 <strong>数据转换</strong> - 支持多种日历格式之间的转换</li>
                </ul>
            </div>

            <div className="about-section">
                <h2>技术栈</h2>
                <div className="tech-stack">
                    <span className="tech-badge">React</span>
                    <span className="tech-badge">Python</span>
                    <span className="tech-badge">OCR</span>
                    <span className="tech-badge">ICS Parser</span>
                </div>
            </div>

            <div className="about-section">
                <h2>联系我们</h2>
                <p>
                    如有任何问题或建议，欢迎通过以下方式联系我们：
                </p>
                <div className="contact-info">
                    <p>📧 Email: info@easyics.com</p>
                    <p>🐙 GitHub: <a href="#" className="link">github.com/easyics</a></p>
                </div>
            </div>
        </div>
    )
}