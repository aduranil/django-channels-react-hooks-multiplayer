import React from 'react';
import { Grommet, Box } from 'grommet';
import { Switch, Route } from 'react-router-dom';
import { connect } from 'react-redux';
import LoginOrSignup from './pages/LoginOrSignup';
import Entrance from './pages/Entrance';
import Signup from './pages/Signup';
import Games from './pages/Games';
import Game from './pages/Game';

const theme = {
  global: {
    font: {
      family: 'Luckiest Guy',
    },
  },
};

const App = () => (
  <Grommet theme={theme}>
    <Box
      justify="center"
      height="100%"
      align="center"
      padding={{ top: '20px' }}
      margin={{ horizontal: 'auto' }}
      round="xsmall"
    >
      <Switch>
        <Route exact path="/" component={Entrance} />
        <Route exact path="/games" component={Games} />
        <Route path="/game/:id" component={Game} />
        <Route exact path="/loginorsignup" component={LoginOrSignup} />
        <Route exact path="/signup" component={Signup} />
      </Switch>
    </Box>
  </Grommet>
);

export default connect()(App);
