import React from 'react';
import { Text, Box } from 'grommet';
import { connect } from 'react-redux';
import { join } from './modules/websocket';
import { wsConnect } from './modules/WSClientActions';
import withAuth from './hocs/authWrapper';

class Game extends React.Component {
  componentDidMount() {
    if (this.props.id) {
      this.connectAndJoin();
    }
  }

  connectAndJoin = () => {
    const { id, dispatch, username } = this.props;
    const host = `ws://127.0.0.1:8000/ws/game/${id}?token=${localStorage.getItem('token')}`;
    dispatch(wsConnect(host));
    // setTimeout(() => {
    //   dispatch(join(username, id));
    // }, 3000);
  };

  render() {
    const { id, joinedUser } = this.props;
    if (id) {
      return (
        <React.Fragment>
          <Box
            round="xsmall"
            height="medium"
            margin="medium"
            width="600px"
            pad="medium"
            elevation="medium"
            background="accent-2"
          >
            {joinedUser}
          </Box>
        </React.Fragment>
      );
    }
  }
}
const s2p = (state, ownProps) => ({
  id: ownProps.match && ownProps.match.params.id,
  username: state.auth.username,
  socket: state.socket.host,
  joinedUser: state.socket.user,
  users: state.socket.users,
});
export default withAuth(connect(s2p)(Game));
