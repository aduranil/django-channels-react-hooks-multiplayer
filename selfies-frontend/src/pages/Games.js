import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Navigation from '../components/Navigation';
import { createGame, getGames } from '../modules/game';
import WithAuth from '../hocs/AuthenticationWrapper';
import HalfRectangle from '../images/Rectangle';

class Games extends React.Component {
  state = {
    roomName: '',
  };

  componentDidMount() {
    const { dispatch, loggedIn } = this.props;
    if (loggedIn) {
      dispatch(getGames());
    }
  }

  // componentDidUpdate(prevProps) {
  //   const { dispatch, games } = this.props;
  //   if (games !== prevProps.games) {
  //     dispatch(getGames());
  //   }
  // }

  onClick = () => {
    const { dispatch, history } = this.props;
    const { roomName } = this.state;
    if (roomName.length === 0) {
      return alert('You must include a room name');
    }
    return dispatch(createGame(roomName)).then((data) => {
      history.push(data);
    });
  };

  onJoin = (e) => {
    e.preventDefault();
    const { history } = this.props;
    history.push(`/game/${e.target.value}`);
  };

  onKeyPress = (e) => {
    if (e.key === 'Enter') {
      this.onClick();
    }
  };

  render() {
    const { roomName } = this.state;
    const { games } = this.props;
    return (
      <React.Fragment>
        <HalfRectangle color="#70D6FF" />
        <Navigation />
        <div className="landingbox">
          <h1 style={{ textAlign: 'center' }}>Active Games</h1>
          <div style={{ overflowY: 'scroll', maxHeight: '250px', marginBottom: '10px' }}>
            {Array.isArray(games.games)
              && games.games.map(game => (
                <div style={{ marginTop: '10px', marginBottom: '10px' }} key={game.id}>
                  <button
                    type="button"
                    onClick={this.onJoin}
                    value={game.id}
                    disabled={game.is_joinable === false}
                  >
                    join
                  </button>
                  <span>
                    {game.room_name}
                    , players:
                    {' '}
                  </span>
                  {game.users.map(user => (
                    <span key={user.username}>
                      {' '}
                      {user.username}
                      ,
                    </span>
                  ))}
                </div>
              ))}
          </div>
          <div style={{ display: 'flex' }}>
            <button type="button" style={{ width: '30%' }} onClick={this.onClick}>
              create game
            </button>
            <input
              value={roomName}
              onChange={event => this.setState({ roomName: event.target.value })}
              placeholder="room name"
              onKeyPress={this.onKeyPress}
              style={{ width: '100%' }}
            />
          </div>
        </div>
      </React.Fragment>
    );
  }
}

const s2p = state => ({
  games: state.games,
  loggedIn: state.auth.loggedIn,
});

Games.propTypes = {
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
  }).isRequired,
  dispatch: PropTypes.func,
  games: PropTypes.shape({
    id: PropTypes.number,
    game_status: PropTypes.string,
    room_name: PropTypes.string,
    users: PropTypes.shape({
      id: PropTypes.number,
      username: PropTypes.string,
    }),
  }),
  loggedIn: PropTypes.bool,
};

Games.defaultProps = {
  dispatch: PropTypes.func,
  games: PropTypes.null,
  loggedIn: PropTypes.bool,
};

export default WithAuth(connect(s2p)(Games));
