export type Emotion = 'neutral' | 'happy' | 'sad' | 'angry' | 'surprised';

export type ChatMessage = {
  role: 'user' | 'assistant';
  content: string;
  emotion?: Emotion;
};
