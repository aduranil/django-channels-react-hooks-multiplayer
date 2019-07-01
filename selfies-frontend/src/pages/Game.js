import React from 'react';
import {
  Box, Text, Button, Grid,
} from 'grommet';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { wsConnect } from '../modules/websocket';
import { getGame, startRound, leaveGame } from '../modules/game';
import withAuth from '../hocs/authWrapper';
import { Phone } from '../images/iPhone';
import Timer from '../components/Timer';
import ChatBox from '../components/ChatBox';

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

  startRound = () => {
    const { id, dispatch } = this.props;
    dispatch(startRound(id));
  };

  render() {
    const { id, game } = this.props;
    if (id) {
      return (
        <React.Fragment>
          <ChatBox game={game} />
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
              {game
                && game.users.map(player => (
                  <Box key={player.id}>
                    {player.username}
                    {player.started ? ' !' : ' ?'}
                    <Phone />
                    {' '}
                  </Box>
                ))}
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
  game: state.games.game,
});
export default withAuth(connect(s2p)(Game));
