import React, {Component, Fragment} from 'react';

import MatchResult from './components/MatchResult';
import TweetLink from './components/TweetLink';
import VarietyMatchList from './components/VarietyMatchList';
import './App.css';

const username = window.username;

class App extends Component {
  constructor() {
    super();

    this.state = {
      varieties: window.varieties.map(variety => ({
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
        <VarietyMatchList
          varieties={this.state.varieties}
          onChange={this.handleChange}
        />

        <MatchResult
          varieties={this.state.varieties}
          username={username}
        />

        <TweetLink
          varieties={this.state.varieties}
          username={username}
        />
      </Fragment>
    );
  }
}

export default App;
