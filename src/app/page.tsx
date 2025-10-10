"use client";
import { useState, useRef, useEffect } from "react";
import ChatbotIcon from "../components/ChatbotIcon";
import ChatForm from "../components/ChatForm";
import ChatMessage from "../components/ChatMessage";

export type ChatItem = {
  role: "user" | "model";
  text: string;
};

export default function Page() {
  const [chatHistory, setChatHistory] = useState<ChatItem[]>([]);
  const [showChatbot, setShowChatbot] = useState(false);
  const chatBodyRef = useRef<HTMLDivElement | null>(null);

  // Genera la respuesta del bot y reemplaza el "Pensando..."
  const generateBotResponse = (
    history: ChatItem[],
    setChat: React.Dispatch<React.SetStateAction<ChatItem[]>>
  ) => {
    const lastUser =
      [...history].reverse().find((m) => m.role === "user")?.text ?? "";

    setTimeout(() => {
      setChat((prev) => {
        const idx = [...prev]
          .map((m, i) => ({ m, i }))
          .reverse()
          .find(({ m }) => m.role === "model" && m.text === "Pensando...")?.i;

        if (idx === undefined) return prev;

        const updated = [...prev];
        updated[idx] = { role: "model", text: `¡Listo! Respuesta para: "${lastUser}"` };
        return updated;
      });
    }, 900);
  };

  // Auto-scroll al final si hay cambios y el chat está visible
  useEffect(() => {
    if (!showChatbot) return;
    const el = chatBodyRef.current;
    if (!el) return;
    el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
  }, [chatHistory, showChatbot]);

  return (
    <div className={`container ${showChatbot ? "show-chatbot" : ""}`}>
      {/* Botón flotante para abrir/cerrar */}
      <button
        id="chatbot-toggler"
        aria-label={showChatbot ? "Cerrar chat" : "Abrir chat"}
        onClick={() => setShowChatbot((v) => !v)}
      >
        <span className="material-symbols-outlined">
          {showChatbot ? "close" : "mode_comment"}
        </span>
      </button>

      <div className="chatbot-popup">
        {/* Header */}
        <div className="chat-header">
          <div className="header-info">
            <ChatbotIcon />
            <h2 className="logo-text">SaborBot</h2>
          </div>
          <button
            className="material-symbols-outlined"
            aria-label="Minimizar"
            onClick={() => setShowChatbot(false)}
          >
            keyboard_arrow_down
          </button>
        </div>

        {/* Body */}
        <div ref={chatBodyRef} className="chat-body">
          <div className="message bot-message">
            <ChatbotIcon />
            <p className="message-text">
              Hola cocinero 🥄 <br /> ¿Qué quieres cocinar el día de hoy?
            </p>
          </div>

          {/* Historial */}
          {chatHistory.map((chat, index) => (
            <ChatMessage key={index} chat={chat} />
          ))}
        </div>

        {/* Footer */}
        <div className="chat-footer">
          <ChatForm
            setChatHistory={setChatHistory}
            generateBotResponse={generateBotResponse}
          />
        </div>
      </div>
    </div>
  );
}
