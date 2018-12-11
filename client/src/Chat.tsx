import * as React from 'react';
import Twemoji from 'react-twemoji';

interface IMessage {
  kind: 'sent' | 'received';
  name: string;
  text: string;
}

interface IChatState {
  userInput: string;
  messages: IMessage[];
}

export default class Chat extends React.Component<{}, IChatState> {
  private messagesEnd = React.createRef<HTMLDivElement>();

  constructor(props: {}) {
    super(props);
    this.state = {
      messages: [],
      userInput: '',
    };
  }

  public render() {
    return (
      <div className="chat">
        <div className="messages">
          {this.state.messages.map((msg, i) => (
            <div key={i} className={`message ${msg.kind}`}>
              <Twemoji
                options={{
                  className: 'twemoji',
                  ext: '.svg',
                  folder: 'svg',
                }}
              >
                {msg.text}
              </Twemoji>
            </div>
          ))}
          <div ref={this.messagesEnd} />
        </div>
        <input
          className="user-input"
          value={this.state.userInput}
          onChange={this.onChange}
          onKeyPress={this.onKeyDown}
          placeholder="Type something..."
        />
      </div>
    );
  }

  private onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const userInput = e.target.value;
    this.setState({ userInput });
  };

  private onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && this.state.userInput.length > 0) {
      this.sendMessage(this.state.userInput, this.addMessage);
      this.addMessage({
        kind: 'sent',
        name: 'user',
        text: this.state.userInput,
      });
      this.setState({ userInput: '' });
    }
  };

  private addMessage = (message: IMessage) => {
    this.setState(
      state => ({
        messages: [...state.messages, message],
      }),
      () => {
        this.messagesEnd.current!.scrollIntoView({
          behavior: 'smooth',
          block: 'nearest',
          inline: 'start',
        });
      }
    );
  };

  private sendMessage = (
    message: string,
    onResponse: (msg: IMessage) => void
  ) => {
    fetch(`/predict?s=${message}`)
      .then(res => res.text())
      .then(text => onResponse({ kind: 'received', name: 'bot', text }));
  };
}
