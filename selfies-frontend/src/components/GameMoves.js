import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import { makeMove } from '../modules/game';

function GameMoves({
  game, dispatch, time, currentPlayer,
}) {
  const [currentMove, setCurrentMove] = useState('');
  useEffect(() => {
    if (time === '90') {
      setCurrentMove(null);
    }
  }, [time]);

  const newMove = (event) => {
    event.preventDefault();
    let move = event.currentTarget.value;
    let theVictim = null;
    // only the comment game move has another player that it impacts
    if (event.currentTarget.value.includes('leave_comment')) {
      move = 'leave_comment';
      theVictim = event.currentTarget.id;
      // victim = event.currentTarget.id;
    }
    setCurrentMove(event.currentTarget.value);
    dispatch(
      makeMove({
        move,
        victim: theVictim,
      }),
    );
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        marginRight: '5px',
        padding: '1%',
        maxHeight: '50vh',
        width: '15vw',
        justifyContent: 'space-Between',
      }}
    >
      <React.Fragment>
        {['post_selfie', 'post_group_selfie', 'post_story', 'dont_post', 'go_live'].map(item => (
          <button
            className={currentMove === item ? 'button-color' : null}
            type="button"
            style={{ padding: '10px' }}
            value={item}
            onClick={newMove}
            disabled={!game.round_started}
          >
            {item.replace(/_/g, ' ')}
          </button>
        ))}
        {' '}
      </React.Fragment>
    </div>
  );
}

export default connect()(GameMoves);
