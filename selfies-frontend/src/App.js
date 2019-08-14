import React from 'react';
import { Switch, Route } from 'react-router-dom';
import { connect } from 'react-redux';
import LoginOrSignup from './pages/LoginOrSignup';
import Entrance from './pages/Entrance';
import Games from './pages/Games';
import Game from './pages/Game';
import Rules from './pages/Rules';

const App = () => (
  <React.Fragment>
    <Switch>
      <Route exact path="/" component={Entrance} />
      <Route exact path="/games" component={Games} />
      <Route path="/game/:id" component={Game} />
      <Route exact path="/loginorsignup" component={LoginOrSignup} />
      <Route exact path="/signup" component={LoginOrSignup} />
      <Route exact path="/rules" component={Rules} />
    </Switch>
  </React.Fragment>
);

export default connect()(App);
