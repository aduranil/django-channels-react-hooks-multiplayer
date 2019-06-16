import React from 'react';
import {
  Button, TextInput, Grid, Box, Text, Grommet,
} from 'grommet';
import PropTypes from 'prop-types';
import { Gamepad } from 'grommet-icons';
import { connect } from 'react-redux';
import Navigation from '../components/Navigation';
import { createGame, getGames } from '../modules/game';
import withAuth from '../hocs/authWrapper';

const theme = {
  button: {
    padding: {
      horizontal: '6px',
    },
  },
};

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
        <Navigation />
        <Box
          round="xsmall"
          height="medium"
          margin="medium"
          width="600px"
          pad="medium"
          elevation="medium"
          background="accent-2"
          overflow={{ horizontal: 'hidden', vertical: 'scroll' }}
        >
          {Array.isArray(games.games)
            && games.games.map(game => (
              <Grid key={game.id} columns={{ count: 2 }}>
                <Grommet theme={theme}>
                  <Button
                    onClick={this.onJoin}
                    value={game.id}
                    margin={{ right: '5px', bottom: '5px' }}
                    label="join"
                  />
                  <Text>
                    {game.room_name}
                    , players:
                    {' '}
                  </Text>
                  {game.users.map(user => (
                    <Text key={user.username}>
                      {' '}
                      {user.username}
                    </Text>
                  ))}
                </Grommet>
              </Grid>
            ))}
        </Box>
        <Grid columns={{ count: 2, size: 'auto' }} gap="small">
          <TextInput
            placeholder="room name"
            value={roomName}
            onChange={event => this.setState({ roomName: event.target.value })}
          />
          <Button onClick={this.onClick} icon={<Gamepad />} label="Create new game" />
        </Grid>
      </React.Fragment>
    );
  }
}

const s2p = state => ({
  games: state.games,
  loggedIn: state.auth.loggedIn,
});

Games.propTypes = {
  history: PropTypes.object,
  dispatch: PropTypes.func,
  games: PropTypes.object,
  loggedIn: PropTypes.boolean,
};

Games.defaultProps = {
  history: PropTypes.object,
  dispatch: PropTypes.func,
  games: PropTypes.null,
  loggedIn: PropTypes.boolean,
};

export default withAuth(connect(s2p)(Games));
