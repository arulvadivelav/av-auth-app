import React from 'react';

const InputField = ({ id, name, type = "text", placeholder, value, required = false, onChange }) => {
  return (
    <input
      id={id}
      name={name}
      type={type}
      placeholder={placeholder}
      value={value}
      required={required}
      onChange={onChange}
      style={{
        width: '100%',
        padding: '10px',
        margin: '8px 0',
        border: '1px solid #ccc',
        borderRadius: '4px',
      }}
    />
  );
};

export default InputField;
