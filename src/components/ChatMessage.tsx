import ChatbotIcon from "./ChatbotIcon";
import type { ChatItem } from "../app/page";

type Props = { chat: ChatItem };

export default function ChatMessage({ chat }: Props) {
  const isBot = chat.role === "model";
  return (
    <div className={`message ${isBot ? "bot" : "user"}-message`}>
      {isBot && <ChatbotIcon />}
      <p className="message-text">{chat.text}</p>
    </div>
  );
}
