import { useState } from 'react';
import type { ChatMessage, Emotion } from './types';
import './App.css';

const API_URL = 'http://localhost:8000/chat';

const getAssistantAvatar = (emotion: Emotion = 'neutral') => {
  switch (emotion) {
    case 'happy':
      return '/avatars/ai_happy.png';
    case 'sad':
      return '/avatars/ai_sad.png';
    case 'angry':
      return '/avatars/ai_angry.png';
    case 'surprised':
      return '/avatars/ai_surprised.png';
    default:
      return '/avatars/ai_neutral.png';
  }
};

const getUserAvatar = () => {
  return '/avatars/user_default.png';
};

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const newUserMessage: ChatMessage = {
      role: 'user',
      content: input.trim(),
    };

    const newMessages = [...messages, newUserMessage];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages }),
      });

      if (!res.ok) throw new Error('API error');

      const data: { reply: string; emotion?: Emotion } = await res.json();

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: data.reply,
        emotion: data.emotion ?? 'neutral',
      };

      setMessages([...newMessages, assistantMessage]);
    } catch {
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'エラーが発生しちゃったみたい…(コンソールを見てね)',
        emotion: 'sad',
      };
      setMessages([...newMessages, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className='app-wrapper'>
      <div className='app'>
        <header className='app-header'>
          <div className='app-title'>
            <span className='logo-dot' />
            <h1>My AI Chat</h1>
          </div>
          <span className='app-subtitle'>Python + React</span>
        </header>

        <main className='chat-layout'>
          <section className='chat-card'>
            <div className='chat-window'>
              {messages.length === 0 && (
                <div className='chat-empty'>
                  こんにちは 👋
                  <br />
                  AI とゆるっとおしゃべりしてみよう。
                </div>
              )}

              {messages.map((m, idx) => (
                <div
                  key={idx}
                  className={`chat-row ${
                    m.role === 'user' ? 'is-user' : 'is-ai'
                  }`}
                >
                  <div className='avatar'>
                    <img
                      className='avatar-img'
                      src={
                        m.role === 'user'
                          ? getUserAvatar()
                          : getAssistantAvatar(m.emotion ?? 'neutral')
                      }
                      alt={m.role === 'user' ? 'User' : 'Assistant'}
                    />
                  </div>
                  <div className='bubble'>{m.content}</div>
                </div>
              ))}

              {loading && (
                <div className='chat-row is-ai'>
                  <div className='avatar talking'>
                    <img
                      className='avatar-img'
                      src={getAssistantAvatar('neutral')}
                      alt='Assistant'
                    />
                  </div>
                  <div className='bubble bubble-typing'>
                    <span />
                    <span />
                    <span />
                  </div>
                </div>
              )}
            </div>

            <form
              className='input-area'
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
            >
              <textarea
                className='message-input'
                placeholder='メッセージを入力してね（Shift+Enterで改行）'
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
              />
              <button
                className='send-button'
                type='submit'
                disabled={loading || !input.trim()}
              >
                {loading ? '送信中…' : '送信'}
              </button>
            </form>
          </section>
        </main>
      </div>
    </div>
  );
}

export default App;
