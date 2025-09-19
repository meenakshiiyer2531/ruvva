import React, { useState, useEffect } from "react";

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    document.body.className = darkMode ? "dark" : "light";
  }, [darkMode]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username && password) {
      onLogin({ name: username });
    } else {
      alert("Please enter credentials");
    }
  };

  return (
    <>
      <div className="login-wrapper">
        <div className="login-image">
          <img src="/login.jpg" alt="Login Illustration" />
        </div>

        <div className="login-card">
          <h2>Welcome Back!</h2>
          <p className="subtext">Login to access your Ruvaa profile</p>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="input-group">
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
              <label>Username</label>
            </div>

            <div className="input-group">
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <label>Password</label>
            </div>

            <button type="submit">Login</button>
          </form>

          <p className="forgot">Forgot Password?</p>

        </div>
      </div>

      <style>{`
        body.light { background:#f0f2f5; transition:0.5s; }
        body.dark { background:#121212; transition:0.5s; }

        .login-wrapper {
          display: flex;
          max-width: 1200px;
          width: 95%;
          height: 650px;
          margin: 60px auto;
          border-radius: 25px;
          overflow: hidden;
          box-shadow: 0 20px 60px rgba(0,0,0,0.3);
          background: var(--card-bg);
          transition: 0.5s;
        }
        body.light .login-wrapper { --card-bg: rgba(255,255,255,0.95); }
        body.dark .login-wrapper { --card-bg: rgba(30,30,30,0.95); }

        .login-image {
          flex: 1.2;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .login-image img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .login-card {
          flex: 1;
          padding: 60px;
          display: flex;
          flex-direction: column;
          justify-content: center;
          background: var(--card-bg);
          transition:0.5s;
        }

        .login-card h2 {
          text-align:center;
          font-size: 2.2rem;
          margin-bottom: 8px;
          color: var(--text-color);
        }
        .login-card .subtext {
          text-align:center;
          font-size:1rem;
          margin-bottom:35px;
          color: #777;
        }

        .input-group { position: relative; margin-bottom: 28px; }
        .input-group input {
          width:100%;
          padding:16px 12px;
          border:2px solid #ddd;
          border-radius:16px;
          background: var(--input-bg);
          color: var(--input-color);
          font-size:1rem;
          transition:0.3s;
        }
        .input-group label {
          position:absolute;
          top:50%;
          left:14px;
          transform:translateY(-50%);
          color:#aaa;
          pointer-events:none;
          transition:0.3s;
          font-size:1rem;
        }
        .input-group input:focus + label,
        .input-group input:not(:placeholder-shown) + label {
          top:-10px;
          left:12px;
          font-size:0.8rem;
          color:#00b4d8;
          background: var(--card-bg);
          padding:0 5px;
        }

        body.light .input-group input { --input-bg:#fff; --input-color:#222; --text-color:#222; }
        body.dark .input-group input { --input-bg:#2b2b2b; --input-color:#f1f1f1; --text-color:#f1f1f1; }

        button {
          width:100%;
          padding:16px;
          background:#00b4d8;
          border:none;
          border-radius:16px;
          color:white;
          font-weight:bold;
          font-size:1.1rem;
          cursor:pointer;
          transition:0.4s;
          margin-top:10px;
        }
        button:hover {
          background:#0077b6;
          transform: translateY(-2px) scale(1.02);
          box-shadow: 0 12px 30px rgba(0,0,0,0.3);
        }

        .forgot {
          text-align:center;
          margin-top:18px;
          font-size:0.9rem;
          color:#777;
          cursor:pointer;
        }
        .forgot:hover { color:#00b4d8; }

        .theme-toggle {
          display:flex;
          align-items:center;
          justify-content:center;
          margin-top:25px;
          gap:12px;
          font-size:1.1rem;
        }
        .switch {
          position: relative;
          display: inline-block;
          width: 55px;
          height: 28px;
        }
        .switch input { opacity:0; width:0; height:0; }
        .slider {
          position: absolute;
          cursor: pointer;
          top: 0; left: 0; right: 0; bottom: 0;
          background-color: #ccc;
          transition: .4s;
          border-radius: 28px;
        }
        .slider:before {
          position: absolute;
          content: "";
          height: 22px;
          width: 22px;
          left: 3px;
          bottom: 3px;
          background-color: white;
          transition: .4s;
          border-radius: 50%;
        }
        input:checked + .slider { background-color: #00b4d8; }
        input:checked + .slider:before { transform: translateX(27px); }

        /* Responsive */
        @media(max-width:1024px){
          .login-wrapper { flex-direction: column; height:auto; }
          .login-image { width:100%; height:350px; }
          .login-card { padding:50px; }
        }
        @media(max-width:768px){
          .login-card { padding:40px; }
          button { padding:14px; font-size:1rem; }
        }
        @media(max-width:480px){
          .login-card { padding:30px; }
          button { padding:12px; font-size:0.95rem; }
        }
      `}</style>
    </>
  );
}

export default Login;
