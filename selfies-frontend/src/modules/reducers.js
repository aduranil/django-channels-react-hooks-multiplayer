import { combineReducers } from 'redux';
import { authReducer } from './account';
import { gameReducer } from './game';
import { messageReducer } from './message';
import socketReducer from './websocket';

const rootReducer = combineReducers({
  auth: authReducer,
  games: gameReducer,
  socket: socketReducer,
  messages: messageReducer,
});

export default rootReducer;
