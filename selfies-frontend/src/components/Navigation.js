import React from 'react';
import {
  Grid, Text, Grommet, Button,
} from 'grommet';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { logoutUser } from '../modules/account';

const theme = {
  button: {
    padding: {
      horizontal: '6px',
    },
  },
};

class Navigation extends React.Component {
  onLogout = () => {
    const { dispatch, history } = this.props;
    dispatch(logoutUser());
    history.push('/loginorsignup');
  };

  render() {
    return (
      <Grid alignSelf="center" columns={['medium', 'medium']}>
        <Text alignSelf="start"> SELFIES 2020 </Text>
        <Grommet theme={theme} style={{ textAlign: 'right' }}>
          <Button onClick={this.onLogout} label="logout" />
        </Grommet>
      </Grid>
    );
  }
}

export default connect()(withRouter(Navigation));
