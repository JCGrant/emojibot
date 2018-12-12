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

/**
 * Uses Twemoji to render the Emojis in a more pleasing manner.
 */
const Message = ({ kind, text }: IMessage) => (
  <div className={`message ${kind}`}>
    <Twemoji
      options={{
        className: 'twemoji',
        ext: '.svg',
        folder: 'svg',
      }}
    >
      {text}
    </Twemoji>
  </div>
);

/**
 * A Chat component with messages, user input, and a connection to a server.
 */
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
            <Message key={i} {...msg} />
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

  /**
   * Allows us to use the userInput in onKeyDown
   */
  private onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const userInput = e.target.value;
    this.setState({ userInput });
  };

  /**
   * When the user press Enter, we create a new message (if it's non-empty), and send
   * it to the server.
   */
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

  /**
   * Appends a message to the state and scrolls the window down to view it.
   */
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

  /**
   * Sends a message to the server and calls onResponse on the resulting text.
   */
  private sendMessage = (
    message: string,
    onResponse: (msg: IMessage) => void
  ) => {
    fetch(`/transform?s=${message}`)
      .then(res => res.text())
      .then(text => onResponse({ kind: 'received', name: 'bot', text }));
  };
}
