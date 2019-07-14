import React from 'react';
import {
  Grid, Text, Grommet, Button,
} from 'grommet';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { logoutUser } from '../modules/account';
import { wsDisconnect } from '../modules/websocket';

const theme = {
  button: {
    padding: {
      horizontal: '6px',
    },
  },
};

class Navigation extends React.Component {
  onLogout = async () => {
    const { dispatch, history, host } = this.props;
    await dispatch(logoutUser());
    await dispatch(wsDisconnect(host));
    history.push('/loginorsignup');
  };

  render() {
    return (
      <div>
        <Text alignSelf="start"> SELFIES 2020 </Text>
        <Grommet theme={theme} style={{ textAlign: 'right' }}>
          <Button onClick={this.onLogout} label="logout" />
        </Grommet>
      </div>
    );
  }
}

const s2p = state => ({
  host: state.websocket.host,
});

export default connect(s2p)(withRouter(Navigation));
