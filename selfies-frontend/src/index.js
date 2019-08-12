import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { createStore, applyMiddleware, compose } from 'redux';
import { Provider } from 'react-redux';
import reduxThunk from 'redux-thunk';
import rootReducer from './modules/reducers';
import wsMiddleware from './middleware/middleware';
import App from './App';
import ErrorBoundary from './Error';
import './App.css';

const middleware = [reduxThunk, wsMiddleware];
const store = createStore(
  rootReducer,
  compose(
    applyMiddleware(...middleware),
    // window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__(),
  ),
);
const Root = ({ store }) => (
  <Router>
    <ErrorBoundary>
      <Provider store={store}>
        <Route path="/" component={App} />
      </Provider>
    </ErrorBoundary>
  </Router>
);

ReactDOM.render(<Root store={store} />, document.getElementById('root'));
