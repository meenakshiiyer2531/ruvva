import React, { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import ApiService from "../services/api";

export default function Chat({ profile, darkMode }) {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hi! I'm your career assistant. Ask me anything about your career journey!" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const send = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input;
    const userMsg = { from: "user", text: userMessage };
    setMessages((m) => [...m, userMsg, { from: "bot", text: "🤔 Thinking..." }]);
    setInput("");
    setLoading(true);

    try {
      const response = await ApiService.sendChatMessage(userMessage, profile);
      setMessages((m) => {
        const newArr = [...m];
        newArr[newArr.length - 1] = {
          from: "bot",
          text: response.response || "I'm here to help with your career questions!",
        };
        return newArr;
      });
    } catch (error) {
      setMessages((m) => {
        const newArr = [...m];
        newArr[newArr.length - 1] = {
          from: "bot",
          text: "Sorry, I'm having trouble connecting right now. Let me give you a helpful response anyway! 💡",
        };
        return newArr;
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const bgColor = darkMode ? "#121212" : "#f5f5f5";
  const cardBg = darkMode ? "#1e1e1e" : "#f0f0f0";
  const userMsgBg = darkMode ? "#2196f3" : "#00b4d8";
  const botMsgBg = darkMode ? "#2a2a2a" : "rgba(0,180,216,0.18)";
  const userTextColor = "#fff";
  const botTextColor = darkMode ? "#e0e0e0" : "#062b3c";
  const inputBg = darkMode ? "#2a2a2a" : "#fff";
  const inputTextColor = darkMode ? "#e0e0e0" : "#000";
  const inputBorder = darkMode ? "1px solid #444" : "1px solid #d6dbe1";

  return (
    <div
      style={{
        height: "85vh",
        width: "100%",
        maxWidth: "1500px",
        margin: "20px auto",
        padding: "0 20px",
        display: "flex",
        flexDirection: "column",
        background: bgColor,
        color: darkMode ? "#fff" : "#000",
        borderRadius: 12,
        boxShadow: darkMode
          ? "0 4px 12px rgba(0,0,0,0.8)"
          : "0 4px 12px rgba(0,0,0,0.1)",
        transition: "all 0.3s ease",
        overflow: "hidden",
      }}
    >
      {/* Messages Area */}
      <div
        style={{
          flex: 1,
          padding: 16,
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-end",
          gap: 12,
          overflowY: "auto",
        }}
      >
        {messages.map((m, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: m.from === "user" ? 50 : -50 }}
            animate={{ opacity: 1, x: 0 }}
            style={{
              alignSelf: m.from === "user" ? "flex-end" : "flex-start",
              maxWidth: "80%",
              background: m.from === "user" ? userMsgBg : botMsgBg,
              color: m.from === "user" ? userTextColor : botTextColor,
              padding: "10px 14px",
              borderRadius: 12,
              transition: "all 0.3s ease",
              wordBreak: "break-word",
            }}
          >
            {m.text}
          </motion.div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Section */}
      <div
        style={{
          display: "flex",
          gap: 8,
          padding: 12,
          background: cardBg,
          borderTopLeftRadius: 12,
          borderTopRightRadius: 12,
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          style={{
            flex: 1, // input takes most of the width
            padding: 14,
            borderRadius: 12,
            border: inputBorder,
            background: inputBg,
            color: inputTextColor,
            fontSize: 16,
            transition: "all 0.3s ease",
          }}
          onKeyDown={(e) => e.key === "Enter" && send()}
        />
        <button
          onClick={send}
          disabled={loading}
          style={{
            flex: "0 0 auto", // button takes minimal space
            padding: "12px 18px",
            borderRadius: 12,
            border: "none",
            background: loading ? "#ccc" : userMsgBg,
            color: "#fff",
            fontWeight: "bold",
            cursor: loading ? "not-allowed" : "pointer",
            transition: "all 0.3s ease",
          }}
        >
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}
