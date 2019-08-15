import React from 'react';
import Navigation from '../components/Navigation';

function Rules() {
  return (
    <React.Fragment>
      <Navigation path="rules" />
      <div
        style={{
          padding: '2%',
          height: '95vh',
          width: '100vw',
          overflow: 'scroll',
        }}
      >
        {' '}
        <h1 style={{ textAlign: 'center' }}>Rules</h1>
        <h3> Gameplay</h3>
        <div className="rulespage">
          The goal of the game is to get to 100 followers first. Use the chat to make strategic
          partnerships. The game starts when everyone clicks the 'START GAME' button. Each round is
          90 seconds but the counter goes down to 10 seconds once everyone moves. You can change
          your move as many times as you want before the timer runs out.
        </div>
        <h3> Moves </h3>
        <div className="rulespage">
          {' '}
          <b style={{ color: '#ff70a6' }}>Post a selfie</b>
          . Move that gains 10 followers. But if someone leaves a mean comment when you post a
          selfie, you lose 5 followers. If two girls leave a mean comment, you lose 10 followers,
          and so on.
        </div>
        {' '}
        <div className="rulespage">
          <b style={{ color: '#ff70a6' }}>Post a group selfie.</b>
          {' '}
If at least two people do a group
          photo, they both get 20 followers. But if someone leaves a sarcastic comment on their
          group photo, the girl who gets the sarcastic comment loses 15 followers. If you do a group
          selfie alone, its like a regular selfie.
        </div>
        <div className="rulespage">
          <b style={{ color: '#ff70a6' }}>Post a story.</b>
          {' '}
Defensive move that can only be done 3
          times. You gain 10 followers. People can’t post mean comments but if anyone went live
          while you posted a story, you dont get any followers because no one will see it and you
          wasted your story.
        </div>
        <div className="rulespage">
          <b style={{ color: '#ff70a6' }}>Go live.</b>
          {' '}
If you go live, every girl that posted a
          photo or story while you were live loses 15 followers. If two or more girls go live at the
          same time, they both lose 20 followers. The person going live gains 20.
        </div>
        <div className="rulespage">
          <b style={{ color: '#ff70a6' }}>Leave a sarcastic comment.</b>
          {' '}
If you leave a mean comment
          on another girl’s photo, she loses 5 followers. Click on any girl's iPhone to leave a mean
          comment.
        </div>
        <div className="rulespage">
          <b style={{ color: '#ff70a6' }}>Dont post.</b>
          {' '}
Nothing happens to you. Defense against Go
          Live and sarcastic comments.
        </div>
        <div className="rulespage">
          If you don't move during a game, you automatically lose 5 followers. You lose an
          additional 10 followers if anyone leaves a mean comment while you do nothing.
        </div>
        <h3>Support</h3>
        <div className="rulespage">
          Star this project on
          {' '}
          <a style={{ color: '#44ffd1' }} href="github.com/aduranil/selfies">
            github.
          </a>
          {' '}
          Email lina.rudashevski@gmail.com with any questions or comments.
        </div>
      </div>
    </React.Fragment>
  );
}

export default Rules;
