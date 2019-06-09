import React from 'react';
import { Form, FormField, Button } from 'grommet';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

class Signup extends React.Component {
  render() {
    const {
      handleSubmit,
      email,
      password,
      username,
      fromLoginOrSignup,
      handleChange,
      error,
    } = this.props;
    return (
      <React.Fragment>
        <Form onSubmit={handleSubmit} color="blue">
          <FormField
            label="email"
            name="email"
            required
            value={email}
            onChange={handleChange}
            error={error}
          />
          {!fromLoginOrSignup && (
            <FormField
              label="username"
              name="username"
              required
              value={username}
              onChange={handleChange}
            />
          )}
          <FormField
            type="password"
            label="password"
            name="password"
            required
            value={password}
            onChange={handleChange}
          />
          <Button type="submit" primary label="Submit" />
        </Form>
      </React.Fragment>
    );
  }
}

Signup.propTypes = {
  handleSubmit: PropTypes.func,
  fromLoginOrSignup: PropTypes.bool,
};

Signup.defaultProps = {
  handleSubmit: PropTypes.func,
  fromLoginOrSignup: PropTypes.bool,
};

const s2p = state => ({
  error: state.auth.errorMessage,
});
export default connect(s2p)(Signup);
