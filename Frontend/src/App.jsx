import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import api from "./api";
import AuthPage from "./views/AuthPage";
import TodoPage from "./views/TodoPage";
import "./App.css";

// Hàm Xác thực người dùng (Auth) và Toàn bộ vòng đời CRUD của các Task.
function App() {
  // Quản lý bảo mật và đăng nhập
  const [token, setToken] = useState(localStorage.getItem("access"));

  const logout = () => { // Hàm logout, xóa sạch mọi thứ trong trình duyệt và đưa token về null
    localStorage.clear();
    setToken(null);
  };

  // --- RENDER ---
if (!token) {
  return <AuthPage setToken={setToken}/>;
  }
  return <TodoPage token={token} onLogout={logout} />;
}

export default App;