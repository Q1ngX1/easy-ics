import { useState } from 'react'
import { Routes, Route, Link, useLocation } from 'react-router-dom'
import './App.css'
import About from './pages/About'
import Home from './pages/Home'

function App() {
  const location = useLocation()

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">Easy ICS</h1>
          <p className="app-subtitle">简单易用的日历文件处理工具</p>
        </div>
      </header>

      <nav className="app-nav">
        <div className="nav-content">
          <Link to='/' className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
            <span className="nav-icon">🏠</span>
            首页
          </Link>
          <Link to='/about' className={`nav-link ${location.pathname === '/about' ? 'active' : ''}`}>
            <span className="nav-icon">ℹ️</span>
            关于
          </Link>
        </div>
      </nav>

      <main className="app-main">
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/about' element={<About />} />
        </Routes>
      </main>

      <footer className="app-footer">
        <p>&copy; 2024 Easy ICS. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default App
