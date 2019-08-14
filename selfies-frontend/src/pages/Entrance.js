import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import HalfRectangle from '../images/Rectangle';
import { EntrancePhone } from '../images/EntrancePhone';
import { Message } from '../images/iMessage';

const Entrance = () => (
  <div>
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
      <div
        style={{
          background: '#ff70a6',
          boxShadow: '0 2px 10px 0 rgba(0, 0, 0, 0.5), inset 0 1px 3px 0 rgba(0, 0, 0, 0.5)',
          borderRadius: '20px',
          margin: '30px auto 100px auto',
          width: '50%',
          padding: '1%',
        }}
      >
        <div
          style={{
            textAlign: 'center',
            marginTop: '15px',
            position: 'relative',
            marginBottom: '15px',
          }}
        >
          <div className="rollIn animated">
            <Link to="/signup">
              <div
                style={{
                  top: '35%',
                  left: '32.5%',
                  width: '215px',
                  minWidth: '215px',
                  height: '30%',
                  borderRadius: '15px',
                  backgroundColor: 'white',
                  opacity: '0.5',
                  position: 'absolute',
                  alignSelf: 'center',
                  overflow: 'hidden',
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
  </div>
);

export default connect()(Entrance);
