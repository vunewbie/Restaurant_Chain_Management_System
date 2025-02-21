import React from "react";

const ForgotPassword = () => {

    return (
        <div></div>
    )
};

export default ForgotPassword;

// import React, { useState, useEffect } from "react";
// import { Link, useNavigate } from "react-router-dom";
// import "./LogIn.css";
// import axios from "axios";

// const LogIn = () => {
//   const [username, setUsername] = useState("");   // Lưu trữ username/Email/SĐT
//   const [password, setPassword] = useState("");   // Lưu trữ mật khẩu
//   const [error, setError] = useState("");         // Lưu thông báo lỗi
//   const [rememberMe, setRememberMe] = useState(false); // Trạng thái checkbox "Nhớ tài khoản"
//   const navigate = useNavigate();

//   // Thêm class "login-page" cho body
//   useEffect(() => {
//     document.body.classList.add("login-page");
//     return () => document.body.classList.remove("login-page");
//   }, []);

//   // Xử lý form submit
//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     // Kiểm tra nếu người dùng chưa nhập gì
//     if (username.trim() === "" || password.trim() === "") {
//       setError("Vui lòng điền thông tin đăng nhập.");
//       return;
//     }

//     try {
//       // Gọi API đăng nhập
//       const response = await axios.post("http://127.0.0.1:8000/api/accounts/token", {
//         username: username,
//         password: password,
//       });

//       // Nếu đăng nhập thành công, lưu token vào localStorage
//       const { access, refresh } = response.data;
//       localStorage.setItem("access", access);
//       localStorage.setItem("refresh", refresh);

//       // Nếu người dùng chọn "Nhớ tài khoản", lưu username
//       if (rememberMe) {
//         localStorage.setItem("rememberedUsername", username);
//       } else {
//         localStorage.removeItem("rememberedUsername");
//       }

//       // Điều hướng sang trang Homepage
//       navigate("/homepage");
//     } catch (err) {
//       if (err.response && err.response.data && err.response.data.message) {
//         setError(err.response.data.message);
//       } else {
//         setError("Đã xảy ra lỗi khi đăng nhập. Vui lòng thử lại.");
//       }
//     }
//   };

//   // Khi trang tải lại, tự động điền username nếu có trong localStorage
//   useEffect(() => {
//     const rememberedUsername = localStorage.getItem("rememberedUsername");
//     if (rememberedUsername) {
//       setUsername(rememberedUsername);
//       setRememberMe(true);
//     }
//   }, []);

//   return (
//     <div className="login-page">
//         <div className="wrapper">
//             <form onSubmit={handleSubmit}>
//                 <h2>Đăng Nhập</h2>
//                 <div className="input-field">
//                 <input
//                     type="text"
//                     required
//                     value={username}
//                     onChange={(e) => setUsername(e.target.value)}
//                 />
//                 <label>Username hoặc Email hoặc SĐT</label>
//                 </div>
//                 <div className="input-field">
//                 <input
//                     type="password"
//                     required
//                     value={password}
//                     onChange={(e) => setPassword(e.target.value)}
//                 />
//                 <label>Mật Khẩu</label>
//                 </div>
//                 <div className="forget">
//                 <label htmlFor="remember">
//                     <input
//                     type="checkbox"
//                     id="remember"
//                     checked={rememberMe}
//                     onChange={(e) => setRememberMe(e.target.checked)}
//                     />
//                     <p className="remember-me">Nhớ tài khoản</p>
//                 </label>
//                 <Link to="/forgot-password">Quên mật khẩu?</Link>
//                 </div>
//                 {error && <p className="error-message">{error}</p>}
//                 <button type="submit">Đăng Nhập</button>
//                 <div className="register">
//                 <p>
//                     Chưa có tài khoản?{" "}
//                     <Link to="/customers/register">Đăng Ký</Link>
//                 </p>
//                 </div>
//             </form>
//         </div>
//     </div>
//   );
// };

// export default LogIn;
