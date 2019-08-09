// const API_ROOT = 'https://selfies-2020.herokuapp.com';
const API_ROOT = process.env.REACT_APP_HOST;

const status = async (res) => {
  if (!res.ok) {
    const response = await res.json();
    throw new Error(response);
  }
  return res;
};

export const getCurrentUser = () => dispatch => fetch(`${API_ROOT}/app/user/`, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Token ${localStorage.getItem('token')}`,
  },
})
  .then(status)
  .then(res => res.json())
  .then((json) => {
    dispatch({ type: 'SET_CURRENT_USER', data: json });
  })
  .catch(e => dispatch({ type: 'SET_ERROR', data: e.message }));

export const removeError = () => ({ type: 'REMOVE_ERROR' });

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
  .catch(e => dispatch({ type: 'SET_ERROR', data: e.message }));

export const handleSignup = jsonData => dispatch => fetch(`${API_ROOT}/app/users/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
  body: JSON.stringify(jsonData),
})
  .then(status)
  .then(res => res.json())
  .then((json) => {
    localStorage.setItem('token', json.token);
    dispatch({ type: 'SET_CURRENT_USER', data: json });
  })
  .catch(e => dispatch({ type: 'SET_ERROR', data: e.message }));

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
    default:
      return state;
  }
};
