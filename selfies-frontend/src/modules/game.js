const headers = {
  'Content-Type': 'application/json',
  Authorization: `Token ${localStorage.getItem('token')}`,
};

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

const gameInitialState = { games: [] };

export const gameReducer = (state = { ...gameInitialState }, action) => {
  switch (action.type) {
    case 'SET_GAME':
      return { ...state, roomName: action.data.room_name };
    case 'SHOW_GAMES':
      return { ...state, games: action.data };
    default:
      return state;
  }
};
