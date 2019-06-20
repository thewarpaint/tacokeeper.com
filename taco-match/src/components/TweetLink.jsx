import React from 'react';

import {getMatchText} from '../helpers';

const tacoKeeperUrl = 'https://tacokeeper.com';
const twitterIntentUrl = 'https://twitter.com/intent/tweet';

function getMatchedVarietiesText(varieties) {
  const conjunctionText = ' y ';
  const matchedVarieties = varieties
    .filter(variety => variety.isMatch)
    .map(variety => variety.name);

  // Works for arrays with length 0 (empty string), 1 ('first'), or 2 ('first and second')
  if (matchedVarieties.length < 3) {
    return matchedVarieties.join(conjunctionText);
  }

  return matchedVarieties.slice(0, matchedVarieties.length - 1).join(', ') +
    conjunctionText +
    matchedVarieties.slice(-1);
}

function getTweetHref(varieties, username) {
  let tweetContent = `${getMatchText(varieties, username)} Coincidimos en: ${getMatchedVarietiesText(varieties)} `;
  tweetContent += `#tacomatch #tacokeeper ${tacoKeeperUrl}/${username}/taco-match`;

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
