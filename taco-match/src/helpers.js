import React, {Fragment} from 'react';

function getMatchPercent(varieties) {
  return varieties
    .filter(variety => variety.isMatch)
    .reduce((acc, variety) => acc + variety.weight, 0);
}

function getMatchPercentClass(matchPercent) {
  let matchPercentClass;

  if (matchPercent >= 75) {
    matchPercentClass = 'match-result--high';
  } else if (matchPercent >= 35) {
    matchPercentClass = 'match-result--medium';
  } else {
    matchPercentClass = 'match-result--low';
  }

  return `match-result ${matchPercentClass}`;
}

export function getMatchText(varieties, username) {
  return `¡Soy un ${getMatchPercent(varieties)}% tacompatible con @${username}!`;
}

export function getMatchContent(varieties, username) {
   const matchPercent = getMatchPercent(varieties);

  return (
    <Fragment>
      ¡Soy un <b className={getMatchPercentClass(matchPercent)}>{matchPercent}%</b> tacompatible con @{username}!
    </Fragment>
  );
}