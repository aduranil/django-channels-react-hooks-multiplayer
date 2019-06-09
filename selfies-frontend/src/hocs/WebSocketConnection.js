import React, { Component } from 'react';
import { connect } from 'react-redux';
import { wsConnect, wsHealth } from '../modules/websocket';

class WebSocketConnection extends Component {
  constructor(props) {
    super(props);
    this.autoconnect = !!props.autoconnect;
  }

  componentDidMount() {
    if (this.autoconnect) {
      this.props.wsConnect(this.props.host);
    }
  }

  render() {
    return <div>{this.props.children}</div>;
  }
}

const mapStateToProps = state => ({
  wsEvents: state.socket,
});

const mapDispatchToProps = { wsConnect, wsHealth };

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(WebSocketConnection);
