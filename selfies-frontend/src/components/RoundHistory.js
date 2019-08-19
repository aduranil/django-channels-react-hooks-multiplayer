import React, { useEffect, useRef } from 'react';
import { connect } from 'react-redux';

function RoundHistory({ game }) {
  const messagesNewRef = useRef(null);
  useEffect(() => {
    messagesNewRef.current.scrollIntoView(false);
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
        height: '36vh',
      }}
    >
      {' '}
      <h3 style={{ textAlign: 'center' }}>News Feed</h3>
      <div
        style={{
          overflowY: 'scroll',
          marginTop: '5px',
        }}
      >
        {!game.round_started && (
          <React.Fragment>
            {' '}
            <div key="exclamation">
              <span style={{ color: 'white' }}>
                {' '}
                ◆ When the ? turns to !, that means the player has started 👸🏾
              </span>
            </div>
            <div key="time">
              <span style={{ color: 'white' }}>
                {' '}
                ◆ There are 90 seconds per round. The timer goes down to 10 seconds once everyone
                has moved 👠
              </span>
            </div>
          </React.Fragment>
        )}
        {game.round_history.map(msg => (
          <div key={msg.id}>
            <span>{msg.message}</span>
          </div>
        ))}
        <div style={{ float: 'left', clear: 'both' }} ref={messagesNewRef} />
      </div>
    </div>
  );
}

export default connect()(RoundHistory);
