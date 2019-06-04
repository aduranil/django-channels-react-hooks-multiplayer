import React from 'react';
import { Text, Box } from 'grommet';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { handleSignup } from './modules/account';
import Login from './components/LoginOrSignup';

class Signup extends React.Component {
  handleSubmit = () => {
    const { dispatch, history } = this.props;
    dispatch(handleSignup(this.state)).then(() => history.push('/games'));
  };

  render() {
    return (
      <React.Fragment>
        <Box margin="medium" width="medium" elevation="medium" pad="medium" round="small">
          <Text textAlign="center" color="white" margin={{ left: 'small' }}>
            NEW USERS
          </Text>
          <Login handleSubmit={this.handleSubmit} />
        </Box>
      </React.Fragment>
    );
  }
}

Signup.propTypes = {
  history: PropTypes.func,
  dispatch: PropTypes.func,
};

Signup.defaultProps = {
  history: PropTypes.func,
  dispatch: PropTypes.func,
};
export default connect()(Signup);
