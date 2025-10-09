import ChatbotIcon from "../components/ChatbotIcon";
import ChatForm from "../components/ChatForm";

export default function Page() {
  return (
    <div className="container">
      <div className="chatbot-popup">
        {/*  Chatbot header */}
        <div className="chat-header">
          <div className="header-info">
            <ChatbotIcon />
            <h2 className="logo-text">SaborBot</h2>
          </div>
          <button className="material-symbols-outlined">keyboard_arrow_down</button>
        </div>

        {/*  Chatbot body */}
        <div className="chat-body">
          <div className="message bot-message">
            <ChatbotIcon />
            <p className="message-text">
              Hola cocinero 🥄 <br /> ¿Qué quieres cocinar el día de hoy?
            </p>
          </div>
          <div className="message user-message">
            <p className="message-text">
              Lorem, ipsum dolor sit amet consectetur adipisicing.
            </p>
          </div>
        </div>
        {/*  Chatbot footer */}
        <div className="chat-footer">
          <ChatForm />
        </div>
      </div>
    </div>
  );
}