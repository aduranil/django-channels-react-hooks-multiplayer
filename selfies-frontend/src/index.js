import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import App from './App';
import ErrorBoundary from './Error';
import './App.scss';
import store from './modules/store';

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
