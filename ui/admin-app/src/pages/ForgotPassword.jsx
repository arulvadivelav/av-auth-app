import React, { useState } from 'react';
import InputField from '../components/InputField';
import { apiRequest } from '../services/AuthServices';
import { useNavigate } from 'react-router-dom';
import { RESPONSE_200, RESPONSE_400 } from '../constants/constants'
import AlertBox from '../components/Alert'
import '../styles/LoginPage.css';

const ForgotPasswordPage = () => {
  const [data, setData] = useState({ email_id: '', otp: '', new_password: '', confirm_password: '' })
  const [errorMsg, setErrorMsg] = useState({ email_id: '', otp: '', new_password: '', confirm_password: '' });
  const navigate = useNavigate()
  const [isRequired, setIsRequired] = useState(true);
  const [alert, setAlert] = useState({ message: '', type: '' });

  const handleForgotPassword = async (e) => {
    e.preventDefault();
    setErrorMsg({});
    try {

      const result = await apiRequest('forgot-password', 'POST', data);

      if (result.status_code === RESPONSE_200) {
        setAlert({ message: result.message, type: 'success' });
        setTimeout(() => {
          navigate('/')
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
      <h2>Forgot Password</h2>
      <form onSubmit={handleForgotPassword}>
        <div className='form-group'>
          <label htmlFor="email_id">Email Address <span className="required">*</span></label>
          <InputField
            id="email_id"
            name="email_id"
            type="email"
            required={isRequired}
            placeholder="Enter your email"
            value={data.email_id}
            onChange={(e) => setData({ ...data, email_id: e.target.value })}
          />
          {errorMsg && <p className="fieldError">{errorMsg.email_id}</p>}
          <label htmlFor="otp">Enter your OTP <span className="required">*</span></label>
          <InputField
            id="otp"
            name="otp"
            type="password"
            required={isRequired}
            placeholder="Enter your OTP"
            value={data.otp}
            onChange={(e) => setData({ ...data, otp: e.target.value })}
          />
          {errorMsg && <p className="fieldError">{errorMsg.otp}</p>}
          <label htmlFor="new_password">Enter your new password <span className="required">*</span></label>
          <InputField
            id="new_password"
            name="new_password"
            type="password"
            required={isRequired}
            placeholder="New Password"
            value={data.new_password}
            onChange={(e) => setData({ ...data, new_password: e.target.value })}
          />
          {errorMsg && <p className="fieldError">{errorMsg.new_password}</p>}
          <label htmlFor="confirm_password">Enter your confirm password <span className="required">*</span></label>
          <InputField
            id="confirm_password"
            name="confirm_password"
            type="password"
            required={isRequired}
            placeholder="Confirm Password"
            value={data.confirm_password}
            onChange={(e) => setData({ ...data, confirm_password: e.target.value })}
          />
          {errorMsg && <p className="fieldError">{errorMsg.confirm_password}</p>}
        </div>

        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default ForgotPasswordPage;
