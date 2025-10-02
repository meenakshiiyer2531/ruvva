import React, { useState } from "react";
import ApiService from "../services/api";

export default function Register({ onRegister, setPage }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();

    console.log("📝 Registration form submitted");

    if (!name || !email || !password || !confirmPassword) {
      alert("Please fill in all fields");
      return;
    }

    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    if (password.length < 6) {
      alert("Password must be at least 6 characters long");
      return;
    }

    setLoading(true);
    try {
      console.log("📤 Sending registration request to backend:", { name, email });
      const response = await ApiService.register({ name, email, password });
      console.log("✅ Registration successful:", response);

      // Auto-login after successful registration
      if (response.user) {
        onRegister(response.user);
      } else if (response.id) {
        // Handle different response formats
        onRegister({ id: response.id, name: response.name, email: response.email });
      }
    } catch (error) {
      console.error("❌ Registration failed:", error);
      alert("Registration failed: " + (error.message || "Unknown error"));
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
          <h2 style={overlayTitle}>Join CareerConnect</h2>
          <p style={overlayText}>Start your personalized career journey today.</p>
        </div>
      </div>

      {/* Right Form */}
      <div style={formWrapper}>
        <h1 style={formTitle}>Create Account</h1>
        <p style={formSubtitle}>Sign up to discover your career path</p>

        <form onSubmit={submit} style={formStyle}>
          <input
            aria-label="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Full Name"
            style={inputStyle}
          />
          <input
            aria-label="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email Address"
            style={inputStyle}
          />
          <input
            aria-label="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password (min 6 characters)"
            type="password"
            style={inputStyle}
          />
          <input
            aria-label="confirm-password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm Password"
            type="password"
            style={inputStyle}
          />
          <button type="submit" style={btnStyle} disabled={loading}>
            {loading ? "Creating Account..." : "Sign Up"}
          </button>
        </form>

        <div style={linkContainer}>
          Already have an account?{" "}
          <span style={linkStyle} onClick={() => setPage("login")}>
            Sign in
          </span>
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
const formSubtitle = { color: "#6c757d", marginBottom: 8 };
const formStyle = { display: "grid", gap: 12, marginTop: 12 };
const inputStyle = { padding: "12px 14px", borderRadius: 10, border: "1px solid #d6dbe1", background: "transparent", color: "#212529", fontSize: 15 };
const btnStyle = { padding: "12px 14px", borderRadius: 12, border: "none", background: "#00b4d8", color: "white", fontWeight: 700, cursor: "pointer", fontSize: 15 };
const linkContainer = { marginTop: 16, textAlign: "center", color: "#6c757d", fontSize: 14 };
const linkStyle = { color: "#0077b6", fontWeight: 600, cursor: "pointer", textDecoration: "underline" };
