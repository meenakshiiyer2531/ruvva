import React, { useState, useRef, useEffect } from "react";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [darkMode, setDarkMode] = useState(false);
  const chatEndRef = useRef(null);

  const handleSend = () => {
    if (!input.trim()) return;
    const newMsg = { from: "user", text: input };
    const botReply = { from: "bot", text: "💡 This is a dummy AI reply (backend needed)." };
    setMessages([...messages, newMsg, botReply]);
    setInput("");
  };

  // Auto scroll to bottom (optional, can be kept or removed since scrolling is removed)
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className={`chat-page ${darkMode ? "dark" : "light"}`}>
      <div className="chat-header">
        <h1>🤖 AI Chat</h1>
        <button className="theme-toggle" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? "🌞 Light" : "🌙 Dark"}
        </button>
      </div>

      <div className="chat-box">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`chat-message ${m.from === "user" ? "user" : "bot"}`}
          >
            {m.text}
          </div>
        ))}
        <div ref={chatEndRef}></div>
      </div>

      <div className="chat-input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>

      {/* Embedded CSS */}
      <style>{`
        .chat-page {
          display: flex;
          flex-direction: column;
          min-height: 100vh;
          width: 100%;
          font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
          transition: 0.3s;
        }

        .chat-page.light {
          background: #f7f7f8;
          color: #222;
        }

        .chat-page.dark {
          background: #1e1e1e;
          color: #f1f1f1;
        }

        .chat-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 20px 30px;
          background: #0077b6;
          color: white;
          font-size: 1.5rem;
        }

        .chat-box {
          flex: 1;
          padding: 20px 50px; /* added horizontal padding */
          display: flex;
          flex-direction: column;
          gap: 12px;
          /* Removed overflow-y to make it non-scrollable */
        }

        .chat-message {
          max-width: 70%;
          padding: 14px 18px;
          border-radius: 18px;
          font-size: 1rem;
          line-height: 1.4;
          word-wrap: break-word;
        }

        .chat-message.user {
          background: #00b4d8;
          color: white;
          align-self: flex-end;
          border-bottom-right-radius: 4px;
        }

        .chat-message.bot {
          background: #e0e0e0;
          color: #222;
          align-self: flex-start;
          border-bottom-left-radius: 4px;
        }

        .chat-page.dark .chat-message.bot {
          background: #2b2b2b;
          color: #f1f1f1;
        }

        .chat-input-container {
          display: flex;
          padding: 15px 30px;
          gap: 12px;
          border-top: 1px solid #ccc;
          background: inherit;
        }

        .chat-input-container input {
          flex: 1;
          padding: 14px 18px;
          border-radius: 25px;
          border: 1px solid #ccc;
          font-size: 1rem;
          outline: none;
          transition: 0.3s;
        }

        .chat-input-container input:focus {
          border-color: #00b4d8;
          box-shadow: 0 0 10px rgba(0,180,216,0.3);
        }

        .chat-input-container button {
          padding: 14px 20px;
          background: #00b4d8;
          color: white;
          border: none;
          border-radius: 25px;
          font-weight: bold;
          cursor: pointer;
          transition: 0.3s;
        }

        .chat-input-container button:hover {
          background: #0077b6;
          transform: translateY(-2px) scale(1.02);
          box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }

        .theme-toggle {
          background: rgba(255,255,255,0.2);
          border: none;
          padding: 8px 14px;
          border-radius: 12px;
          cursor: pointer;
          font-size: 1rem;
          transition: 0.3s;
        }

        .theme-toggle:hover {
          background: rgba(255,255,255,0.4);
        }

        @media(max-width:768px){
          .chat-message { max-width: 85%; font-size: 0.95rem; }
          .chat-header { font-size: 1.2rem; padding: 15px; }
          .chat-input-container { padding: 10px 15px; gap: 8px; }
          .chat-box { padding: 15px 20px; }
        }
      `}</style>
    </div>
  );
}

export default Chat;
