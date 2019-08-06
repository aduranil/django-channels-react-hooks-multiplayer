export const newMessage = msg => ({ type: 'NEW_MESSAGE', msg });
export const updateGame = (json, player) => ({ type: 'SET_GAME', data: json, player });
export const leaveGame = () => ({ type: 'LEAVE_GAME' });
export const startRound = () => ({ type: 'START_ROUND' });
export const updateTimer = time => ({ type: 'UPDATE_TIMER', time });
export const makeMove = move => ({ type: 'MAKE_MOVE', move });
// const API_ROOT = 'https://selfies-2020.herokuapp.com';
const API_ROOT = 'http://localhost:8000';

export const createGame = roomName => dispatch => fetch(`${API_ROOT}/app/game/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Token ${localStorage.getItem('token')}`,
  },
  body: JSON.stringify({ room_name: roomName }),
})
  .then(res => res.json())
  .then((json) => {
    dispatch({ type: 'SET_GAME', data: json });
    return `/game/${json.id}`;
  });

export const getGames = () => dispatch => fetch(`${API_ROOT}/app/games`, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Token ${localStorage.getItem('token')}`,
  },
})
  .then(res => res.json())
  .then((json) => {
    dispatch({ type: 'SHOW_GAMES', data: json });
  });

export const getGame = id => dispatch => fetch(`${API_ROOT}/app/game/${id}`, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Token ${localStorage.getItem('token')}`,
  },
})
  .then(res => res.json())
  .then((json) => {
    dispatch({ type: 'SET_GAME', data: json });
  });

const gameInitialState = { time: null };

export const gameReducer = (state = { ...gameInitialState }, action) => {
  switch (action.type) {
    case 'SET_GAME':
      return { ...state, game: action.data, currentPlayer: action.player };
    case 'SHOW_GAMES':
      return { ...state, games: action.data };
    case 'UPDATE_TIMER':
      return { ...state, time: action.time };
    default:
      return state;
  }
};
