import * as actions from '../modules/websocket';
import { updateGame, updateTimer } from '../modules/game';

const socketMiddleware = (function () {
  let socket = null;

  /**
   * Handler for when the WebSocket opens
   */
  const onOpen = (ws, store, host) => (event) => {
    // Authenticate with Backend... somehow...
    console.log('websocket open');
    store.dispatch(actions.wsConnected(host));
  };

  /**
   * Handler for when the WebSocket closes
   */
  const onClose = (ws, store) => (event) => {
    store.dispatch(actions.wsDisconnected(event.host));
  };

  /**
   * Handler for when a message has been received from the server.
   */
  const onMessage = (ws, store) => (event) => {
    const payload = JSON.parse(event.data);

    switch (payload.type) {
      case 'update_game_players':
        store.dispatch(updateGame(payload.game));
        break;
      case 'update_timer':
        store.dispatch(updateTimer(payload.time));
        break;
      default:
        console.log('Received unknown server payload', payload);
        break;
    }
  };

  /**
   * Middleware
   */
  return store => next => (action) => {
    switch (action.type) {
      case 'WS_CONNECT':
        if (socket !== null) {
          socket.close();
        }

        // Pass action along
        next(action);

        // Tell the store that we're busy connecting...
        store.dispatch(actions.wsConnecting(action.host));

        // Attempt to connect to the remote host...
        socket = new WebSocket(action.host);

        // Set up WebSocket handlers
        socket.onmessage = onMessage(socket, store);
        socket.onclose = onClose(socket, store);
        socket.onopen = onOpen(socket, store, action.host);

        break;

      case 'WS_DISCONNECT':
        if (socket !== null) {
          socket.close();
        }
        socket = null;
        console.log('websocket closed');
        // Tell the store that we've been disconnected...
        store.dispatch(actions.wsDisconnected(action.host));

        break;

      case 'LEAVE_GAME':
        socket.send(
          JSON.stringify({ command: 'LEAVE_GAME', username: action.username, id: action.id }),
        );
        break;
      case 'NEW_MESSAGE':
        socket.send(JSON.stringify({ command: 'NEW_MESSAGE', message: action.msg }));
        break;
      case 'START_ROUND':
        socket.send(JSON.stringify({ command: 'START_ROUND', id: action.id }));
        break;
      case 'MAKE_MOVE':
        socket.send(JSON.stringify({ command: 'MAKE_MOVE', move: action.move }));
        break;
      default:
        return next(action);
    }
  };
}());

export default socketMiddleware;
