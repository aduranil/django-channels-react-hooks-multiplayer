import { combineReducers } from 'redux';
import { authReducer } from './account';
import { gameReducer } from './game';
import socketReducer from './websocket';

const rootReducer = combineReducers({
  auth: authReducer,
  games: gameReducer,
  socket: socketReducer,
});

export default rootReducer;
