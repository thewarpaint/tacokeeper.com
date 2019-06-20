import React, {Component, Fragment} from 'react';

import VarietyMatchList from './components/VarietyMatchList';
import {VARIETIES} from './varieties.config';
import './App.css';

class App extends Component {
  constructor() {
    super();

    this.state = {
      varieties: VARIETIES.map(variety => ({
        ...variety,
        isMatch: false,
      })),
    };
  }

  handleChange = (isChecked, variety) => {
    const varieties = [...this.state.varieties];
    const newVariety = {
      ...variety,
      isMatch: isChecked,
    };

    const varietyIndex = varieties.indexOf(variety);
    varieties[varietyIndex] = newVariety;

    this.setState({
      varieties,
    });
  };

  render() {
    return (
      <Fragment>
        <h1>TacoMatch</h1>

        <VarietyMatchList
          varieties={this.state.varieties}
          onChange={this.handleChange}
        />
      </Fragment>
    );
  }
}

export default App;
