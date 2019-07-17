import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { handleLogin, removeError, handleSignup } from '../modules/account';
import Form from '../components/Form';
import HalfRectangle from '../images/Rectangle';
import Navigation from '../components/Navigation';

class LoginOrSignup extends React.Component {
  state = {
    email: '',
    password: '',
    username: '',
  };

  componentWillUnmount() {
    const { dispatch } = this.props;
    dispatch(removeError());
  }

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
    const { dispatch, history, route } = this.props;
    if (route === '/loginorsignup') {
      await dispatch(handleLogin(this.state));
      return history.push('/games');
    }
    await dispatch(handleSignup(this.state));
    history.push('/games');
  };

  render() {
    const { username, email, password } = this.state;
    const { route } = this.props;
    return (
      <React.Fragment>
        <Navigation />
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            minWidth: '100vw',
            minHeight: '80vh',
          }}
        >
          <HalfRectangle color="#70D6FF" />
          <div
            style={{
              alignSelf: 'center',
              boxShadow: '0 2px 10px 0 rgba(0, 0, 0, 0.25), inset 0 1px 3px 0 rgba(0, 0, 0, 0.25)',
              borderRadius: '20px',
              backgroundColor: '#ff70a6',
            }}
          >
            <h1 style={{ textAlign: 'center', marginTop: '15px' }}>
              {route === '/loginorsignup' ? 'Returning Users' : 'New Users'}
            </h1>
            <Form
              route={route}
              username={username}
              password={password}
              email={email}
              handleChange={this.handleChange}
              handleSubmit={this.handleSubmit}
            />
          </div>
        </div>
      </React.Fragment>
    );
  }
}

LoginOrSignup.propTypes = {
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
  }).isRequired,
  dispatch: PropTypes.func,
  route: PropTypes.string,
};

LoginOrSignup.defaultProps = {
  dispatch: PropTypes.func,
  route: PropTypes.string,
};

const s2p = (state, ownProps) => ({
  route: ownProps.match && ownProps.match.path,
});
export default connect(s2p)(LoginOrSignup);
