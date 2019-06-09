const headers = {
  'Content-Type': 'application/json',
  Authorization: `Token ${localStorage.getItem('token')}`,
};

const API_ROOT = 'http://localhost:8000';

export const getCurrentUser = () => dispatch => fetch(`${API_ROOT}/app/user/`, {
  method: 'GET',
  headers,
})
  .then(res => res.json())
  .then(json => dispatch({ type: 'SET_CURRENT_USER', data: json }));

function status(res) {
  if (!res.ok) {
    throw new Error(res.statusText);
  }
  return res;
}

export const handleLogin = data => dispatch => fetch(`${API_ROOT}/app/login/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
  body: JSON.stringify(data),
})
  .then(status)
  .then(res => res.json())
  .then((json) => {
    localStorage.setItem('token', json.token);
    return dispatch({ type: 'SET_CURRENT_USER', data: json });
  })
  .catch((e) => {
    dispatch({ type: 'SET_ERROR', data: e.message });
  });

export const handleSignup = jsonData => dispatch => fetch(`${API_ROOT}/app/users/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
  body: JSON.stringify(jsonData),
})
  .then(res => res.json())
  .then((json) => {
    localStorage.setItem('token', json.token);
    return dispatch({ type: 'SET_CURRENT_USER', data: json });
  });

export const logoutUser = () => (dispatch) => {
  localStorage.removeItem('token');
  return dispatch({ type: 'LOGOUT_USER' });
};

const initialState = {};

export const authReducer = (state = { ...initialState }, action) => {
  switch (action.type) {
    case 'SET_CURRENT_USER':
      return {
        ...state,
        loggedIn: true,
        username: action.data.username,
        errorMessage: null,
      };
    case 'LOGOUT_USER':
      return { ...state, loggedIn: false, username: null };
    case 'SET_ERROR':
      return { ...state, errorMessage: action.data };
    default:
      return state;
  }
};
