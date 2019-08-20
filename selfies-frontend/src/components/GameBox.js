import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import useMoveUpdate from '../hooks/CurrentMove';

const Phone = () => (
  <img
    className="animated rollIn phone-game"
    src={require('../images/purpleiphone.png')}
    alt="entrance-phone"
  />
);

function GameBox({
  game, dispatch, time, currentPlayer,
}) {
  const [currentMove, newMove] = useMoveUpdate(dispatch, time);

  return (
    <React.Fragment>
      <div
        style={{
          background: '#ff70a6',
          boxShadow: '0 2px 10px 0 rgba(0, 0, 0, 0.5), inset 0 1px 3px 0 rgba(0, 0, 0, 0.5)',
          borderRadius: '20px',
          flexGrow: '1',
          padding: '2%',
        }}
      >
        <div
          className="phone-gamebox"
          style={{
            display: 'flex',
            flexWrap: 'wrap',
          }}
        >
          {['post_selfie', 'dont_post', 'go_live'].map(item => (
            <button
              className={currentMove === item ? 'button-color' : null}
              key={item}
              type="button"
              value={item}
              onClick={newMove}
              style={{ marginRight: '3px', marginBottom: '2px' }}
              disabled={
                (item === 'post_selfie' && currentPlayer && currentPlayer.selfies === 0)
                || (item === 'go_live' && currentPlayer && currentPlayer.go_live === 0)
                || !game.round_started
                || (currentPlayer && currentPlayer.loser === true)
              }
            >
              {item.replace(/_/g, ' ')}
            </button>
          ))}
        </div>
        <div
          style={{
            display: 'flex',
            flexDirection: 'row',
            flexWrap: 'wrap',
          }}
        >
          {game.users.map(player => (
            <div
              style={{ margin: '1%', display: 'flex', flexDirection: 'column' }}
              key={player.username}
            >
              <div>
                {player.username}
                {!game.round_started && (player.started ? '!' : ' ?')}
              </div>
              {['leave_comment', 'dislike', 'call_iphone'].map(item => (
                <div key={item} style={{ marginBottom: '5px' }}>
                  <button
                    onClick={newMove}
                    id={player.id}
                    style={{ width: '100%' }}
                    disabled={
                      !game.round_started || player.loser || (currentPlayer && currentPlayer.loser)
                    }
                    value={`${item}_${player.id}`}
                    className={
                      currentMove === `${item}_${player.id}` ? 'button-color' : 'gamebutton'
                    }
                    type="button"
                  >
                    {item.replace(/_/g, ' ')}
                    {' '}
                  </button>
                </div>
              ))}

              <Phone />

              {!player.loser && (
                <div>
                  {player.followers}
                  {' '}
                  {player.followers === 1 ? 'follower' : 'followers'}
                </div>
              )}
              {currentPlayer && currentPlayer.id === player.id && (
                <React.Fragment>
                  <div style={{ marginBottom: '3px' }}>
                    {player.selfies}
                    {' '}
                    {player.selfies === 1 ? 'selfie' : 'selfies'}
                  </div>
                  <div style={{ marginBottom: '3px' }}>
                    {player.go_live}
                    {' '}
                    {player.go_live === 1 ? 'go live' : 'go lives'}
                  </div>
                </React.Fragment>
              )}
            </div>
          ))}
        </div>
      </div>
    </React.Fragment>
  );
}

GameBox.propTypes = {
  dispatch: PropTypes.func.isRequired,
  game: PropTypes.shape({
    id: PropTypes.number.isRequired,
    game_status: PropTypes.string.isRequired,
    is_joinable: PropTypes.bool.isRequired,
    room_name: PropTypes.string.isRequired,
    round_started: PropTypes.bool.isRequired,
    users: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        followers: PropTypes.number.isRequired,
        selfies: PropTypes.number.isRequired,
        username: PropTypes.string.isRequired,
        started: PropTypes.bool.isRequired,
      }),
    ),
    messages: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        username: PropTypes.string.isRequired,
        message: PropTypes.string.isRequired,
        message_type: PropTypes.string.isRequired,
        created_at: PropTypes.string.isRequired,
      }),
    ),
  }),
};

GameBox.defaultProps = {
  game: PropTypes.null,
};

export default connect()(GameBox);
