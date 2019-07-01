import React from 'react';
import { Box, Grid } from 'grommet';
import { Phone } from '../images/iPhone';

const GameView = ({ game }) => (
  <Box
    width="800px"
    height="500px"
    round="xsmall"
    pad="medium"
    elevation="medium"
    background="accent-2"
  >
    <Grid gap="small" columns="100px" justify="center">
      {game
        && game.users.map(player => (
          <Box key={player.username}>
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
          </Box>
        ))}
    </Grid>
  </Box>
);

export default GameView;
