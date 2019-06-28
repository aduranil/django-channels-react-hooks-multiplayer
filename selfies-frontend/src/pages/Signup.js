import React from 'react';
import { Text, Box } from 'grommet';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { handleSignup } from '../modules/account';
import Login from '../components/LoginOrSignup';

class Signup extends React.Component {
  state = {
    email: '',
    password: '',
    username: '',
  };

  handleChange = (e) => {
    const { name } = e.target;
    const { value } = e.target;
    this.setState((prevstate) => {
      const newState = { ...prevstate };
      newState[name] = value;
      return newState;
    });
  };

  handleSubmit = async () => {
    const { dispatch, history } = this.props;
    const response = await dispatch(handleSignup(this.state));
    if (!response) return history.push('/games');
  };

  render() {
    const { username, email, password } = this.state;
    return (
      <React.Fragment>
        <Box margin="medium" width="medium" elevation="medium" pad="medium" round="small">
          <Text textAlign="center" color="white" margin={{ left: 'small' }}>
            NEW USERS
          </Text>
          <Login
            username={username}
            password={password}
            email={email}
            handleChange={this.handleChange}
            fromLoginOrSignup={false}
            handleSubmit={this.handleSubmit}
          />
        </Box>
      </React.Fragment>
    );
  }
}

Signup.propTypes = {
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
  }).isRequired,
  dispatch: PropTypes.func,
};

Signup.defaultProps = {
  dispatch: PropTypes.func,
};
export default connect()(Signup);
