import { useState } from 'react'
import { Routes, Route, Link} from 'react-router-dom'
import './App.css'
import About from './pages/About'
import Home from './pages/Home'

function App() {

  return (
    <>
      <div>
        <nav>
          <Link to='/'>Home Page</Link>
          <Link to='/about'>About Page</Link>
        </nav>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/about' element={<About />} />
        </Routes>
      </div>
    </>
  )
}

export default App
