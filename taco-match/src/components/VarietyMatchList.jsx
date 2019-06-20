import React from 'react';

const VarietyMatchList = ({onChange, varieties}) => {
	return (
		<ul className="variety-match-list">
      {
        varieties.map(variety => {
          return (
            <li key={variety.name}>
              <label>
                <input
                  type="checkbox"
                  checked={variety.isMatch}
                  onChange={(event) => onChange(event.target.checked, variety)}
                />
                {variety.name}
              </label>
            </li>
          );
        })
      }
    </ul>
	);
};

export default VarietyMatchList;