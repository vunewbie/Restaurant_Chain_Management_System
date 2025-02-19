import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const RegisterVerifyOTP = () => {
  const [otpCode, setOtpCode] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const username = localStorage.getItem('username');

  const handleOTPSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/accounts/verify-otp/register', {
        username: username,
        otp_code: otpCode
      });
      if (response.data && response.data.message === 'Account has been created') {
        alert('Tài khoản đã được tạo thành công!');
        navigate('/Login');
      }
    } catch (err) {
      setError('OTP không hợp lệ, vui lòng thử lại.');
    }
  };

  const handleResendOTP = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/accounts/customers/resend-otp', {
        username: username
      });
      if (response.data && response.data.message === 'OTP has been sent to your email') {
        alert('OTP đã được gửi lại thành công!');
      }
    } catch (err) {
      setError('Không thể gửi lại OTP, vui lòng thử lại.');
    }
  };

  return (
    <div>
      <h1>Verify OTP</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleOTPSubmit}>
        <input
          type="text"
          placeholder="Enter OTP"
          value={otpCode}
          onChange={(e) => setOtpCode(e.target.value)}
          required
        />
        <button type="submit">Submit</button>
      </form>
      <button onClick={handleResendOTP}>Gửi Lại OTP</button>
    </div>
  );
};

export default RegisterVerifyOTP;
