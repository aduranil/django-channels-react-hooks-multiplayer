import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import HalfRectangle from '../images/Rectangle';
import { getCurrentUser } from '../modules/account';

const Image = () => (
  <img
    className="animated rollIn"
    style={{
      width: '50%',
      minHeight: '100%',
      maxHeight: '100%',
      position: 'relative',
    }}
    src={require('../images/entrance-phone.svg')}
    alt="entrance-phone"
  />
);
const Entrance = ({ dispatch, loggedIn }) => {
  useEffect(() => {
    if (localStorage.getItem('token')) {
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
          width: '50%',
          padding: '1%',
          position: 'absolute',
          height: '50%',
          top: '0px',
          bottom: '0px',
          left: '0px',
          right: '0px',
          textAlign: 'center',
        }}
      >
        {loggedIn ? (
          <Link to="/games">
            <Image />
          </Link>
        ) : (
          <Link to="/signup">
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
