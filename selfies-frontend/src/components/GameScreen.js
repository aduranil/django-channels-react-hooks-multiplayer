import React from 'react';
import { Box, Grid } from 'grommet';
import Timer from './Timer';
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
    <Timer />
    <Grid gap="small" columns="100px" justify="center">
      {game
        && game.users.map(player => (
          <Box key={player.id}>
            {player.username}
            {player.started ? ' !' : ' ?'}
            <Phone />
            {' '}
          </Box>
        ))}
    </Grid>
  </Box>
);

export default GameView;
