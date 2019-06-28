import { combineReducers } from 'redux';
import { authReducer } from './account';
import { gameReducer } from './game';
import { messageReducer } from './message';

const rootReducer = combineReducers({
  auth: authReducer,
  games: gameReducer,
  messages: messageReducer,
});

export default rootReducer;
