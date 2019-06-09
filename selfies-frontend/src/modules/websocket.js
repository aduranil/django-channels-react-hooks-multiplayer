// Set up WebSocket handlers
// socket.onmessage = onMessage(socket, store);

export const WS_CONNECT = 'WS_CONNECT';
export const WS_CONNECTING = 'WS_CONNECTING';
export const WS_CONNECTED = 'WS_CONNECTED';
export const WS_DISCONNECT = 'WS_DISCONNECT';
export const WS_DISCONNECTED = 'WS_DISCONNECTED';
export const WS_HEALTH = 'WS_HEALTH';

export const wsConnect = host => ({ type: WS_CONNECT, host });
export const wsConnecting = host => ({ type: WS_CONNECTING, host });
export const wsConnected = host => ({ type: WS_CONNECTED, host });
export const wsDisconnect = host => ({ type: WS_DISCONNECT, host });
export const wsDisconnected = host => ({ type: WS_DISCONNECTED, host });
export const join = username => ({ type: 'join', username });
export const wsHealth = status => ({ type: WS_HEALTH, status });

const socketInitialState = { socket: null, user: null, users: [] };

const socketReducer = (state = { ...socketInitialState }, action) => {
  switch (action.type) {
    case 'join':
      return { ...state, users: [...state.users, action.username], user: action.username };
    case WS_HEALTH:
      return { ...state, status: action.status };
    case WS_CONNECT:
      return { ...state, host: action.host };
    case WS_CONNECTING:
      return { ...state, host: action.host };
    case WS_CONNECTED:
      return { ...state, host: action.host };
    case WS_DISCONNECTED:
      return { ...state, host: action.host };
    default:
      return state;
  }
};

export default socketReducer;
