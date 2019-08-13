import { useState, useEffect } from 'react';
import { makeMove } from '../modules/game';

function CurrentMoveUpdate(dispatch, time) {
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
  return [currentMove, newMove];
}

export default CurrentMoveUpdate;
