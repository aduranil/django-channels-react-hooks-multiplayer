import React from 'react';
import {
  Box, Text, Button, Grid, Grommet,
} from 'grommet';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { grommet } from 'grommet/themes';
import { wsConnect, wsDisconnect } from '../modules/websocket';
import { getGame, startRound, leaveGame } from '../modules/game';
import withAuth from '../hocs/authWrapper';
import ChatBox from '../components/ChatBox';
import GameView from '../components/GameScreen';

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

  leaveGame = async () => {
    const { id, dispatch, history } = this.props;
    const host = `ws://127.0.0.1:8000/ws/game/${id}?token=${localStorage.getItem('token')}`;
    await dispatch(leaveGame(id));
    await dispatch(wsDisconnect(host));
    history.push('/games');
  };

  startRound = () => {
    const { id, dispatch } = this.props;
    dispatch(startRound(id));
  };

  render() {
    const { id, game, time } = this.props;
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
                <Grid columns="140px">
                  <Button margin="xsmall" onClick={this.leaveGame} label="leave game" />
                  <Button margin="xsmall" onClick={this.startRound} label="start game" />
                  <Text>{time}</Text>
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
  game: PropTypes.shape({
    id: PropTypes.number,
    username: PropTypes.string,
  }),
  time: PropTypes.string,
};

Game.defaultProps = {
  id: PropTypes.string,
  dispatch: PropTypes.func,
  game: PropTypes.null,
  time: PropTypes.null,
};

const s2p = (state, ownProps) => ({
  id: ownProps.match && ownProps.match.params.id,
  username: state.auth.username,
  game: state.games.game,
  time: state.games.time,
});
export default withAuth(connect(s2p)(Game));
