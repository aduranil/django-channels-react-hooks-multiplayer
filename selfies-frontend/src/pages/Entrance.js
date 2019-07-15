import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import HalfRectangle from '../images/Rectangle';
import { EntrancePhone } from '../images/EntrancePhone';
import { Message } from '../images/iMessage';
import './App.scss';

class Entrance extends React.Component {
  render() {
    return (
      <div style={{ minWidth: '100vw', minHeight: '100vh' }}>
        <HalfRectangle color="#70D6FF" />
        <div style={{ textAlign: 'center' }}>
          <span className="entrance-title">Selfies 2020</span>
        </div>
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            minWidth: '100vw',
            minHeight: '80vh',
          }}
        >
          <div className="landing-page-wrapper">
            <div
              style={{
                textAlign: 'center',
                marginTop: '15px',
                position: 'relative',
                marginBottom: '15px',
              }}
            >
              <Link to="/loginorsignup">
                <div
                  style={{
                    top: '35%',
                    left: '37.6%',
                    width: '25%',
                    height: '14%',
                    borderRadius: '15px',
                    backgroundColor: 'white',
                    opacity: '0.5',
                    position: 'absolute',
                    alignSelf: 'center',
                  }}
                >
                  <Message />
                </div>
              </Link>
              <EntrancePhone />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

Entrance.propTypes = {
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
  }).isRequired,
  loggedIn: PropTypes.bool,
};

Entrance.defaultProps = {
  loggedIn: PropTypes.null,
};
const mapStateToProps = state => ({
  loggedIn: state.auth.loggedIn,
});

export default connect(mapStateToProps)(Entrance);
