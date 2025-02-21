import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import LogIn from './pages/Auths/LogIn/LogIn.jsx';
import CustomerRegister from './pages/Auths/Register/CustomerRegister.jsx';
import VerifyOTP from './pages/Auths/VerifyOTP/VerifyOTP.jsx';
import ForgotPassword from './pages/Auths/ForgotPassword/ForgotPassword.jsx';
import Homepage from './pages/Homepage/Homepage.jsx';

function App() {
  console.log('App loaded');
  return (
    <Router>
      <Routes>
        <Route path="/customers/register" element={<CustomerRegister />} />
        <Route path="/verify-otp" element={<VerifyOTP />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/" element={<Homepage />} />
      </Routes>
    </Router>
  );
}

export default App
