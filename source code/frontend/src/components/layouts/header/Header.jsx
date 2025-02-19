// src/components/layouts/header/Header.jsx
import React from "react";
import style from "./Header.module.css";
import vunewbieLogo from "../../../assets/layouts/header/vunewbie-logo.png"; // Import logo

const Header = () => {
  return (
    <header className={style["site-header"]}>
      <div className="container-fluid">
        <div className="row align-items-center">
          {/* Logo section (2 columns) */}
          <div className="col-lg-2">
            <img src={vunewbieLogo} alt="VuNewbie Logo" className={style["logo"]} />
          </div>

          {/* Spacer section (2 columns) */}
          <div className="col-lg-2"></div>

          {/* Navbar section (8 columns) */}
          <div className="col-lg-8">
            <nav className={style["navbar"]}>
              <ul className="nav">
                <li className="nav-item">
                  <a href="#trang-chu" className="nav-link">
                    Trang Chủ
                  </a>
                </li>
                <li className="nav-item">
                  <a href="#gioi-thieu" className="nav-link">
                    Giới Thiệu
                  </a>
                </li>
                <li className="nav-item">
                  <a href="#thuc-don" className="nav-link">
                    Thực Đơn
                  </a>
                </li>
                <li className="nav-item">
                  <a href="#dat-ban" className="nav-link">
                    Đặt Bàn
                  </a>
                </li>
                <li className="nav-item">
                  <a href="#giao-hang" className="nav-link">
                    Giao Hàng
                  </a>
                </li>
                <li className="nav-item">
                  <a href="#thanh-vien" className="nav-link">
                    Thành Viên
                  </a>
                </li>
                <li className="nav-item">
                  <a href="#uu-dai" className="nav-link">
                    Ưu Đãi
                  </a>
                </li>
                <li className="nav-item">
                  <a href="#dang-nhap" className="nav-link">
                    Đăng Nhập
                  </a>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
