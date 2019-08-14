import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { handleLogin, handleSignup } from '../modules/account';
import Form from '../components/Form';
import HalfRectangle from '../images/Rectangle';
import Navigation from '../components/Navigation';

class LoginOrSignup extends React.Component {
  state = {
    email: '',
    password: '',
    username: '',
    error: null,
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
    const { dispatch, history, route } = this.props;
    let response;
    if (route === '/loginorsignup') {
      response = await dispatch(handleLogin(this.state));
    } else {
      response = await dispatch(handleSignup(this.state));
    }
    if (response && response.type === 'SET_ERROR') {
      return this.setState({ error: response.data });
    }
    return history.push('/games');
  };

  componentWillUnmount() {
    this.setState({ error: null });
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.route !== this.props.route) {
      this.setState({ error: null });
    }
  }

  render() {
    const {
      username, email, password, error,
    } = this.state;
    const { route } = this.props;
    return (
      <div>
        <Navigation path="login" />
        <React.Fragment>
          <HalfRectangle color="#70D6FF" />
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              minHeight: '80vh',
            }}
          >
            <div
              className="phone-signup"
              style={{
                alignSelf: 'center',
                boxShadow:
                  '0 2px 10px 0 rgba(0, 0, 0, 0.25), inset 0 1px 3px 0 rgba(0, 0, 0, 0.25)',
                borderRadius: '20px',
                backgroundColor: '#ff70a6',
                width: '30%',
                minWidth: '300px',
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
                error={error}
                handleChange={this.handleChange}
                handleSubmit={this.handleSubmit}
              />
            </div>
          </div>
        </React.Fragment>
      </div>
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
