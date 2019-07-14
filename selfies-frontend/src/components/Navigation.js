import React from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { logoutUser } from '../modules/account';
import { wsDisconnect } from '../modules/websocket';

class Navigation extends React.Component {
  onLogout = async () => {
    const { dispatch, history, host } = this.props;
    await dispatch(logoutUser());
    await dispatch(wsDisconnect(host));
    history.push('/loginorsignup');
  };

  render() {
    return (
      <div className="container">
        <button style={{ width: '100px' }} onClick={this.onLogout}>
          logout
        </button>
      </div>
    );
  }
}

const s2p = state => ({
  host: state.websocket.host,
});

export default connect(s2p)(withRouter(Navigation));
