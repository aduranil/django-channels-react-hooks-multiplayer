import React from 'react';

const FormField = ({
  input, onChange, error, labelName, type,
}) => (
  <div
    style={{
      marginTop: '10px',
      marginBottom: '10px',
    }}
  >
    <label>{labelName}</label>
    <input
      style={{
        width: '100%',
      }}
      type={type}
      label={labelName}
      name={labelName}
      value={input}
      onChange={onChange}
      error={error}
    />
  </div>
);
export default FormField;
