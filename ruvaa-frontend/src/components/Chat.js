import React, { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";
import ApiService from "../services/api";

export default function Chat({ profile, darkMode }) {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hi! I'm your career assistant. Ask me anything about your career journey!" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showScrollButton, setShowScrollButton] = useState(false);
  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null);

  const send = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input;
    const userMsg = { from: "user", text: userMessage };
    setMessages((m) => [...m, userMsg, { from: "bot", text: "🤔 Thinking..." }]);
    setInput("");
    setLoading(true);

    console.log("💬 Sending chat message:", userMessage);

    try {
      const response = await ApiService.sendChatMessage(userMessage, profile);
      console.log("✅ Chat response received:", response);

      // Extract AI response from backend wrapper
      let aiResponse = response.data?.response || response.response || response.message || "I'm here to help with your career questions!";

      // Clean up response: remove literal \n and ensure proper line breaks for markdown
      aiResponse = aiResponse
        .replace(/\\n/g, '\n')  // Convert literal \n to actual newlines
        .replace(/\n{3,}/g, '\n\n')  // Replace 3+ newlines with 2 (paragraph break)
        .trim();

      console.log("🤖 AI Response:", aiResponse);

      setMessages((m) => {
        const newArr = [...m];
        newArr[newArr.length - 1] = {
          from: "bot",
          text: aiResponse,
        };
        return newArr;
      });
    } catch (error) {
      console.error("❌ Chat error:", error.message);
      console.error("🔌 Backend Status: Python AI appears to be disconnected");

      setMessages((m) => {
        const newArr = [...m];
        newArr[newArr.length - 1] = {
          from: "bot",
          text: "⚠️ Sorry, I can't connect to the AI backend right now. Please check that the Python AI service is running on port 5000. Error: " + error.message,
        };
        return newArr;
      });
    } finally {
      setLoading(false);
    }
  };

  // Smart auto-scroll: only scroll to bottom if user is already near bottom
  useEffect(() => {
    const container = messagesContainerRef.current;
    if (!container) return;

    const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 150;

    // Only auto-scroll if user is near bottom (not reading previous messages)
    if (isNearBottom) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  // Handle scroll to show/hide scroll-to-bottom button
  const handleScroll = () => {
    const container = messagesContainerRef.current;
    if (!container) return;

    const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 150;
    setShowScrollButton(!isNearBottom);
  };

  // Scroll to bottom manually
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

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
        ref={messagesContainerRef}
        onScroll={handleScroll}
        style={{
          flex: 1,
          padding: 16,
          display: "flex",
          flexDirection: "column",
          gap: 12,
          overflowY: "auto",
          overflowX: "hidden",
          position: "relative",
        }}
      >
        {/* Flexible spacer to push messages to bottom when list is short */}
        <div style={{ flex: messages.length < 3 ? 1 : 0, minHeight: 0 }} />

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
            className={m.from === "bot" ? "markdown-message" : ""}
          >
            {m.from === "bot" ? (
              <ReactMarkdown
                components={{
                  p: ({ children }) => <p style={{ margin: "0.5em 0", lineHeight: "1.6" }}>{children}</p>,
                  strong: ({ children }) => <strong style={{ fontWeight: 700, color: darkMode ? "#4fc3f7" : "#0277bd" }}>{children}</strong>,
                  em: ({ children }) => <em style={{ fontStyle: "italic" }}>{children}</em>,
                  ul: ({ children }) => <ul style={{ marginLeft: "1.2em", marginTop: "0.5em", marginBottom: "0.5em" }}>{children}</ul>,
                  ol: ({ children }) => <ol style={{ marginLeft: "1.2em", marginTop: "0.5em", marginBottom: "0.5em" }}>{children}</ol>,
                  li: ({ children }) => <li style={{ marginBottom: "0.3em", lineHeight: "1.5" }}>{children}</li>,
                  code: ({ inline, children }) => (
                    <code style={{
                      background: darkMode ? "#1a1a1a" : "#f5f5f5",
                      padding: inline ? "2px 6px" : "8px 12px",
                      borderRadius: 4,
                      fontSize: "0.9em",
                      fontFamily: "monospace",
                      display: inline ? "inline" : "block",
                      margin: inline ? "0" : "0.5em 0"
                    }}>{children}</code>
                  ),
                  h1: ({ children }) => <h1 style={{ fontSize: "1.4em", fontWeight: 700, margin: "0.5em 0", color: darkMode ? "#4fc3f7" : "#0277bd" }}>{children}</h1>,
                  h2: ({ children }) => <h2 style={{ fontSize: "1.3em", fontWeight: 700, margin: "0.5em 0", color: darkMode ? "#4fc3f7" : "#0277bd" }}>{children}</h2>,
                  h3: ({ children }) => <h3 style={{ fontSize: "1.2em", fontWeight: 700, margin: "0.5em 0", color: darkMode ? "#4fc3f7" : "#0277bd" }}>{children}</h3>,
                  a: ({ href, children }) => <a href={href} target="_blank" rel="noopener noreferrer" style={{ color: "#00b4d8", textDecoration: "underline" }}>{children}</a>,
                }}
              >
                {m.text}
              </ReactMarkdown>
            ) : (
              m.text
            )}
          </motion.div>
        ))}
        <div ref={messagesEndRef} />

        {/* Scroll to bottom button */}
        {showScrollButton && (
          <motion.button
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            onClick={scrollToBottom}
            style={{
              position: "absolute",
              bottom: 20,
              right: 20,
              width: 48,
              height: 48,
              borderRadius: "50%",
              border: "none",
              background: userMsgBg,
              color: "#fff",
              fontSize: 20,
              cursor: "pointer",
              boxShadow: darkMode
                ? "0 4px 12px rgba(0,0,0,0.6)"
                : "0 4px 12px rgba(0,0,0,0.3)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              transition: "all 0.3s ease",
              zIndex: 10,
            }}
            onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.1)")}
            onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
            title="Scroll to bottom"
          >
            ↓
          </motion.button>
        )}
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

      {/* Custom scrollbar styles */}
      <style>{`
        .markdown-message p:first-child {
          margin-top: 0;
        }
        .markdown-message p:last-child {
          margin-bottom: 0;
        }

        /* Custom scrollbar for messages container */
        div[style*="overflowY: auto"]::-webkit-scrollbar {
          width: 8px;
        }
        div[style*="overflowY: auto"]::-webkit-scrollbar-track {
          background: ${darkMode ? "#1a1a1a" : "#f1f1f1"};
          border-radius: 10px;
        }
        div[style*="overflowY: auto"]::-webkit-scrollbar-thumb {
          background: ${darkMode ? "#444" : "#888"};
          border-radius: 10px;
        }
        div[style*="overflowY: auto"]::-webkit-scrollbar-thumb:hover {
          background: ${darkMode ? "#555" : "#666"};
        }
      `}</style>
    </div>
  );
}
