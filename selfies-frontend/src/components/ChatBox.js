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
        <div style={{ display: 'flex' }}>
          <input
            style={{ width: '100%', marginRight: '5px' }}
            onChange={this.handleChange}
            value={message}
          />
          <button style={{ width: '20%' }} type="button" onClick={this.handleSubmit}>
            send
            {' '}
          </button>
        </div>
      </div>
    );
  }
}

export default connect()(ChatBox);
