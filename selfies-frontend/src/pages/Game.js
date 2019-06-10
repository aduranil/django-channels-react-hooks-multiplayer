import React from 'react';
import { Box, Text, Button } from 'grommet';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { wsConnect, leaveGame } from '../modules/websocket';
import { getGame } from '../modules/game';
import withAuth from '../hocs/authWrapper';

class Game extends React.Component {
  componentDidMount() {
    const { id } = this.props;
    if (id) {
      this.connectAndJoin();
    }
  }

  connectAndJoin = async () => {
    const { id, dispatch } = this.props;
    const host = `ws://127.0.0.1:8000/ws/game/${id}?token=${localStorage.getItem('token')}`;
    await dispatch(wsConnect(host));
    dispatch(getGame(id));
  };

  leaveGame = () => {
    const { id, dispatch, history } = this.props;
    dispatch(leaveGame(id));
    history.push('/games');
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
          <Button onClick={this.leaveGame} label="leave game" />
        </React.Fragment>
      );
    }
    return `${<Text> LOADING </Text>}`;
  }
}

Game.propTypes = {
  id: PropTypes.string,
  dispatch: PropTypes.func,
  joinedUser: PropTypes.string,
  history: PropTypes.func,
};

Game.defaultProps = {
  id: PropTypes.string,
  dispatch: PropTypes.func,
  joinedUser: PropTypes.null,
  history: PropTypes.func,
};

const s2p = (state, ownProps) => ({
  id: ownProps.match && ownProps.match.params.id,
  username: state.auth.username,
  socket: state.socket.host,
  joinedUser: state.socket.user,
  users: state.socket.users,
});
export default withAuth(connect(s2p)(Game));
