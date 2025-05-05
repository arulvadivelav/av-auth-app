import React, { useState } from 'react';
import InputField from '../components/InputField';
import { apiRequest } from '../services/AuthServices';
import { RESPONSE_200, RESPONSE_201, RESPONSE_400 } from '../constants/constants'
import AlertBox from '../components/Alert'
import { useNavigate } from 'react-router-dom';
import '../styles/LoginPage.css';

const RegisterPage = () => {
  const [data, setData] = useState({ username: '', password: '', confirm_password: '', email: '', first_name: '', last_name: '' })
  const [errorMsg, setErrorMsg] = useState({ username: '', password: '', confirm_password: '', email: '', first_name: '', last_name: '' });
  const [isRequired, setIsRequired] = useState(true);
  const [alert, setAlert] = useState({ message: '', type: '' });
  const navigate = useNavigate()

  const handleRegister = async (e) => {
    e.preventDefault();
    setErrorMsg({});
    try {

      const result = await apiRequest('register', 'POST', data);

      if (result.status_code === RESPONSE_200 || result.status_code === RESPONSE_201) {
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
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <div className='form-group'>
          <label htmlFor="username">Username <span className="required">*</span></label>
          <InputField
            id="username"
            name="username"
            type=""
            required={isRequired}
            placeholder="Enter your username"
            value={data.username}
            onChange={(e) => setData({ ...data, username: e.target.value })}
          />
          {errorMsg && <p className="fieldError">{errorMsg.username}</p>}
          <label htmlFor="password">Password <span className="required">*</span></label>
          <InputField
            id="password"
            name="password"
            type="password"
            required={isRequired}
            placeholder="password"
            value={data.password}
            onChange={(e) => setData({ ...data, password: e.target.value })}
          />
          {errorMsg && <p className="fieldError">{errorMsg.password}</p>}
          <label htmlFor="confirm_password">Confirm password <span className="required">*</span></label>
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
          <label htmlFor="email_id">Email Address <span className="required">*</span></label>
          <InputField
            id="email_id"
            name="email_id"
            type="email"
            required={isRequired}
            placeholder="Enter your email"
            value={data.email}
            onChange={(e) => setData({ ...data, email: e.target.value })}
          />
          {errorMsg && <p className="fieldError">{errorMsg.email}</p>}
          <label htmlFor="first_name">First name</label>
          <InputField
            id="first_name"
            name="first_name"
            type=""
            required={isRequired}
            placeholder="Enter your first name"
            onChange={(e) => setData({ ...data, first_name: e.target.value })}
          />
          {errorMsg && <p className="fieldError">{errorMsg.first_name}</p>}
          <label htmlFor="last_name">Last name</label>
          <InputField
            id="last_name"
            name="last_name"
            type=""
            placeholder="Enter your last name"
            value={data.last_name}
            onChange={(e) => setData({ ...data, last_name: e.target.value })}
          />
          {errorMsg && <p className="fieldError">{errorMsg.last_name}</p>}
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  );
};

export default RegisterPage;
