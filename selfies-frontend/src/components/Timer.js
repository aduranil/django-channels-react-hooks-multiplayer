import React from 'react';
import { Text } from 'grommet';
import { connect } from 'react-redux';

class Timer extends React.Component {
  state = {
    time: 0,
    start: 0,
    isOn: false,
  };

  startTimer = () => {
    console.log('timer started');
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

  componentDidUpdate(prevProps) {
    const { game } = this.props;
    console.log(prevProps);
    console.log(game);
    if (
      game
      && prevProps.game
      && game.round_started
      && game.round_started !== prevProps.game.round_started
    ) {
      this.startTimer();
    }
  }

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
        <Text>{this.state.time}</Text>
      </div>
    );
  }
}

const s2p = (state, ownProps) => ({
  game: state.games.game,
});

export default connect(s2p)(Timer);
