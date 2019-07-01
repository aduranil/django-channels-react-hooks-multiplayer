import React from 'react';
import {
  Box, Text, Button, Grid, Grommet, TextArea,
} from 'grommet';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { wsConnect } from '../modules/websocket';
import { getGame, startRound, leaveGame } from '../modules/game';
import { newMessage } from '../modules/message';
import withAuth from '../hocs/authWrapper';
import { Phone } from '../images/iPhone';
import Timer from '../components/Timer';

const theme = {
  button: {
    padding: {
      horizontal: '6px',
    },
  },
};

class Game extends React.Component {
  state = {
    message: '',
  };

  componentDidMount() {
    const { id } = this.props;
    if (id) {
      this.connectAndJoin();
    }
  }

  componentDidUpdate() {
    this.scrollToBottom();
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

  handleChange = (e) => {
    const { value } = e.target;
    this.setState({ message: value });
  };

  handleSubmit = () => {
    const { dispatch } = this.props;
    const { message } = this.state;
    dispatch(newMessage(message));
    this.setState({ message: '' });
  };

  scrollToBottom = () => {
    this.messagesEnd.scrollIntoView({ behavior: 'smooth' });
  };

  startRound = () => {
    const { id, dispatch } = this.props;
    dispatch(startRound(id));
  };

  render() {
    const { id, messages, players } = this.props;
    const { message } = this.state;
    if (id) {
      return (
        <React.Fragment>
          <Box
            round="xsmall"
            width="600px"
            height="300px"
            pad="medium"
            elevation="medium"
            background="accent-2"
            overflow={{ horizontal: 'hidden', vertical: 'scroll' }}
          >
            {Array.isArray(messages.messages)
              && messages.messages.map(msg => (
                <Grid key={msg.id} columns={{ count: 2 }}>
                  <Grommet theme={theme}>
                    <Text>
                      {' '}
                      {msg.message_type === 'action' ? null : `${msg.user.username}: `}
                      {msg.message}
                    </Text>
                  </Grommet>
                </Grid>
              ))}
            <div
              style={{ float: 'left', clear: 'both' }}
              ref={(el) => {
                this.messagesEnd = el;
              }}
            />
          </Box>
          <Box
            width="800px"
            height="500px"
            round="xsmall"
            pad="medium"
            elevation="medium"
            background="accent-2"
          >
            <Timer />
            <Grid gap="small" columns="100px" justify="center">
              {Array.isArray(players)
                && players.map(player => (
                  <Box key={player.id}>
                    {player.username}
                    {player.started ? ' !' : ' ?'}
                    <Phone />
                    {' '}
                  </Box>
                ))}
            </Grid>
          </Box>

          <Box round="xsmall" width="600px" pad="medium" elevation="medium" background="accent-2">
            <Grid gap="small" columns={['450px', 'xsmall']}>
              <Box>
                <TextArea onChange={this.handleChange} value={message} />
              </Box>
              <Box justify="center" align="center" alignContent="center">
                <Button onClick={this.handleSubmit} label="send" />
              </Box>
            </Grid>
          </Box>
          <Button onClick={this.leaveGame} label="leave game" />
          <Button onClick={this.startRound} label="start game" />
        </React.Fragment>
      );
    }
    return `${<Text> LOADING </Text>}`;
  }
}

Game.propTypes = {
  id: PropTypes.string,
  dispatch: PropTypes.func,
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
  }).isRequired,
  messages: PropTypes.shape({
    id: PropTypes.number,
    message: PropTypes.string,
  }),
  players: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      username: PropTypes.string,
    }),
  ),
};

Game.defaultProps = {
  id: PropTypes.string,
  dispatch: PropTypes.func,
  messages: PropTypes.shape({
    id: PropTypes.number,
    message: PropTypes.string,
  }),
  players: PropTypes.Array,
};

const s2p = (state, ownProps) => ({
  id: ownProps.match && ownProps.match.params.id,
  messages: state.messages,
  username: state.auth.username,
  players: state.games.players,
});
export default withAuth(connect(s2p)(Game));
