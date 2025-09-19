import React, { useState, useEffect } from "react";
import Login from "./components/Login";
import Profile from "./components/Profile";
import Assessment from "./components/Assessment";
import Chat from "./components/Chat";
import Recommendations from "./components/Recommendations";
import CollegeFinder from "./components/CollegeFinder";
import MentorBooking from "./components/MentorBooking";
import Navbar from "./components/Navbar";
import "./App.css";

function App() {
  const [page, setPage] = useState("login"); // default page is login
  const [darkMode, setDarkMode] = useState(false);
  const [user, setUser] = useState(null); // user object

  useEffect(() => {
    document.body.className = darkMode ? "dark" : "light";
  }, [darkMode]);

  const toggleTheme = () => setDarkMode(!darkMode);

  const handleLogin = (userData) => {
    setUser(userData);
    setPage("profile"); // go to profile after login
  };

  return (
    <div>
      {page !== "login" && <Navbar setPage={setPage} />}

      {/* Sliding Theme Toggle
      <div className="theme-switch" onClick={toggleTheme}>
        <div className={`switch-knob ${darkMode ? "dark" : "light"}`}>
          <span className="icon">{darkMode ? "🌙" : "🌞"}</span>
        </div>
      </div> */}

      <div className="container">
        {page === "login" && <Login onLogin={handleLogin} />}
        {page === "profile" && <Profile user={user} />}
        {page === "assessment" && <Assessment />}
        {page === "chat" && <Chat />}
        {page === "recommendations" && <Recommendations />}
        {page === "colleges" && <CollegeFinder />}
        {page === "mentor" && <MentorBooking />}
      </div>
    </div>
  );
}

export default App;
