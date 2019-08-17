import React from 'react';
import { connect } from 'react-redux';
import { startRound } from '../modules/game';

function GameInfo({ game, dispatch, time }) {
  const beginRound = () => {
    dispatch(startRound());
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        padding: '1%',
        justifyContent: 'center',
        marginRight: '5px',
      }}
    >
      {!game.round_started && (
        <button type="button" onClick={beginRound}>
          START GAME!
        </button>
      )}
      {game.round_started && (
        <div style={{ textAlign: 'center' }}>
          seconds left
          <br />
          <h1 className="entrance-title phone-time">{time}</h1>
        </div>
      )}
    </div>
  );
}

export default connect()(GameInfo);
