import { combineReducers } from 'redux';
import { authReducer } from './account';
import { gameReducer } from './game';

const rootReducer = combineReducers({
  auth: authReducer,
  games: gameReducer,
});

export default rootReducer;
