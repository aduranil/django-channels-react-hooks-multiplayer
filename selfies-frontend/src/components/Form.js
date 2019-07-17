import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

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
        marginTop: '5px',
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

const Form = ({
  handleSubmit, email, password, username, route, handleChange, error,
}) => (
  <div
    style={{
      padding: '5%',
      width: '500px',
      height: '350px',
    }}
  >
    <FormField input={email} labelName="email" onChange={handleChange} error={error} type="text" />
    {route === '/signup' && (
      <FormField
        input={username}
        labelName="username"
        type="text"
        onChange={handleChange}
        error={error}
      />
    )}
    <FormField
      input={password}
      labelName="password"
      onChange={handleChange}
      type="password"
      error={error}
    />
    <button
      type="submit"
      style={{ width: '100%', marginTop: '10px', marginBottom: '10px' }}
      onClick={handleSubmit}
    >
      <span style={{ fontSize: '20px' }}>Submit</span>
    </button>
    {route === '/loginorsignup' && (
      <div>
        Click
        {' '}
        <Link to="/signup">here</Link>
        {' '}
to create your user!
      </div>
    )}
  </div>
);

Form.propTypes = {
  handleSubmit: PropTypes.func,
  handleChange: PropTypes.func,
  email: PropTypes.string,
  password: PropTypes.string,
  username: PropTypes.string,
  error: PropTypes.string,
  route: PropTypes.string,
};

Form.defaultProps = {
  handleSubmit: PropTypes.func,
  handleChange: PropTypes.func,
  email: PropTypes.string,
  password: PropTypes.string,
  username: PropTypes.null,
  error: PropTypes.null,
  route: PropTypes.string,
};

const s2p = state => ({
  error: state.auth.errorMessage,
});
export default connect(s2p)(Form);
