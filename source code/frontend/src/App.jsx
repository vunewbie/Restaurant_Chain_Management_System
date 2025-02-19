// App.jsx
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import SignUp from "./pages/signup/SignUp.jsx";
import RegisterVerifyOTP from "./pages/registerverifyotp/RegisterVerifyOTP.jsx";

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<SignUp />} />
          <Route path="/verify-otp" element={<RegisterVerifyOTP />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;