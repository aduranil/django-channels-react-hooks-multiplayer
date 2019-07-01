const headers = {
  'Content-Type': 'application/json',
  Authorization: `Token ${localStorage.getItem('token')}`,
};

export const newMessage = msg => ({ type: 'NEW_MESSAGE', msg });
export const updateGame = json => ({ type: 'SET_GAME', data: json });
export const leaveGame = id => ({ type: 'LEAVE_GAME', id });
export const startRound = id => ({ type: 'START_ROUND', id });
const API_ROOT = 'http://localhost:8000';

export const createGame = roomName => dispatch => fetch(`${API_ROOT}/app/game/`, {
  method: 'POST',
  headers,
  body: JSON.stringify({ room_name: roomName }),
})
  .then(res => res.json())
  .then((json) => {
    dispatch({ type: 'SET_GAME', data: json });
    return `/game/${json.id}`;
  });

export const getGames = () => dispatch => fetch(`${API_ROOT}/app/games`, {
  method: 'GET',
  headers,
})
  .then(res => res.json())
  .then((json) => {
    dispatch({ type: 'SHOW_GAMES', data: json });
  });

export const getGame = id => dispatch => fetch(`${API_ROOT}/app/game/${id}`, {
  method: 'GET',
  headers,
})
  .then(res => res.json())
  .then((json) => {
    dispatch({ type: 'SET_GAME', data: json });
  });

const gameInitialState = {};

export const gameReducer = (state = { ...gameInitialState }, action) => {
  switch (action.type) {
    case 'LEAVE_GAME':
      return { ...state, users: [...state.users] };
    case 'SET_GAME':
      return { ...state, game: action.data };
    case 'SHOW_GAMES':
      return { ...state, games: action.data };
    default:
      return state;
  }
};
