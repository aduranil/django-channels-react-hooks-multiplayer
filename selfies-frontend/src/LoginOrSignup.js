import React from "react";
import { Box, Text } from "grommet";
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { handleLogin } from "./modules/account";
import Login from "./components/LoginOrSignup";

class LoginOrSignup extends React.Component {
  state = {
    email: "",
    password: ""
  };

  handleChange = e => {
    const { name } = e.target;
    const { value } = e.target;
    this.setState(prevstate => {
      const newState = { ...prevstate };
      newState[name] = value;
      return newState;
    });
  };

  handleSubmit = async () => {
    const { dispatch, history } = this.props;
    await dispatch(handleLogin(this.state));
    history.push("/games");
  };

  render() {
    const { username, email, password } = this.state;
    return (
      <React.Fragment>
        <Box
          gap="medium"
          width="medium"
          elevation="medium"
          pad="medium"
          round="small"
          margin="15px"
        >
          <Text textAlign="center" color="white" margin={{ left: "small" }}>
            NEW USERS
          </Text>
          <Text margin={{ left: "small" }}>
            Click <Link to="/signup">here</Link> to create your user!
          </Text>
        </Box>
        <Box width="medium" elevation="medium" pad="medium" round="small">
          <Text textAlign="center" color="white" margin={{ left: "small" }}>
            RETURNING USERS
          </Text>
          <Login
            fromLoginOrSignup
            username={username}
            password={password}
            email={email}
            handleChange={this.handleChange}
            handleSubmit={this.handleSubmit}
          />
        </Box>
      </React.Fragment>
    );
  }
}

LoginOrSignup.propTypes = {
  history: PropTypes.object,
  dispatch: PropTypes.func
};

LoginOrSignup.defaultProps = {
  history: PropTypes.object,
  dispatch: PropTypes.func
};
export default connect()(LoginOrSignup);
