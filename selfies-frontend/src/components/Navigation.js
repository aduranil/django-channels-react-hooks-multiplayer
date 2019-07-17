import React from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { logoutUser } from '../modules/account';

class Navigation extends React.Component {
  onLogout = async () => {
    const { dispatch, history } = this.props;
    await dispatch(logoutUser());
    return history.push('/loginorsignup');
  };

  render() {
    const { loggedIn } = this.props;
    return (
      <div className="container">
        <h1> Selfies 2020 </h1>
        {loggedIn && (
          <button type="button" style={{ width: '100px' }} onClick={this.onLogout}>
            logout
          </button>
        )}
      </div>
    );
  }
}

const s2p = state => ({
  host: state.websocket.host,
  loggedIn: state.auth.loggedIn,
});

export default connect(s2p)(withRouter(Navigation));
