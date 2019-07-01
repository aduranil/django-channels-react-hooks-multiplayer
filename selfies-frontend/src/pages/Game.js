import React from 'react';
import {
  Box, Text, Button, Grid, Grommet,
} from 'grommet';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { grommet } from 'grommet/themes';
import { wsConnect } from '../modules/websocket';
import { getGame, startRound, leaveGame } from '../modules/game';
import withAuth from '../hocs/authWrapper';
import ChatBox from '../components/ChatBox';
import GameView from '../components/GameScreen';

class Game extends React.Component {
  state = {
    time: 0,
    start: 0,
    isOn: false,
  };

  componentDidMount() {
    const { id } = this.props;
    if (id) {
      this.connectAndJoin();
    }
  }

  componentDidUpdate(prevProps) {
    const { game } = this.props;
    if (
      game
      && prevProps.game
      && game.round_started
      && game.round_started !== prevProps.game.round_started
    ) {
      this.startTimer();
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

  startTimer = () => {
    console.log('timer started');
    this.setState({
      time: this.state.time,
      start: Date.now() - this.state.time,
      isOn: true,
    });
    this.timer = setInterval(
      () => this.setState({
        time: Date.now() - this.state.start,
      }),
      1,
    );
  };

  stopTimer = () => {
    this.setState({ isOn: false });
    clearInterval(this.timer);
  };

  resetTimer = () => {
    this.setState({ time: 0 });
  };

  render() {
    const { id, game } = this.props;
    if (id) {
      return (
        <React.Fragment>
          <Grommet theme={grommet} full>
            <Grid
              fill
              areas={[
                { name: 'nav', start: [0, 0], end: [0, 0] },
                { name: 'main', start: [1, 0], end: [1, 0] },
              ]}
              columns={['medium', 'flex']}
              rows={['flex']}
              gap="small"
            >
              <Box gridArea="nav">
                <ChatBox game={game} />
              </Box>
              <Box gridArea="main">
                <GameView game={game} />
                <Grid columns="small">
                  <Text>{this.state.time}</Text>
                  <Button onClick={this.leaveGame} label="leave game" />
                  <Button onClick={this.startRound} label="start game" />
                </Grid>
              </Box>
            </Grid>
          </Grommet>
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
  players: PropTypes.Array,
};

const s2p = (state, ownProps) => ({
  id: ownProps.match && ownProps.match.params.id,
  username: state.auth.username,
  game: state.games.game,
});
export default withAuth(connect(s2p)(Game));
