import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import "./CustomerRegister.css";

const CustomerRegister = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    confirmPassword: "",
    email: "",
    phone_number: "",
    citizen_id: "",
    full_name: "",
    date_of_birth: "",
    gender: "M",
    avatar: null, 
  });
  const [error, setError] = useState("");

  useEffect(() => {
    document.body.classList.add("register-page");
    return () => document.body.classList.remove("register-page");
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    // gán lỗi ngay khi thay đổi giá trị nếu có bằng validateField
    setError({ ...error, [e.target.name]: "" });
  };

  const validateForm = () => {
    const newErrors = {};

    // Nếu tên đăng nhập không đủ 6 ký tự thì báo lỗi nếu không thì kiểm tra tên đăng nhập có ký tự khoảng trắng hay không
    if (formData.username.length < 6) {
      newErrors.username = "Tên đăng nhập phải có ít nhất 6 ký tự.";
    } else if (formData.username.includes(" ")) {
      newErrors.username = "Tên đăng nhập không được chứa khoảng trắng.";
    }

    // Kiểm tra mật khẩu có ít nhất 8 ký tự
    if (formData.password.length < 8) {
      newErrors.password = "Mật khẩu phải có ít nhất 8 ký tự.";
    }

    // Kiểm tra mật khẩu nhập lại có trùng với mật khẩu không
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Mật khẩu nhập lại không khớp.";
    }

    // Kiểm tra email có đúng định dạng không
    if (!formData.email.includes("@")) {
      newErrors.email = "Email không hợp lệ.";
    }

    // Kiểm tra số điện thoại có bắt đầu bằng số 0 không, có đúng 10 số không, có chứa ký tự khác số không chỉ báo ra lỗi đầu tiên
    if (!formData.phone_number.startsWith("0")) {
      newErrors.phone_number = "Số điện thoại phải bắt đầu bằng số 0.";
    } else if(formData.phone_number.length !== 10) {
      newErrors.phone_number = "Số điện thoại phải có 10 số.";
    } else if (isNaN(formData.phone_number)) {
      newErrors.phone_number = "Số điện thoại chỉ được chứa số.";
    }

    // Kiểm tra căn cước công dân có đúng 12 số không, có chứa ký tự khác số không chỉ báo ra lỗi đầu tiên
    if (formData.citizen_id.length !== 12) {
      newErrors.citizen_id = "Căn cước công dân phải có 12 số.";
    } else if (isNaN(formData.citizen_id)) {
      newErrors.citizen_id = "Căn cước công dân chỉ được chứa số.";
    }

    // Kiểm tra họ tên có chứa ký tự khác chữ cái không
    if (!/^[a-zA-Z\s]*$/.test(formData.full_name)) {
      newErrors.full_name = "Họ tên chỉ được chứa chữ cái.";
    }

    // Kiểm tra ngày sinh có đúng định dạng không
    if (isNaN(Date.parse(formData.date_of_birth))) {
      newErrors.date_of_birth = "Ngày sinh không hợp lệ.";
    }

    setError(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    const requestData = { ...formData };

    if(!requestData.avatar) {
      delete requestData.avatar;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/accounts/customers", {
        user: requestData,
      });
      console.log(response.data);
      

    if (response.data.message === "OTP has been sent to your email") {
      localStorage.setItem("username", formData.username);
      localStorage.setItem("mode", "register");
      navigate("/verify-otp");
    }
  } catch (error) {
    if (error.response && error.response.data.user) {
      const errors = error.response?.data?.user || {}; // Nếu không có lỗi thì trả về đối tượng rỗng
      const errorMessages = {};

      Object.keys(errors).forEach((key) => {
      errorMessages[key] = errors[key]?.[0] || ''; // Lấy thông báo lỗi đầu tiên nếu tồn tại
      });
      setErrors(errorMessages);
    } else {
      setError("Đã xảy ra lỗi. Vui lòng thử lại.");
    }
  }
};

  return (
    <div className="register-page">
      <div className="register-wrapper">
        <div className="container">
          <div className="title">Đăng Ký</div>
          <div className="content">
            <form onSubmit={handleSubmit}>
              <div className="user-details">
                <div className="input-box">
                  <span className="details">Tên Đăng Nhập</span>
                  <input 
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    placeholder="Nhập tên đăng nhập" 
                    required
                  />
                  {error.username && <span className="error-text">{error.username}</span>}
                </div>
                <div className="input-box">
                  <span className="details">Số Điện Thoại</span>
                  <input 
                    type="text"
                    name="phone_number"
                    value={formData.phone_number}
                    onChange={handleChange} 
                    placeholder="Nhập số điện thoại" 
                    required 
                  />
                  {error.phone_number && <span className="error-text">{error.phone_number}</span>}
                </div>
                <div className="input-box">
                  <span className="details">Email</span>
                  <input 
                    type="text"
                    name="email"
                    value={formData.email}
                    onChange={handleChange} 
                    placeholder="Nhập email" 
                    required 
                  />
                  {error.email && <span className="error-text">{error.email}</span>}
                </div>
                <div className="input-box">
                  <span className="details">Căn Cước Công Dân</span>
                  <input 
                    type="text"
                    name="citizen_id"
                    value={formData.citizen_id}
                    onChange={handleChange} 
                    placeholder="Nhập căn cước công dân" 
                    required 
                  />
                  {error.citizen_id && <span className="error-text">{error.citizen_id}</span>}
                </div>
                <div className="input-box">
                  <span className="details">Họ Tên</span>
                  <input 
                    type="text"
                    name="full_name"
                    value={formData.full_name}
                    onChange={handleChange} 
                    placeholder="Nhập họ tên" 
                    required 
                  />
                </div>
                <div className="input-box">
                  <span className="details">Ngày Sinh</span>
                  <input 
                    type="date"
                    name="date_of_birth"
                    value={formData.date_of_birth}
                    onChange={handleChange} 
                    required 
                  />
                  {error.date_of_birth && <span className="error-text">{error.date_of_birth}</span>}
                </div>
                <div className="input-box">
                  <span className="details">Mật Khẩu</span>
                  <input 
                    type="text"
                    name="password"
                    value={formData.password}
                    onChange={handleChange} 
                    placeholder="Nhập mật khẩu" 
                    required 
                  />
                  {error.password && <span className="error-text">{error.password}</span>}
                </div>
                <div className="input-box">
                  <span className="details">Xác Nhận Mật Khẩu</span>
                  <input 
                    type="text"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange} 
                    placeholder="Xác nhận mật khẩu" 
                    required 
                  />
                  {error.confirmPassword && <span className="error-text">{error.confirmPassword}</span>}
                </div>
              </div>
              <div className="gender-image-wrapper">
                <div className="gender-details">
                  <input 
                    type="radio" 
                    name="gender"
                    value="M"
                    checked={formData.gender === "M"}
                    onChange={handleChange} 
                    id="dot-1" 
                  />
                  <input 
                    type="radio" 
                    name="gender"
                    value="F"
                    checked={formData.gender === "F"}
                    onChange={handleChange} 
                    id="dot-2" />
                  <span className="gender-title">Giới Tính</span>
                  <div className="category">
                    <label htmlFor="dot-1">
                      <span className="dot one"></span>
                      <span className="gender">Nam</span>
                    </label>
                    <label htmlFor="dot-2">
                      <span className="dot two"></span>
                      <span className="gender">Nữ</span>
                    </label>
                  </div>
                </div>
                
                <div className="input-box image-upload">
                  <span className="details">Ảnh Đại Diện</span>
                  <input 
                    type="file" 
                    name="avatar"
                    onChange={handleChange}
                    accept="image/*"/>
                </div>
              </div>
              <div className="button">
                <input type="submit" value="Đăng Ký" />
              </div>
            </form>
          </div>
        </div>
        <div class="background-section"></div>
      </div>
    </div>
  );
};

export default CustomerRegister;
