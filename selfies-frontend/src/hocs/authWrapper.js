import React from 'react';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import { getCurrentUser } from '../modules/account';

const withAuth = (WrappedComponent) => {
  class AuthedComponent extends React.Component {
    state = {
      authCompleted: this.props.loggedIn,
    };

    componentDidMount = async () => {
      if (localStorage.getItem('token')) {
        await this.props.dispatch(getCurrentUser());
      } else {
        this.setState({ authCompleted: true });
      }
    };

    componentWillReceiveProps(nextProps) {
      if (nextProps.loggedIn) {
        this.setState({ authCompleted: true });
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
