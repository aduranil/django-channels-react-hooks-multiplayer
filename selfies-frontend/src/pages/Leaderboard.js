import React, { useEffect, useState } from 'react';
import Navigation from '../components/Navigation';

const API_ROOT = process.env.REACT_APP_HOST;

function Influencers() {
  const [influencers, setInfluencers] = useState('');

  const getLeaderboard = () => fetch(`${API_ROOT}/app/leaderboard/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then(res => res.json())
    .then((json) => {
      setInfluencers(json);
    });

  useEffect(() => {
    getLeaderboard();
  }, []);

  return (
    <React.Fragment>
      <Navigation path="influencers" />
      <div
        style={{
          padding: '2%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {' '}
        <h1 style={{ textAlign: 'center', paddingBottom: '5%' }}>Influencers</h1>
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-Between',
            width: '50%',
          }}
        >
          <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-Between' }}>
            <div>
              {' '}
              <h3>Rank</h3>
            </div>
            <div>
              {' '}
              <h3>Player</h3>
            </div>
            <div>
              {' '}
              <h3>Followers </h3>
            </div>
          </div>
          {influencers
            && influencers.map((influencer, index) => (
              <div
                key={influencer}
                style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-Between' }}
              >
                <div>
                  {' '}
                  {index + 1}
                </div>
                <div>
                  {' '}
                  {influencer.username}
                </div>
                <div>
                  {' '}
                  {influencer.followers}
                  {' '}
                </div>
              </div>
            ))}
        </div>
      </div>
    </React.Fragment>
  );
}

export default Influencers;
