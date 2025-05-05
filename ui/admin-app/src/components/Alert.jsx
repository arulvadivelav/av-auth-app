import React, { useEffect } from 'react';
import '../styles/AlertMessage.css';

const stringify = (data) => {
  if (typeof data === 'string') return data;
  if (Array.isArray(data)) return data.join(', ');
  if (typeof data === 'object' && data !== null) return JSON.stringify(data);
  return String(data);
};

const AlertBox = ({ message, onClose, alertType = 'info' }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`alert-box ${alertType}`}>
      {stringify(message)}
      <span className="closebtn" onClick={onClose}>
        &times;
      </span>
    </div>
  );
};

export default AlertBox;
