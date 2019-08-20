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
      if (authCompleted && loggedIn) {
        return <WrappedComponent {...this.props} />;
      }
      return <Redirect to="/" />;
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
