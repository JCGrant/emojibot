import * as React from 'react';

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
      messages: [
        { kind: 'received', name: 'bot', text: 'BEEP BOOP' },
        { kind: 'sent', name: 'user', text: 'Hey!' },
        { kind: 'received', name: 'bot', text: 'BEEP BOOP' },
        { kind: 'sent', name: 'user', text: 'Haha, nice!' },
      ],
      userInput: '',
    };
  }

  public render() {
    return (
      <div className="chat">
        <div className="messages">
          {this.state.messages.map(msg => (
            <div className={`message ${msg.kind}`}>{msg.text}</div>
          ))}
          <div ref={this.messagesEnd} />
        </div>
        <input
          className="user-input"
          value={this.state.userInput}
          onChange={this.onChange}
          onKeyPress={this.onKeyDown}
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
      this.setState(
        state => ({
          messages: [
            ...state.messages,
            { kind: 'sent', name: 'user', text: this.state.userInput },
          ],
          userInput: '',
        }),
        () => {
          this.messagesEnd.current!.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'start',
          });
        }
      );
    }
  };
}
