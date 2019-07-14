import React from 'react';

const Button = (props, { text }) => (
  <button
    style={{
      width: '100%',
      height: '40px',
      borderRadius: '5px',
      border: 'none',
      marginTop: '20px',
      marginBottom: '10px',
      cursor: 'pointer',
    }}
    type="submit"
  >
    {text}
  </button>
);

export default Button;
