import React from 'react';

const VarietyMatchList = ({onChange, varieties}) => {
	return (
		<ul className="variety-match-list">
      {
        varieties.map(variety => {
          return (
            <li key={variety.name}
                className="variety">
              <label className="variety__label">
                <input
                  type="checkbox"
                  className="variety__input"
                  checked={variety.isMatch}
                  onChange={(event) => onChange(event.target.checked, variety)}
                />

                <div className="variety__text">
                  <div className="variety__name">
                    {variety.name}
                  </div>

                  <div className="variety__category">
                    {variety.category}
                  </div>
                </div>
              </label>
            </li>
          );
        })
      }
    </ul>
	);
};

export default VarietyMatchList;