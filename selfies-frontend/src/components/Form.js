import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import FormField from './FormField';

const Form = ({
  handleSubmit, email, password, username, route, handleChange, error,
}) => (
  <div
    style={{
      padding: '5%',
      width: '500px',
      height: '330px',
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
    <button type="submit" style={{ width: '100%' }} onClick={handleSubmit}>
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
