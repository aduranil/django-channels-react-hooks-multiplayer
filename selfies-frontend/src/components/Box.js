import React from 'react';

const Box = props => (
  <div
    style={{
      backgroundColor: '#ff70a6',
      boxShadow: '0 2px 10px 0 rgba(0, 0, 0, 0.5), inset 0 1px 3px 0 rgba(0, 0, 0, 0.5)',
      borderRadius: '20px',
      flexGrow: 1,
      margin: '30px auto 100px auto',
      width: '50%',
      padding: '3%',
      minHeight: '300px',
    }}
  >
    {props.children}
  </div>
);

export default Box;
