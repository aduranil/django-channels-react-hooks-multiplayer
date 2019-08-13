import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import { makeMove } from '../modules/game';

function GameMoves({
  game, dispatch, time, currentPlayer,
}) {
  const [currentMove, setCurrentMove] = useState('');
  useEffect(
    () => {
      if (time === '90') {
        setCurrentMove(null);
      }
    },
    [time],
  );

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
        <button
          className={currentMove === 'post_selfie' ? 'button-color' : null}
          type="button"
          style={{ padding: '10px' }}
          value="post_selfie"
          onClick={newMove}
          disabled={!game.round_started}
        >
          post a selfie
        </button>
        <button
          className={currentMove === 'post_group_selfie' ? 'button-color' : null}
          type="button"
          value="post_group_selfie"
          style={{ padding: '10px' }}
          onClick={newMove}
          disabled={!game.round_started}
        >
          post group selfie
          {!game.round_started}
        </button>
        <button
          type="button"
          className={currentMove === 'post_story' ? 'button-color' : null}
          disabled={currentPlayer && currentPlayer.stories === 0}
          value="post_story"
          style={{ padding: '10px' }}
          onClick={newMove}
          disabled={!game.round_started}
        >
          post story
        </button>
        <button
          className={currentMove === 'dont_post' ? 'button-color' : null}
          type="button"
          value="dont_post"
          style={{ padding: '10px' }}
          onClick={newMove}
          disabled={!game.round_started}
        >
          {"don't post"}
        </button>
        <button
          className={currentMove === 'go_live' ? 'button-color' : null}
          type="button"
          value="go_live"
          style={{ padding: '10px' }}
          onClick={newMove}
          disabled={!game.round_started}
        >
          go live
        </button>
        {' '}
      </React.Fragment>
    </div>
  );
}

export default connect()(GameMoves);
