const headers = {
  'Content-Type': 'application/json',
  Authorization: `Token ${localStorage.getItem('token')}`,
};

const API_ROOT = 'http://localhost:8000';
export const setMessages = messages => ({ type: 'SET_MESSAGES', messages });

export const getMessages = id => dispatch => fetch(`${API_ROOT}/app/messages/${id}`, {
  method: 'GET',
  headers,
})
  .then(res => res.json())
  .then((json) => {
    dispatch({ type: 'SET_MESSAGES', messages: json });
  });

export const newMessage = msg => ({ type: 'NEW_MESSAGE', msg });

const messageInitialState = { messages: [] };

export const messageReducer = (state = { ...messageInitialState }, action) => {
  switch (action.type) {
    case 'SET_MESSAGES':
      return { ...state, messages: action.messages };
    default:
      return state;
  }
};
