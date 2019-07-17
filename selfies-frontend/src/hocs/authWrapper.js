import React from 'react';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import { getCurrentUser } from '../modules/account';

const withAuth = (WrappedComponent) => {
  class AuthedComponent extends React.Component {
    state = {
      authCompleted: this.props.loggedIn,
    };

    componentDidMount() {
      if (localStorage.getItem('token')) {
        this.props.dispatch(getCurrentUser());
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
        return loggedIn ? <WrappedComponent {...this.props} /> : <Redirect to="/loginorsignup" />;
      }
      return <React.Fragment>Loading</React.Fragment>;
    }
  }

  const mapStateToProps = state => ({
    loggedIn: state.auth.loggedIn,
  });

  return connect(mapStateToProps)(AuthedComponent);
};

export default withAuth;
