import React from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import PropTypes from 'prop-types';
import { logoutUser } from '../modules/account';

function Navigation({ dispatch, history, loggedIn }) {
  const onLogout = async () => {
    await dispatch(logoutUser());
    return history.push('/loginorsignup');
  };

  return (
    <div className="container">
      <h1 style={{ paddingRight: '5px' }}> Selfies 2020 </h1>
      {loggedIn && (
        <button type="button" style={{ width: '100px' }} onClick={onLogout}>
          logout
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
};

Navigation.defaultProps = {
  loggedIn: PropTypes.undefined,
};
export default connect(s2p)(withRouter(Navigation));
