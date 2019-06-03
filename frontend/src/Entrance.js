import React from 'react';
import { Text } from 'grommet';
import { connect } from 'react-redux';

class Entrance extends React.Component {
  componentDidMount() {
    const { loggedIn, history } = this.props;
    if (loggedIn) {
      history.push('/games');
    }
  }

  render() {
    return (
      <React.Fragment>
        <Text color="accent-1" size="77px">
          SELFIES 2020
        </Text>
        <a href="/loginorsignup">
          <img alt="Door" src={require('./images/Door.png')} />
        </a>
      </React.Fragment>
    );
  }
}

const mapStateToProps = state => ({
  loggedIn: state.auth.loggedIn,
});

export default connect(mapStateToProps)(Entrance);
