import React from 'react';
import { Phone } from '../images/iPhone';

const GameView = ({ game }) => (
  <div style={{ display: 'flex', flexDirection: 'row' }}>
    {game
      && game.users.map(player => (
        <div style={{ margin: '1%' }} key={player.username}>
          {player.username}
          {player.started ? ' !' : ' ?'}
          <div>
            {player.followers}
            {' '}
followers
          </div>
          <div>
            {player.stories}
            {' '}
stories
          </div>
          <Phone />
          {' '}
        </div>
      ))}
  </div>
);

export default GameView;
