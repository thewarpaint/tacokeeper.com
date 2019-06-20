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

                <div class="variety__text">
                  <div class="variety__name">
                    {variety.name}
                  </div>

                  <div class="variety__category">
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