import React, { useEffect, useRef } from 'react';
import { connect } from 'react-redux';

function RoundHistory({ game }) {
  let messagesNewRef = useRef();
  useEffect(() => {
    messagesNewRef.scrollIntoView(false);
  }, []);

  return (
    <div
      style={{
        background: '#ff70a6',
        boxShadow: '0 2px 10px 0 rgba(0, 0, 0, 0.5), inset 0 1px 3px 0 rgba(0, 0, 0, 0.5)',
        borderRadius: '20px',
        marginLeft: '1%',
        marginRight: '1%',
        marginTop: '1%',
        width: '98%',
        padding: '1%',
        minHeight: '150px',
        maxHeight: '150px',
      }}
    >
      {' '}
      <h3 style={{ textAlign: 'center' }}>
        {' '}
        {game.room_name}
        {' '}
Round History
      </h3>
      <div
        style={{
          overflowY: 'scroll',
          marginRight: '2px',
          minHeight: '100px',
          maxHeight: '100px',
        }}
      >
        {game.round_history.map(msg => (
          <div key={msg.id}>
            <span>{msg.message}</span>
          </div>
        ))}
        <div ref={el => (messagesNewRef = el)} />
      </div>
    </div>
  );
}

export default connect()(RoundHistory);
