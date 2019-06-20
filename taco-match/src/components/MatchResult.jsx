import React from 'react';

import {getMatchContent} from '../helpers';

const MatchResult = ({username, varieties}) => {
  return (
    <h2>{getMatchContent(varieties, username)}</h2>
  );
};

export default MatchResult;