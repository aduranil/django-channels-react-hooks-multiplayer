import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

const FormField = ({
  input, onChange, labelName, type,
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
        marginTop: '5px',
      }}
      type={type}
      label={labelName}
      name={labelName}
      value={input}
      onChange={onChange}
      autoComplete="on"
    />
  </div>
);

const Form = ({
  handleSubmit, email, password, username, route, handleChange, error,
}) => (
  <div
    style={{
      padding: '5%',
      width: '500px',
      height: '375px',
    }}
  >
    <form>
      <FormField input={email} labelName="email" onChange={handleChange} type="text" />
      {route === '/signup' && (
        <FormField input={username} labelName="username" type="text" onChange={handleChange} />
      )}
      <FormField input={password} labelName="password" onChange={handleChange} type="password" />
      <button
        onClick={handleSubmit}
        type="button"
        style={{ width: '100%', marginTop: '10px', marginBottom: '10px' }}
      >
        <span style={{ fontSize: '20px' }}>Submit</span>
      </button>
      <span style={{ color: 'white', fontWeight: 'bold' }}>{error}</span>
    </form>
    {route === '/loginorsignup' && (
      <div>
        Click
        {' '}
        <Link to="/signup">here</Link>
        {' '}
to create your user!
      </div>
    )}
    {route === '/signup' && (
      <div>
        Click
        {' '}
        <Link to="/loginorsignup">here</Link>
        {' '}
to login!
      </div>
    )}
  </div>
);

FormField.propTypes = {
  onChange: PropTypes.func.isRequired,
  input: PropTypes.string.isRequired,
  labelName: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
};
Form.propTypes = {
  handleSubmit: PropTypes.func.isRequired,
  handleChange: PropTypes.func.isRequired,
  email: PropTypes.string.isRequired,
  password: PropTypes.string.isRequired,
  username: PropTypes.string.isRequired,
  error: PropTypes.string,
  route: PropTypes.string,
};

Form.defaultProps = {
  error: PropTypes.null,
  route: PropTypes.string,
};

export default Form;
