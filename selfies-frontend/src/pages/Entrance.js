import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import * as Cookies from 'js-cookie';
import HalfRectangle from '../images/Rectangle';
import { getCurrentUser } from '../modules/account';

const Image = () => (
  <img
    className="animated rollIn"
    style={{ width: '60%', height: '100%', display: 'inline' }}
    src={require('../images/entrancephone.png')}
    alt="entrance-phone"
  />
);
const Entrance = ({ dispatch, loggedIn }) => {
  useEffect(() => {
    if (Cookies.get('token')) {
      dispatch(getCurrentUser());
    }
  }, [dispatch]);
  return (
    <div>
      <HalfRectangle color="#70D6FF" />
      <div style={{ textAlign: 'center' }}>
        <span className="entrance-title">Selfies 2020</span>
      </div>
      <div
        className="phone-entrance"
        style={{
          background: '#ff70a6',
          boxShadow: '0 2px 10px 0 rgba(0, 0, 0, 0.5), inset 0 1px 3px 0 rgba(0, 0, 0, 0.5)',
          borderRadius: '20px',
          margin: 'auto',
          width: '60%',
          padding: '1%',
          position: 'absolute',
          height: '60%',
          top: '0px',
          bottom: '0px',
          left: '0px',
          right: '0px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {loggedIn ? (
          <Link
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}
            to="/games"
          >
            <Image />
          </Link>
        ) : (
          <Link
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}
            to="/signup"
          >
            <Image />
          </Link>
        )}
      </div>
    </div>
  );
};

const s2p = state => ({
  loggedIn: state.auth.loggedIn,
});

export default connect(s2p)(Entrance);
