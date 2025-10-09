"use client"; // importante para usar useRef o cualquier hook

import { useRef } from "react";

export default function ChatForm() {
  const inputRef = useRef<HTMLInputElement | null>(null);

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const userMessage = inputRef.current?.value.trim();
    if (!userMessage) return;

    console.log(userMessage);

    // Limpia el input después de enviar
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
