import { useState } from 'react'
import { Routes, Route, Link, useLocation } from 'react-router-dom'
import './App.css'
import About from './pages/About'
import Home from './pages/Home'
import NotFound from './pages/NotFound'

function App() {
  const location = useLocation()

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">Easy ICS</h1>
          <p className="app-subtitle">Simple and easy-to-use calendar file processing tool</p>
        </div>
      </header>

      <nav className="app-nav">
        <div className="nav-content">
          <Link to='/' className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
            Home
          </Link>
          <Link to='/about' className={`nav-link ${location.pathname === '/about' ? 'active' : ''}`}>
            About
          </Link>
        </div>
      </nav>

      <main className="app-main">
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/about' element={<About />} />
          <Route path='*' element={<NotFound />} />
        </Routes>
      </main>

      <footer className="app-footer">
        <p>&copy; 2024 Easy ICS. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default App
