function getMatchPercent(varieties) {
  return varieties
    .filter(variety => variety.isMatch)
    .reduce((acc, variety) => acc + variety.weight, 0);
}

export function getMatchText(varieties, username) {
	return `¡Soy un ${getMatchPercent(varieties)}% tacompatible con @${username}!`;
}