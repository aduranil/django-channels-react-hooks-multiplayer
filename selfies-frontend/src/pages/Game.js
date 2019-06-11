import React from 'react';
import {
  Box, Text, Button, Grid, Grommet,
} from 'grommet';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { wsConnect, leaveGame } from '../modules/websocket';
import { getGame } from '../modules/game';
import { getMessages } from '../modules/message';
import withAuth from '../hocs/authWrapper';

const theme = {
  button: {
    padding: {
      horizontal: '6px',
    },
  },
};

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
    dispatch(getMessages(id));
  };

  leaveGame = () => {
    const { id, dispatch, history } = this.props;
    dispatch(leaveGame(id));
    history.push('/games');
  };

  render() {
    const { id, messages } = this.props;
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
            {Array.isArray(messages.messages)
              && messages.messages.map(message => (
                <Grid key={message.id} columns={{ count: 2 }}>
                  <Grommet theme={theme}>
                    <Text>
                      {' '}
                      {message.user.username}
:
                      {message.message}
                    </Text>
                  </Grommet>
                </Grid>
              ))}
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
  messages: state.messages,
  username: state.auth.username,
  socket: state.socket.host,
  joinedUser: state.socket.user,
  users: state.socket.users,
});
export default withAuth(connect(s2p)(Game));
