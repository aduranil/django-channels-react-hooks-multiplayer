import React, { useState, useEffect, useRef } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { newMessage } from '../modules/game';

function ChatBox({ game, dispatch }) {
  let messagesRef = useRef();
  const [message, setMessage] = useState('');
  useEffect(() => {
    messagesRef.scrollIntoView({ behavior: 'smooth' });
  });

  const handleSubmit = () => {
    dispatch(newMessage(message));
    setMessage('');
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        background: '#70d6ff',
        boxShadow: '0 2px 10px 0 rgba(0, 0, 0, 0.5), inset 0 1px 3px 0 rgba(0, 0, 0, 0.5)',
        borderRadius: '20px',
        marginRight: '1%',
        marginLeft: '1%',
        marginBottom: '1%',
        marginTop: '1%',
        padding: '2%',
        maxHeight: '500px',
        width: '40%',
      }}
    >
      <h3 style={{ textAlign: 'center' }}>Group Chat</h3>
      <div
        style={{
          overflowY: 'scroll',
          marginRight: '2px',
          minHeight: '350px',
          maxHeight: '350px',
        }}
      >
        {game.messages.map(msg => (
          <div key={msg.id}>
            <span>
              {' '}
              {msg.message_type === 'action' ? null : `${msg.username}: `}
              {msg.message}
            </span>
          </div>
        ))}
        <div style={{ float: 'left', clear: 'both' }} ref={el => (messagesRef = el)} />
      </div>
      <div
        style={{
          display: 'flex',
          marginTop: '5px',
          width: '100%',
        }}
      >
        <input
          style={{ width: '100%', marginRight: '10px' }}
          onChange={e => setMessage(e.target.value)}
          value={message}
          onKeyPress={e => e.key === 'Enter' && handleSubmit()}
        />
        <button style={{ width: '10%' }} type="button" onClick={handleSubmit}>
          send
          {' '}
        </button>
      </div>
    </div>
  );
}

ChatBox.propTypes = {
  dispatch: PropTypes.func.isRequired,
  game: PropTypes.shape({
    id: PropTypes.number.isRequired,
    game_status: PropTypes.string.isRequired,
    is_joinable: PropTypes.bool.isRequired,
    room_name: PropTypes.string.isRequired,
    round_started: PropTypes.bool.isRequired,
    users: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        followers: PropTypes.number.isRequired,
        stories: PropTypes.number.isRequired,
        username: PropTypes.string.isRequired,
        started: PropTypes.bool.isRequired,
      }),
    ),
    messages: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        username: PropTypes.string.isRequired,
        message: PropTypes.string.isRequired,
        message_type: PropTypes.string.isRequired,
        created_at: PropTypes.string.isRequired,
      }),
    ),
  }),
};

ChatBox.defaultProps = {
  game: PropTypes.null,
};

export default connect()(ChatBox);
