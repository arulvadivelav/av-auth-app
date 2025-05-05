import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import SendOtpPage from './pages/SendOTP';
import DashboardPage from './pages/Dashboard';
import RegisterPage from './pages/Register';
import ForgotPasswordPage from './pages/ForgotPassword'

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/send-otp" element={<SendOtpPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/register" element={< RegisterPage />} />
        <Route path="/forgot-password" element={< ForgotPasswordPage />} />
        {/* You can add other routes like Home, Register, etc */}
      </Routes>
    </Router>
  );
};

export default AppRoutes;
