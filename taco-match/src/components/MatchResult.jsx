import React from 'react';

function getMatchPercent(varieties) {
	return varieties
		.filter(variety => variety.isMatch)
		.reduce((acc, variety) => acc + variety.weight, 0);
}

const MatchResult = ({username, varieties}) => {
	return (
		<h2>
			¡Soy un {getMatchPercent(varieties)}% tacompatible con @{username}!
		</h2>
	);
};

export default MatchResult;