import React, { useState } from "react";
import ApiService from "../services/api";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    if (!username || !password) return alert("Enter credentials");

    setLoading(true);
    try {
      const response = await ApiService.login({ username, password });
      onLogin(response.user);
    } catch (error) {
      alert("Login failed: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={container}>
      {/* Left Image */}
      <div style={imageWrapper}>
        <img src="/login.jpg" alt="CareerConnect" style={imageStyle} />
        <div style={imageOverlay}>
          <h2 style={overlayTitle}>Welcome to CareerConnect</h2>
          <p style={overlayText}>Your journey to a brighter future starts here.</p>
        </div>
      </div>

      {/* Right Form */}
      <div style={formWrapper}>
        <h1 style={formTitle}>Login</h1>
        <p style={formSubtitle}>Sign in to begin your career journey</p>

        <form onSubmit={submit} style={formStyle}>
          <input
            aria-label="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Your name"
            style={inputStyle}
          />
          <input
            aria-label="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            type="password"
            style={inputStyle}
          />
          <button type="submit" style={btnStyle} disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <div style={tipText}>
          MVP: Tries real API, falls back to mock if backend unavailable.
        </div>
      </div>

      <style>{`
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body { overflow-x: hidden; font-family: sans-serif; }
        input:focus { outline: 2px solid rgba(0,180,216,0.18); }
        @media(max-width:768px){
          div[style*="flexDirection: row"] {
            flex-direction: column;
            height: auto;
            max-width: 90%;
            margin: 20px auto;
          }
          div[style*="flex: 1"][style*="position: relative"] { display: none; }
          div[style*="padding: 36px"] { padding: 24px; }
        }
      `}</style>
    </div>
  );
}

// Styles
const container = { display: "flex", flexDirection: "row", width: "100%", maxWidth: 900, minHeight: "70vh", margin: "40px auto", borderRadius: 20, overflow: "hidden", boxShadow: "0 10px 40px rgba(2,6,23,0.2)", background: "white" };
const imageWrapper = { flex: 1, position: "relative", minWidth: 0 };
const imageStyle = { width: "100%", height: "100%", objectFit: "cover", display: "block" };
const imageOverlay = { position: "absolute", top: 0, left: 0, width: "100%", height: "100%", background: "linear-gradient(135deg, rgba(0,180,216,0.7), rgba(0,119,182,0.7))", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", color: "white", textAlign: "center", padding: 20 };
const overlayTitle = { margin: 0, fontSize: 28 };
const overlayText = { fontSize: 16, marginTop: 10 };
const formWrapper = { flex: 1, padding: 36, display: "flex", flexDirection: "column", justifyContent: "center", minWidth: 0, boxSizing: "border-box" };
const formTitle = { margin: 0, color: "#0077b6" };
const formSubtitle = { color: "#6c757d" };
const formStyle = { display: "grid", gap: 12, marginTop: 12 };
const inputStyle = { padding: "12px 14px", borderRadius: 10, border: "1px solid #d6dbe1", background: "transparent", color: "#212529", fontSize: 15 };
const btnStyle = { padding: "12px 14px", borderRadius: 12, border: "none", background: "#00b4d8", color: "white", fontWeight: 700, cursor: "pointer", fontSize: 15 };
const tipText = { marginTop: 10, color: "#6c757d", fontSize: 13 };
