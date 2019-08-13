import React from 'react';
import { connect } from 'react-redux';
import { withRouter, Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import { logoutUser } from '../modules/account';
import { leaveGame } from '../modules/game';

function Navigation({
  dispatch, history, loggedIn, inGame,
}) {
  const onLogout = async () => {
    await dispatch(logoutUser());
    return history.push('/loginorsignup');
  };

  const exitGame = async () => {
    await dispatch(leaveGame());
    history.push('/games');
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-Between',
        padding: '5px 1%',
        // marginLeft: '5px',
      }}
    >
      {' '}
      <Link to="/">
        <h1 style={{ paddingRight: '5px' }}>Selfies 2020 </h1>
      </Link>
      {loggedIn
        && !inGame && (
          <button type="button" style={{ width: '5vw' }} onClick={onLogout}>
            logout
          </button>
      )}
      {loggedIn
        && inGame && (
          <button type="button" onClick={exitGame}>
            leave game
          </button>
      )}
    </div>
  );
}

const s2p = state => ({
  loggedIn: state.auth.loggedIn,
});

Navigation.propTypes = {
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
  }).isRequired,
  dispatch: PropTypes.func.isRequired,
  loggedIn: PropTypes.bool,
  inGame: PropTypes.bool,
};

Navigation.defaultProps = {
  loggedIn: PropTypes.undefined,
  inGame: PropTypes.undefined,
};
export default connect(s2p)(withRouter(Navigation));
