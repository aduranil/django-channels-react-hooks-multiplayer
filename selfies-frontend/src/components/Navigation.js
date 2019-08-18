import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { withRouter, Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import * as Cookies from 'js-cookie';
import { logoutUser, getCurrentUser } from '../modules/account';
import { leaveGame } from '../modules/game';

function Navigation({
  path, dispatch, history, loggedIn, inGame = false,
}) {
  const onLogout = async () => {
    await dispatch(logoutUser());
    return history.push('/loginorsignup');
  };

  const exitGame = async () => {
    await dispatch(leaveGame());
    history.push('/games');
  };

  useEffect(
    () => {
      if (Cookies.get('token')) {
        dispatch(getCurrentUser());
      }
    },
    [dispatch],
  );

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-Between',
        padding: '5px 1%',
      }}
    >
      <div>
        <Link to="/">
          <h3 style={{ paddingRight: '5px' }}>Selfies 2020 </h3>
        </Link>
      </div>
      <div>
        <div style={{ marginRight: '10px', display: 'inline-block' }}>
          {path !== 'rules' && (
            <Link to="/rules">
              <span>Rules </span>
            </Link>
          )}
        </div>

        <div style={{ marginRight: '10px', display: 'inline-block' }}>
          {path !== 'influencers' && (
            <Link to="/influencers">
              <span> Influencers </span>
            </Link>
          )}
        </div>

        <div style={{ display: 'inline-block' }}>
          {loggedIn
            && path === 'rules' && (
              <Link to="/games">
                {' '}
                <span>Games </span>
              </Link>
          )}
          {loggedIn
            && !inGame && (
              <button type="button" className="linkbutton" onClick={onLogout}>
                Logout
              </button>
          )}
          {loggedIn
            && inGame && (
              <button type="button" className="linkbutton" onClick={exitGame}>
                Exit Game
              </button>
          )}
          {!loggedIn
            && path !== 'login' && (
              <Link to="/signup">
                {' '}
                <span style={{ fontColor: 'black' }}>Signup </span>
              </Link>
          )}
        </div>
      </div>
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
