import React from 'react';
import {
  Button, TextInput, Grid, Grommet,
} from 'grommet';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Navigation from '../components/Navigation';
import { createGame, getGames } from '../modules/game';
import withAuth from '../hocs/authWrapper';
import Box from '../components/Box';
import HalfRectangle from '../images/Rectangle';

class Games extends React.Component {
  state = {
    roomName: '',
  };

  componentDidMount() {
    const { dispatch, loggedIn } = this.props;
    if (loggedIn) return dispatch(getGames());
  }

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

  render() {
    const { roomName } = this.state;
    const { games } = this.props;
    return (
      <React.Fragment>
        <HalfRectangle color="#70D6FF" />
        <Navigation />
        <Box>
          {Array.isArray(games.games)
            && games.games.map(game => (
              <div style={{ marginTop: '10px', marginBottom: '10px' }} key={game.id}>
                <button
                  style={{
                    borderRadius: '20px',
                    marginRight: '10px',
                    padding: '7px',
                    cursor: 'pointer',
                    border: '3px solid #44FFD1',
                    backgroundColor: '#44FFD1',
                  }}
                  onClick={this.onJoin}
                  value={game.id}
                  disabled={game.is_joinable === false}
                >
                  {' '}
                  join
                  {' '}
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
          <div style={{ flexWrap: 'wrap' }}>
            <button
              style={{
                borderRadius: '20px',
                marginRight: '10px',
                padding: '7px',
                cursor: 'pointer',
                border: '3px solid #44FFD1',
                backgroundColor: '#44FFD1',
              }}
              onClick={this.onClick}
            >
              create a new game
              {' '}
            </button>
            <input
              value={roomName}
              onChange={event => this.setState({ roomName: event.target.value })}
              placeholder="room name"
              style={{
                height: '30px',
                padding: '5px',
                border: 'none',
                borderRadius: '20px',
                marginTop: '5px',
              }}
            />
          </div>
        </Box>
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

export default withAuth(connect(s2p)(Games));
