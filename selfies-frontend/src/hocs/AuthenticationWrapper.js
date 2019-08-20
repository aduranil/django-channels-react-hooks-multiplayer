import React from 'react';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import PropTypes from 'prop-types';
import * as Cookies from 'js-cookie';
import { getCurrentUser } from '../modules/account';

const WithAuth = (WrappedComponent) => {
  class AuthedComponent extends React.Component {
    state = {
      authCompleted: this.props.loggedIn,
    };

    componentDidMount() {
      const { dispatch } = this.props;
      if (Cookies.get('token')) {
        dispatch(getCurrentUser());
      }
    }

    componentWillReceiveProps(nextProps) {
      if (nextProps.loggedIn) {
        this.setState({ authCompleted: true });
      } else {
        this.setState({ authCompleted: false });
      }
    }

    render() {
      const { authCompleted } = this.state;
      const { loggedIn } = this.props;
      if (authCompleted) {
        return loggedIn && <WrappedComponent {...this.props} />;
      }
      return (
        <React.Fragment>
          <h1
            className="animated infinite bounce"
            style={{
              textAlign: 'center',
              margin: 'auto',
              position: 'absolute',
              height: '100px',
              width: '100px',
              top: '0px',
              bottom: '0px',
              left: '0px',
              right: '0px',
            }}
          >
            Loading
          </h1>
        </React.Fragment>
      );
    }
  }

  AuthedComponent.propTypes = {
    loggedIn: PropTypes.bool,
    dispatch: PropTypes.func.isRequired,
  };

  AuthedComponent.defaultProps = {
    loggedIn: PropTypes.null,
  };

  const s2p = state => ({
    loggedIn: state.auth.loggedIn,
  });

  return connect(s2p)(AuthedComponent);
};

export default WithAuth;
