import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import App from './pages/Lista'
import Cadastro from './pages/Cadastro'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/cadastrar" element={<Cadastro />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)