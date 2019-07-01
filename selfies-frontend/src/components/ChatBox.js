import React from 'react';
import {
  Grid, Text, Grommet, Box, TextArea, Button,
} from 'grommet';
import { connect } from 'react-redux';
import { newMessage } from '../modules/game';

const theme = {
  button: {
    padding: {
      horizontal: '6px',
    },
  },
};

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
      <React.Fragment>
        <Box
          pad="medium"
          elevation="medium"
          background="accent-2"
          overflow={{ horizontal: 'hidden', vertical: 'scroll' }}
        >
          {game
            && game.messages.map(msg => (
              <Grid key={msg.id} columns={{ count: 2 }}>
                <Grommet theme={theme}>
                  <Text>
                    {' '}
                    {msg.message_type === 'action' ? null : `${msg.user.username}: `}
                    {msg.message}
                  </Text>
                </Grommet>
              </Grid>
            ))}
          <div
            style={{ float: 'left', clear: 'both' }}
            ref={(el) => {
              this.messagesEnd = el;
            }}
          />
        </Box>
        <Box pad="medium" elevation="medium" background="accent-2">
          <Grid gap="small" columns={['small', 'xsmall']}>
            <Box>
              <TextArea onChange={this.handleChange} value={message} />
            </Box>
            <Box justify="center" align="center" alignContent="center">
              <Button onClick={this.handleSubmit} label="send" />
            </Box>
          </Grid>
        </Box>
      </React.Fragment>
    );
  }
}

export default connect()(ChatBox);
