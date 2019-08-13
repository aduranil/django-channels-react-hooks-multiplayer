import React from 'react';
import { connect } from 'react-redux';
import CurrentMoveUpdate from '../hooks/CurrentMove';

function GameMoves({
  game, dispatch, time, currentPlayer,
}) {
  const [currentMove, newMove] = CurrentMoveUpdate(dispatch, time);

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
    </div>
  );
}

export default connect()(GameMoves);
