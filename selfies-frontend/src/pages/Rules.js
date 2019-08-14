import React from 'react';
import Navigation from '../components/Navigation';

function Rules() {
  return (
    <React.Fragment>
      <Navigation path="rules" />
      <div style={{ padding: '1%' }}>
        {' '}
        <h1 style={{ textAlign: 'center' }}>Rules</h1>
        <div>
          {' '}
          Post a selfie - move that gains 10 followers. But if someone leaves a mean comment when
          you post a selfie, you lose 5 followers. If two girls leave a mean comment, you lose 10
          followers, and so on.
        </div>
        {' '}
        <div>
          Post a group selfie - if at least two people do a group photo, they both get 20 followers.
          But if someone leaves a sarcastic comment on their group photo, the girl who gets the
          sarcastic comment loses 15 followers. If you do a group selfie alone, its like a regular
          selfie.
        </div>
        <div>
          Post a story - defensive move that can only be done 3 times. You gain 10 followers. People
          can’t post mean comments but if anyone went live while you posted a story, you dont get
          any followers because no one will see it and you wasted your story.
        </div>
        <div>
          Go live - if you go live, every girl that posted a photo or story while you were live
          loses 15 followers. If two or more girls go live at the same time, they both lose 20
          followers. The person going live gains 20.
        </div>
        <div>
          Leave a sarcastic comment. - If you leave a mean comment on another girl’s photo, she
          loses 5 followers.
        </div>
        <div>
          Dont post. - Nothing happens to you. Defense against Go Live and sarcastic comments.
        </div>
        <div>
          If you don't move during a game, you automatically lose 5 followers. You lose an
          additional 10 followers if anyone leaves a mean comment while you do nothing.
        </div>
      </div>
    </React.Fragment>
  );
}

export default Rules;
