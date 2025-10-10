"use client";
import { useRef } from "react";
import type { ChatItem } from "../app/page";

type ChatFormProps = {
  setChatHistory: React.Dispatch<React.SetStateAction<ChatItem[]>>;
  generateBotResponse: (
    history: ChatItem[],
    setChat: React.Dispatch<React.SetStateAction<ChatItem[]>>
  ) => void;
};

export default function ChatForm({ setChatHistory, generateBotResponse }: ChatFormProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const userMessage = inputRef.current?.value.trim();
    if (!userMessage) return;

    // En una sola actualización:
    // 1) agrega el mensaje del usuario
    // 2) agrega el placeholder del bot
    // 3) dispara la generación de respuesta con el "history" ya actualizado
    setChatHistory((prev) => {
      const next: ChatItem[] = [
        ...prev,
        { role: "user", text: userMessage },
        { role: "model", text: "Pensando..." },
      ];
      generateBotResponse(next, setChatHistory);
      return next;
    });

    // limpia input
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <form action="#" className="chat-form" onSubmit={handleFormSubmit}>
      <input
        ref={inputRef}
        type="text"
        placeholder="Responder..."
        className="message-input"
        required
      />
      <button type="submit" className="material-symbols-outlined">
        keyboard_arrow_up
      </button>
    </form>
  );
}
