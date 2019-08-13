import React, { useEffect, useRef } from 'react';
import { connect } from 'react-redux';

function RoundHistory({ game }) {
  let messagesNewRef = useRef();
  useEffect(() => {
    messagesNewRef.scrollIntoView({ behavior: 'smooth' });
  });

  return (
    <div
      style={{
        background: '#ff70a6',
        display: 'flex',
        flexDirection: 'column',
        boxShadow: '0 2px 10px 0 rgba(0, 0, 0, 0.5), inset 0 1px 3px 0 rgba(0, 0, 0, 0.5)',
        borderRadius: '20px',
        padding: '2%',
        // width: '60vw',
        height: '100%',
        maxHeight: '100%',
      }}
    >
      {' '}
      <h3 style={{ textAlign: 'center' }}>Round History</h3>
      <div
        style={{
          overflowY: 'scroll',
          marginTop: '5px',
          minHeight: '30vh',
          maxHeight: '40vh',
        }}
      >
        {!game.round_started && (
          <React.Fragment>
            <div key="instruction">
              <span> Click on any player's iPhone during gameplay to leave a mean comment</span>
            </div>
            <div key="exclamation">
              <span> When the ? turns to !, that means the player has started</span>
            </div>
          </React.Fragment>
        )}
        {game.round_history.map(msg => (
          <div key={msg.id}>
            <span>{msg.message}</span>
          </div>
        ))}
        <div style={{ float: 'left', clear: 'both' }} ref={el => (messagesNewRef = el)} />
      </div>
    </div>
  );
}

export default connect()(RoundHistory);
