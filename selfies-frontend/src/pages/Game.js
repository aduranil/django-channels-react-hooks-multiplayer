import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { wsConnect } from '../modules/websocket';
import {
  startRound, leaveGame, makeMove, getGame,
} from '../modules/game';
import WithAuth from '../hocs/AuthenticationWrapper';
import ChatBox from '../components/ChatBox';
import Navigation from '../components/Navigation';
import { Phone } from '../images/iPhone';

const HOST = 'localhost:8000';
// const HOST = 'selfies-2020.herokuapp.com';

class Game extends React.Component {
  state = {
    currentMove: null,
  };

  componentDidMount() {
    const { id } = this.props;
    if (id) {
      this.connectAndJoin();
    }
  }

  componentDidUpdate(prevProps) {
    const { dispatch, games } = this.props;
    if (games !== prevProps.games) {
      dispatch(updateGame());
    }
  }

  connectAndJoin = async () => {
    const { id, dispatch } = this.props;
    const host = `ws://${HOST}/ws/game/${id}?token=${localStorage.getItem('token')}`;
    await dispatch(wsConnect(host));
  };

  leaveGame = async () => {
    const { id, dispatch, history } = this.props;
    await dispatch(leaveGame(id));
    history.push('/games');
  };

  startRound = () => {
    const { id, dispatch } = this.props;
    dispatch(startRound(id));
  };

  makeMove = (event) => {
    const { dispatch } = this.props;
    let victim = null;
    this.setState({ currentMove: event.currentTarget.value });
    // only the comment game move has another player that it impacts
    if (event.currentTarget.value === 'leave_comment') {
      victim = event.currentTarget.id;
    }
    dispatch(
      makeMove({
        move: event.currentTarget.value,
        victim,
      }),
    );
  };

  render() {
    const {
      id, game, time, currentPlayer,
    } = this.props;
    const { currentMove } = this.state;
    if (id && game) {
      return (
        <React.Fragment>
          <Navigation />
          <h1 style={{ textAlign: 'center' }}>
            {' '}
            {game.room_name}
          </h1>
          <div style={{ display: 'flex', flexDirection: 'row' }}>
            <ChatBox game={game} />
            <div
              style={{
                background: '#ff70a6',
                boxShadow: '0 2px 10px 0 rgba(0, 0, 0, 0.5), inset 0 1px 3px 0 rgba(0, 0, 0, 0.5)',
                borderRadius: '20px',
                flexGrow: '1',
                marginRight: '1%',
                marginBottom: '1%',
                marginTop: '2%',
                width: '50%',
                padding: '2%',
                maxHeight: '500px',
              }}
            >
              <div
                style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-Between' }}
              >
                {game.round_started && (
                  <div>
                    Time left in the round:
                    {time}
                  </div>
                )}
                <div>
                  <button type="button" onClick={this.leaveGame}>
                    leave game
                  </button>
                  {!game.round_started && (
                    <button type="button" onClick={this.startRound}>
                      start game
                    </button>
                  )}
                </div>
              </div>
              <div style={{ display: 'flex', flexDirection: 'row' }}>
                {game.users.map(player => (
                  <div style={{ margin: '1%' }} key={player.username}>
                    {player.username}
                    {player.started ? ' !' : ' ?'}
                    <div>
                      {player.followers}
                      {' '}
                      {player.followers === 1 ? 'follower' : 'followers'}
                    </div>
                    <div style={{ marginBottom: '3px' }}>
                      {player.stories}
                      {' '}
                      {player.stories === 1 ? 'story' : 'stories'}
                    </div>
                    <button
                      onClick={this.makeMove}
                      id={player.id}
                      disabled={!game.round_started}
                      value="leave_comment"
                      className={currentMove === 'leave_comment' ? 'button-color' : null}
                      type="button"
                    >
                      <Phone />
                    </button>
                    {' '}
                  </div>
                ))}
              </div>

              <div style={{ display: 'flex', flexDirection: 'row' }}>
                {game.round_started && (
                  <React.Fragment>
                    <button
                      className={currentMove === 'post_selfie' ? 'button-color' : null}
                      type="button"
                      value="post_selfie"
                      onClick={this.makeMove}
                    >
                      post a selfie
                    </button>
                    <button
                      className={currentMove === 'post_group_selfie' ? 'button-color' : null}
                      type="button"
                      value="post_group_selfie"
                      onClick={this.makeMove}
                    >
                      post group selfie
                    </button>
                    <button
                      type="button"
                      className={currentMove === 'post_story' ? 'button-color' : null}
                      disabled={currentPlayer && currentPlayer.stories === 0}
                      value="post_story"
                      onClick={this.makeMove}
                    >
                      post story
                    </button>
                    <button
                      className={currentMove === 'dont_post' ? 'button-color' : null}
                      type="button"
                      value="dont_post"
                      onClick={this.makeMove}
                    >
                      don't post
                    </button>
                    <button
                      className={currentMove === 'go_live' ? 'button-color' : null}
                      type="button"
                      value="go_live"
                      onClick={this.makeMove}
                    >
                      go live
                    </button>
                    {' '}
                  </React.Fragment>
                )}
              </div>
            </div>
          </div>
        </React.Fragment>
      );
    }
    return `${<span> LOADING </span>}`;
  }
}

Game.propTypes = {
  id: PropTypes.string,
  dispatch: PropTypes.func,
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
  }).isRequired,
  currentPlayer: PropTypes.shape({
    id: PropTypes.number.isRequired,
    followers: PropTypes.number.isRequired,
    stories: PropTypes.number.isRequired,
    username: PropTypes.string.isRequired,
    started: PropTypes.bool.isRequired,
  }),
  game: PropTypes.shape({
    id: PropTypes.number.isRequired,
    game_status: PropTypes.string.isRequired,
    is_joinable: PropTypes.bool.isRequired,
    room_name: PropTypes.string.isRequired,
    round_started: PropTypes.bool.isRequired,
    users: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        followers: PropTypes.number.isRequired,
        stories: PropTypes.number.isRequired,
        username: PropTypes.string.isRequired,
        started: PropTypes.bool.isRequired,
      }),
    ),
    messages: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        username: PropTypes.string.isRequired,
        message: PropTypes.string.isRequired,
        message_type: PropTypes.string.isRequired,
        created_at: PropTypes.string.isRequired,
      }),
    ),
  }),
  time: PropTypes.string,
};

Game.defaultProps = {
  id: PropTypes.string,
  dispatch: PropTypes.func,
  game: PropTypes.null,
  time: PropTypes.null,
  currentPlayer: PropTypes.null,
};

const s2p = (state, ownProps) => ({
  id: ownProps.match && ownProps.match.params.id,
  username: state.auth.username,
  game: state.games.game,
  currentPlayer: state.games.currentPlayer,
  time: state.games.time,
});
export default WithAuth(connect(s2p)(Game));
