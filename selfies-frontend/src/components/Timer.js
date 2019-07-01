import React from 'react';

class Timer extends React.Component {
  state = {
    time: 0,
    start: 0,
    isOn: false,
  };

  startTimer = () => {
    this.setState({
      time: this.state.time,
      start: Date.now() - this.state.time,
      isOn: true,
    });
    this.timer = setInterval(
      () => this.setState({
        time: Date.now() - this.state.start,
      }),
      1,
    );
  };

  stopTimer = () => {
    this.setState({ isOn: false });
    clearInterval(this.timer);
  };

  resetTimer = () => {
    this.setState({ time: 0 });
  };

  render() {
    return (
      <div>
        <h3>{this.state.time}</h3>
      </div>
    );
  }
}

export default Timer;
