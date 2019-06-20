import React from 'react';

import {getMatchText} from '../helpers';

const MatchResult = ({username, varieties}) => {
  return (
    <h2>{getMatchText(varieties, username)}</h2>
  );
};

export default MatchResult;