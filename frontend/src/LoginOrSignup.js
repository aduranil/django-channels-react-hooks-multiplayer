import React from 'react';
import { Box, Text } from 'grommet';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { handleLogin } from './modules/account';
import Login from './components/LoginOrSignup';

class LoginOrSignup extends React.Component {
  handleSubmit = () => {
    const { dispatch, history } = this.props;
    dispatch(handleLogin(this.state)).then(() => history.push('/games'));
  };

  render() {
    return (
      <React.Fragment>
        <Box
          gap="medium"
          width="medium"
          elevation="medium"
          pad="medium"
          round="small"
          margin="15px"
        >
          <Text textAlign="center" color="white" margin={{ left: 'small' }}>
            NEW USERS
          </Text>
          <Text margin={{ left: 'small' }}>
            Click
            {' '}
            <Link to="/signup">here</Link>
            {' '}
to create your user!
          </Text>
        </Box>
        <Box width="medium" elevation="medium" pad="medium" round="small">
          <Text textAlign="center" color="white" margin={{ left: 'small' }}>
            RETURNING USERS
          </Text>
          <Login handleSubmit={this.handleSubmit} />
        </Box>
      </React.Fragment>
    );
  }
}

LoginOrSignup.propTypes = {
  history: PropTypes.func,
  dispatch: PropTypes.func,
};

LoginOrSignup.defaultProps = {
  history: PropTypes.func,
  dispatch: PropTypes.func,
};
export default connect()(LoginOrSignup);
