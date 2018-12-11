import * as React from 'react';
import './App.css';
import Chat from './Chat';

import logo from './logo.svg';

class App extends React.Component {
  public render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Emojibot</h1>
        </header>
        <Chat />
      </div>
    );
  }
}

export default App;
