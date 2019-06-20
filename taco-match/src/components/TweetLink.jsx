import React from 'react';

import {getMatchText} from '../helpers';

const tacoKeeperUrl = 'https://tacokeeper.com';
const twitterIntentUrl = 'https://twitter.com/intent/tweet';

function getTweetHref(varieties, username) {
  const tweetText = getMatchText(varieties, username);
  const tweetContent = `${tweetText} #tacomatch #tacokeeper ${tacoKeeperUrl}/${username}/taco-match`;

  return `${twitterIntentUrl}?text=${encodeURIComponent(tweetContent)}`;
}

const TweetLink = ({username, varieties}) => {
  return (
    <div className="tweet-link-wrapper">
      <a href={getTweetHref(varieties, username)}
         className="tweet-link"
         target="_blank"
         rel="noopener noreferrer">Comparte en Twitter</a>
    </div>
  );
};

export default TweetLink;
