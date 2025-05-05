import React, { useState } from 'react';
import InputField from '../components/InputField';
import { apiRequest } from '../services/AuthServices';
import { useNavigate } from 'react-router-dom';
import { RESPONSE_200, RESPONSE_400 } from '../constants/constants'
import AlertBox from '../components/Alert'
import '../styles/LoginPage.css';

const LoginPage = () => {
  const [data, setData] = useState({ email_id: '', password: '' });
  const [errorMsg, setErrorMsg] = useState({ email_id: '', password: '', general: '' });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [isRequired, setIsRequired] = useState(true);
  const [alert, setAlert] = useState({ message: '', type: '' });

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorMsg({ email_id: '', password: '', general: '' });
    setLoading(true);
    try {

      const result = await apiRequest('login', 'POST', data);

      if (result.status_code === RESPONSE_200) {
        setAlert({ message: result.message, type: 'success' });
        setTimeout(() => {
          navigate('/dashboard')
        }, 2000)

      } else if (result.status_code === RESPONSE_400) {
        setAlert({ message: result.message, type: 'error' });
        setErrorMsg(result.message)
      } else {
        setAlert({ message: result.message, type: 'error' });
      }
    } catch (error) {
      setAlert({ message: "Internal server error", type: 'error' });
    }
    setLoading(false);
  };

  return (
    <div className="login-container">
      {alert.message && (
        <AlertBox
          message={alert.message}
          alertType={alert.type}
          onClose={() => setAlert({ message: '', type: '' })}
        />
      )}
      <h2>Welcome Back</h2>
      <p className="subtitle">Please login to your account</p>

      <form onSubmit={handleLogin}>
        <div className="form-group">
          <label htmlFor="email_id">Email Address <span className="required">*</span></label>
          <InputField
            id="email_id"
            name="email_id"
            type="email"
            placeholder="Enter your email"
            value={data.email_id}
            required={isRequired}
            onChange={(e) => setData({ ...data, email_id: e.target.value })}
          />
          {errorMsg.email_id && <p className="fieldError">{errorMsg.email_id}</p>}
        </div>

        <div className="form-group">
          <label htmlFor="password">Password <span className="required">*</span></label>
          <InputField
            id="password"
            name="password"
            type="password"
            placeholder="Enter your password"
            value={data.password}
            required={isRequired}
            onChange={(e) => setData({ ...data, password: e.target.value })}
          />
          {errorMsg.password && <p className="fieldError">{errorMsg.password}</p>}
        </div>

        {errorMsg.general && <p className="fieldError">{errorMsg.general}</p>}

        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>

      <div className="links">
        <a href="/send-otp?type=forgot">Forgot Password?</a>
        <span>|</span>
        <a href="/send-otp?type=register">New User</a>
      </div>
    </div>
  );
};

export default LoginPage;
