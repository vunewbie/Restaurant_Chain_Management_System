import { useState } from "react";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const BACKEND_URL = "http://127.0.0.1:8000"; // Thay đổi nếu backend chạy ở host khác

  // Xử lý đăng nhập bằng username/password
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${BACKEND_URL}/api/token/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      if (response.ok) {
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);
        alert("Đăng nhập thành công!");
        window.location.href = "/";
      } else {
        alert("Đăng nhập thất bại: " + data.detail);
      }
    } catch (error) {
      console.error("Lỗi khi đăng nhập:", error);
      alert("Đăng nhập không thành công!");
    }
  };

  // Xử lý đăng nhập bằng Google OAuth2
  const handleGoogleLogin = () => {
    window.location.href = `${BACKEND_URL}/auth/login/google-oauth2/`;
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 shadow-md rounded-lg w-96">
        <h2 className="text-xl font-semibold mb-4 text-center">Đăng nhập</h2>

        {/* Form đăng nhập bằng username/password */}
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <label className="block text-gray-700">Tên đăng nhập</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-blue-300"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Mật khẩu</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-blue-300"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600"
          >
            Đăng nhập
          </button>
        </form>

        {/* Hoặc đăng nhập bằng Google */}
        <div className="mt-4 text-center">
          <button
            onClick={handleGoogleLogin}
            className="w-full bg-red-500 text-white py-2 px-4 rounded-lg hover:bg-red-600 flex items-center justify-center"
          >
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png"
              alt="Google Logo"
              className="w-5 h-5 mr-2"
            />
            Đăng nhập với Google
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;
