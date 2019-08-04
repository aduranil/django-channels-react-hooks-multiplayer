![SELFIES](https://i.imgur.com/0oZKbIf.png)

## About

Every girl starts with 0 followers. The girl that gets to 100 followers first wins and wins an advertisement deal with flat tummy tea! Everyone else sets their account to private :(

how to run:

```
docker-compose up -d
cd selfies-frontend
yarn start
```

![game_screen](https://thepracticaldev.s3.amazonaws.com/i/2nict69l0gvu0b79kiz1.png)

![all_games](https://thepracticaldev.s3.amazonaws.com/i/43ot9t2h2lt4ogexfllw.png)

## Moves

Post a selfie - move that gains 10 followers. But if someone leaves a mean comment when you post a selfie, you lose 5 followers. If two girls leave a mean comment, you lose 10 followers, and so on.

Post a group selfie - if at least two people do a group photo, they both get 20 followers. But if someone leaves a sarcastic comment on their group photo, the girl who gets the sarcastic comment loses 15 followers. If you do a group selfie alone, its like a regular selfie.

Post a story - defensive move that can only be done 3 times. You gain 10 followers. People can’t post mean comments but if anyone went live while you posted a story, you dont get any followers because no one will see it and you wasted your story.

Go live - if you go live, every girl that posted a photo or story while you were live loses 15 followers. If two or more girls go live at the same time, they both lose 20 followers. The person going live gains 20.

Leave a sarcastic comment. - If you leave a mean comment on another girl’s photo, she loses 5 followers.

Dont post. - Nothing happens to you. Defense against Go Live and sarcastic comments.

If you don't move during a game, you automatically lose 5 followers. You lose an additional 10 followers if anyone leaves a mean comment while you do nothing.
