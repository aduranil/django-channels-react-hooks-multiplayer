import React from 'react';
import { Form, FormField, Button } from 'grommet';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

class Signup extends React.Component {
  state = {
    email: '',
    password: '',
    username: '',
  };

  handleChange = (e) => {
    const { name } = e.target;
    const { value } = e.target;
    if (name === 'email') {
      this.setState({ username: value });
    }
    this.setState((prevstate) => {
      const newState = { ...prevstate };
      newState[name] = value;
      return newState;
    });
  };

  render() {
    const { email, password } = this.state;
    const { handleSubmit } = this.props;
    return (
      <React.Fragment>
        <Form onSubmit={handleSubmit} color="blue">
          <FormField
            label="email"
            name="email"
            required
            value={email}
            onChange={this.handleChange}
          />
          <FormField
            type="password"
            label="password"
            name="password"
            required
            value={password}
            onChange={this.handleChange}
          />
          <Button type="submit" primary label="Submit" />
        </Form>
      </React.Fragment>
    );
  }
}

Signup.propTypes = {
  handleSubmit: PropTypes.func,
};

Signup.defaultProps = {
  handleSubmit: PropTypes.func,
};
export default connect()(Signup);
