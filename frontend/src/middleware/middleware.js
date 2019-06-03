import * as client_actions from '../modules/WSClientActions';
import * as server_actions from '../modules/WSServerActions';
import { join } from '../modules/websocket';

const socketMiddleware = (function () {
  let socket = null;

  /**
   * Handler for when the WebSocket opens
   */
  const onOpen = (ws, store, host) => (event) => {
    // Authenticate with Backend... somehow...
    console.log('websocket open');
    store.dispatch(client_actions.wsConnected(host));
  };

  /**
   * Handler for when the WebSocket closes
   */
  const onClose = (ws, store) => (event) => {
    store.dispatch(client_actions.wsDisconnected(event.host));
  };

  /**
   * Handler for when a message has been received from the server.
   */
  const onMessage = (ws, store) => (event) => {
    const payload = JSON.parse(event.data);

    switch (payload.type) {
      case server_actions.WS_HEALTH:
        store.dispatch(server_actions.wsHealth(status));
        break;
      case 'join':
        store.dispatch(join(payload.username));
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
      case client_actions.WS_CONNECT:
        if (socket !== null) {
          socket.close();
        }

        // Pass action along
        next(action);

        // Tell the store that we're busy connecting...
        store.dispatch(client_actions.wsConnecting(action.host));

        // Attempt to connect to the remote host...
        socket = new WebSocket(action.host);

        // Set up WebSocket handlers
        socket.onmessage = onMessage(socket, store);
        socket.onclose = onClose(socket, store);
        socket.onopen = onOpen(socket, store, action.host);

        break;

      case client_actions.WS_DISCONNECT:
        if (socket !== null) {
          socket.close();
        }
        socket = null;

        // Tell the store that we've been disconnected...
        store.dispatch(client_actions.wsDisconnected(action.host));

        break;

      // case 'join':
      //   socket.send(JSON.stringify({ command: 'join', username: action.username, id: action.id }));
      //   console.log('sent', action.username, action.id);
      //   break;
      default:
        return next(action);
    }
  };
}());

export default socketMiddleware;
