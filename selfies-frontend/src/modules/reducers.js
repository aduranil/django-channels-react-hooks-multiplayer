import { combineReducers } from 'redux';
import { authReducer } from './account';
import { gameReducer } from './game';
import { websocketReducer } from './websocket';

const rootReducer = combineReducers({
  auth: authReducer,
  games: gameReducer,
  websocket: websocketReducer,
});

export default rootReducer;
