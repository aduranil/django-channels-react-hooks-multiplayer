import { useState, useEffect } from 'react';
import { makeMove } from '../modules/game';

function useMoveUpdate(dispatch, time) {
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
    if (event.currentTarget.value.includes('leave_comment')) {
      move = 'leave_comment';
      theVictim = event.currentTarget.id;
    }
    if (event.currentTarget.value.includes('dislike')) {
      move = 'dislike';
      theVictim = event.currentTarget.id;
    }
    if (event.currentTarget.value.includes('call_iphone')) {
      move = 'call_iphone';
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

export default useMoveUpdate;
