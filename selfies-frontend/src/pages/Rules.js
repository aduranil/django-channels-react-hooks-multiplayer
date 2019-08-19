import React from 'react';
import Navigation from '../components/Navigation';

function Rules() {
  return (
    <React.Fragment>
      <Navigation path="rules" />
      <div
        style={{
          padding: '2%',
        }}
      >
        {' '}
        <h1 style={{ textAlign: 'center' }}>Rules</h1>
        <h3> Gameplay</h3>
        <div className="rulespage">
          The goal is to be one of the last two girls standing with followers left. Use the chat to
          make strategic partnerships. The game starts when everyone clicks the 'START GAME' button.
          Each round is 90 seconds but the counter goes down to 10 seconds once everyone moves. You
          can change your move as many times as you want before the timer runs out. Three players
          are needed to start the round. The last two players win and get 100 followers. Each girl
          gets 10 followers for playing.
        </div>
        <h3> Moves </h3>
        <div className="rulespage">
          <b style={{ color: '#ff70a6' }}>Leave a Mean Comment.</b>
          {' '}
If you Leave a Mean Comment on
          another girl's social media, she loses 10 followers. It doesn't work if she selected
          "Don't Post" that round.
        </div>
        <div className="rulespage">
          <b style={{ color: '#ff70a6' }}>Dislike.</b>
          {' '}
When you Dislike a girl's social media, she
          loses 20 followers per disliker. It only works if two or more girls both Dislike the same
          girl. If one girl Dislikes, no damage occurs to the target.
        </div>
        <div className="rulespage">
          <b style={{ color: '#ff70a6' }}>Call iPhone.</b>
          {' '}
Blocks what another girl tried to do that
          turn. She cannot Dislike, Leave a Mean Comment, or Go Live because you're distracting her.
        </div>
        <div className="rulespage">
          <b style={{ color: '#ff70a6' }}>Go Live.</b>
          {' '}
All girls will lose 30 points when you Go
          Live. If two girl's Go Live at the same time, they both lose 30 points. You get two Go
          Live's per game.
        </div>
        <div className="rulespage">
          <b style={{ color: '#ff70a6' }}>Don't Post.</b>
          {' '}
Nothing happens to you. Defense against Go
          Live and Mean Comments. If you Don't Post twice in a row, the second time you lose 10
          followers if no one attacked you or went live.
        </div>
        <div className="rulespage">
          {' '}
          <b style={{ color: '#ff70a6' }}>Post a Selfie.</b>
          {' '}
Gives you twenty followers. If you Post
          a Selfie while someone is Going Live, there is no damage done to you. You get three
          selfies per game. It doesn't work if someone Calls your iPhone or Leaves a Mean Comment
          though, in which case you lose 0 and 20 followers, respectively, and are susceptible to Go
          Live damage.
        </div>
        {' '}
        <div className="rulespage">
          If you don't move during a game, you automatically lose 10 followers and are open to all
          attacks.
        </div>
        <h3>Support</h3>
        <div className="rulespage">
          Star this project on
          {' '}
          <a style={{ color: '#44ffd1' }} href="https://www.github.com/aduranil/selfies">
            github.
          </a>
          {' '}
          Email lina.rudashevski@gmail.com with any questions or comments. This game was inspired by
          {' '}
          <a style={{ color: '#44ffd1' }} href="http://play.sissyfight.com/main">
            {' '}
            sissyfight.
          </a>
        </div>
      </div>
    </React.Fragment>
  );
}

export default Rules;
