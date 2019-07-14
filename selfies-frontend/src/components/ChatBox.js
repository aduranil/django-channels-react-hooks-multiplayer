import React from 'react';
import { connect } from 'react-redux';
import { newMessage } from '../modules/game';

class ChatBox extends React.Component {
  state = {
    message: '',
  };

  componentDidUpdate() {
    this.scrollToBottom();
  }

  scrollToBottom = () => {
    this.messagesEnd.scrollIntoView({ behavior: 'smooth' });
  };

  handleChange = (e) => {
    const { value } = e.target;
    this.setState({ message: value });
  };

  handleSubmit = () => {
    const { dispatch } = this.props;
    const { message } = this.state;
    dispatch(newMessage(message));
    this.setState({ message: '' });
  };

  render() {
    const { message } = this.state;
    const { game } = this.props;
    return (
      <div className="chatbox" style={{ horizontal: 'hidden', vertical: 'scroll' }}>
        {game
          && game.messages.map(msg => (
            <div key={msg.id}>
              <span>
                {' '}
                {msg.message_type === 'action' ? null : `${msg.username}: `}
                {msg.message}
              </span>
            </div>
          ))}
        <div
          style={{ float: 'left', clear: 'both' }}
          ref={(el) => {
            this.messagesEnd = el;
          }}
        />
        <div>
          <div>
            <input onChange={this.handleChange} value={message} />
            <button type="button" onClick={this.handleSubmit}>
              send
              {' '}
            </button>
          </div>
        </div>
      </div>
    );
  }
}

export default connect()(ChatBox);
