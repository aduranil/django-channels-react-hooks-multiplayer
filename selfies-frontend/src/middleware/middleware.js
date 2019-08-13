import * as actions from '../modules/websocket';
import { updateGame, updateTimer } from '../modules/game';

const socketMiddleware = () => {
  let socket = null;

  const onOpen = store => (event) => {
    store.dispatch(actions.wsConnected(event.target.url));
  };

  const onClose = store => () => {
    store.dispatch(actions.wsDisconnected());
  };

  const onMessage = store => (event) => {
    const payload = JSON.parse(event.data);
    switch (payload.type) {
      case 'update_game_players':
        store.dispatch(updateGame(payload.game, payload.current_player));
        break;
      case 'update_timer':
        store.dispatch(updateTimer(payload.time));
        break;
      default:
        break;
    }
  };

  return store => next => (action) => {
    switch (action.type) {
      case 'WS_CONNECT':
        if (socket !== null) {
          socket.close();
        }

        // connect to the remote host
        socket = new WebSocket(action.host);

        // websocket handlers
        socket.onmessage = onMessage(store);
        socket.onclose = onClose(store);
        socket.onopen = onOpen(store);

        break;
      case 'WS_DISCONNECT':
        if (socket !== null) {
          socket.close();
        }
        socket = null;
        break;
      case 'LEAVE_GAME':
        socket.send(JSON.stringify({ command: 'LEAVE_GAME' }));
        break;
      case 'NEW_MESSAGE':
        socket.send(JSON.stringify({ command: 'NEW_MESSAGE', message: action.msg }));
        break;
      case 'START_ROUND':
        socket.send(JSON.stringify({ command: 'START_ROUND' }));
        break;
      case 'MAKE_MOVE':
        socket.send(
          JSON.stringify({
            command: 'MAKE_MOVE',
            move: action.move,
            victim: action.victim,
          }),
        );
        break;
      default:
        console.log(action);
        return next(action);
    }
  };
};

export default socketMiddleware();
