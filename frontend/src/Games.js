import React from 'react';
import {
  Button, TextInput, Grid, Box, Text, Grommet,
} from 'grommet';
import PropTypes from 'prop-types';
import { Gamepad } from 'grommet-icons';
import { connect } from 'react-redux';
import { logoutUser } from './modules/account';
import { createGame, getGames } from './modules/game';
import withAuth from './hocs/authWrapper';

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
    const { dispatch } = this.props;
    return dispatch(getGames());
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

  onLogout = () => {
    const { dispatch, history } = this.props;
    dispatch(logoutUser());
    history.push('/loginorsignup');
  };

  render() {
    const { roomName } = this.state;
    const { games } = this.props;
    return (
      <React.Fragment>
        <Grid alignSelf="center" columns={['medium', 'medium']}>
          <Text alignSelf="start"> SELFIES 2020 </Text>
          <Grommet theme={theme} style={{ textAlign: 'right' }}>
            <Button onClick={this.onLogout} label="logout" />
          </Grommet>
        </Grid>
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
          {games.games
            && games.games.map(game => (
              <Grid key={game.id} columns={{ count: 2 }}>
                <Grommet theme={theme}>
                  <Button
                    onClick={this.onJoin}
                    value={game.id}
                    margin={{ right: '5px', bottom: '5px' }}
                    label="join"
                  />
                  <Text>{game.room_name}</Text>
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
});

Games.propTypes = {
  history: PropTypes.object,
  dispatch: PropTypes.func,
  games: PropTypes.object,
};

Games.defaultProps = {
  history: PropTypes.object,
  dispatch: PropTypes.func,
  games: PropTypes.null,
};

export default withAuth(connect(s2p)(Games));
