import { useState } from "react";
import api from "../api";
import "./AuthPage.css";

function AuthPage({ setToken }) {
    // Quản lý bảo mật và đăng nhập
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isLoginView, setIsLoginView] = useState(true);

    // --- AUTHENTICATION ---
  const handleAuth = async (e) => {
    e.preventDefault();
    try {
      if (isLoginView) { // if isLoginView === true 
        const res = await api.post("token/", { username, password }); // gọi POST tới token/ 
        localStorage.setItem("access", res.data.access); // nếu trả về thành công, lưu cả "access" và "refresh" vào localStorage
        localStorage.setItem("refresh", res.data.refresh);
        setToken(res.data.access); // cập nhật setToken
      } else { // isLoginView === false
        await api.post("user/register/", { username, password }); // gọi POST tới register
        alert("Đăng ký thành công! Vui lòng đăng nhập."); // đăng ký xong thì chuyển về màn hình đăng nhập
        setIsLoginView(true); // set isLoginView === true để người dùng Login
      }
    } catch (error) {
      alert("Có lỗi xảy ra. Kiểm tra lại thông tin!");

      console.log("Status:", error.response?.status);
      console.log("Detail:", error.response?.data);
      alert(JSON.stringify(error.response?.data));
    }
  };

    return (
      <>
      <section className="container">
        <meta charSet="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            {/* Google Fonts */}
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
            <link
              href="https://fonts.googleapis.com/css2?family=Bungee&family=Inter:wght@400&display=swap"
              rel="stylesheet"
            />
          <div style={{ textAlign: "center", marginTop: "50px" }}>
              <h2 className="login-title" >{isLoginView ? "Đăng Nhập" : "Đăng Ký"}</h2>
              <form onSubmit={handleAuth}>
                  <input className="login-input" type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
                  <br /><br />
                  <input className="login-input" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                  <br /><br />

                  <button className="login-button" type="submit">{isLoginView ? "Login" : "Register"}</button>
              </form>
              <p className="register-login" onClick={() => setIsLoginView(!isLoginView)} style={{ color: "blue", cursor: "pointer" }}>
                  {isLoginView ? "Chưa có tài khoản? Đăng ký ngay" : "Đã có tài khoản? Đăng nhập"}
              </p>
          </div>
        </section>
      </>
    );
}

export default AuthPage;