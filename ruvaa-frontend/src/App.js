import React, { useState, useEffect } from "react";
import Login from "./components/Login";
import Navbar from "./components/Navbar";
import Onboarding from "./components/Onboarding";
import Profile from "./components/Profile";
import Assessment from "./components/Assessment";
import Chat from "./components/Chat";
import Recommendations from "./components/Recommendations";
import CollegeFinder from "./components/CollegeFinder";
import MentorBooking from "./components/MentorBooking";
import CareerAnalysis from "./components/CareerAnalysis";
import LearningPath from "./components/LearningPath";
import "./global.css";

function App() {
  const [page, setPage] = useState("login");
  const [darkMode, setDarkMode] = useState(() => JSON.parse(localStorage.getItem("cc_dark")) ?? false);
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem("cc_user")) || null);
  const [profileData, setProfileData] = useState(() => JSON.parse(localStorage.getItem("cc_profile")) || null);
  const [selectedCareer, setSelectedCareer] = useState(null);

  useEffect(() => {
    document.body.className = darkMode ? "dark" : "light";
    localStorage.setItem("cc_dark", JSON.stringify(darkMode));
  }, [darkMode]);

  const handleLogin = (u) => {
    setUser(u);
    localStorage.setItem("cc_user", JSON.stringify(u));
    setPage("onboarding");
  };

  const handleLogout = () => {
    setUser(null);
    setProfileData(null);
    localStorage.removeItem("cc_user");
    localStorage.removeItem("cc_profile");
    setPage("login");
  };

  const saveProfile = (data) => {
    setProfileData(data);
    localStorage.setItem("cc_profile", JSON.stringify(data));
    setPage("profile");
  };

  return (
    <div>
      {page !== "login" && <Navbar setPage={setPage} onLogout={handleLogout} profile={user} />}

      <div className="theme-switch" onClick={() => setDarkMode(s => !s)} title="Toggle theme">
        <div className={`knob ${darkMode ? "on" : "off"}`}>{darkMode ? "🌙" : "🌞"}</div>
      </div>

      <div className="app-container">
        {page === "login" && <Login onLogin={handleLogin} />}
        {page === "onboarding" && <Onboarding initial={profileData} onComplete={saveProfile} />}
        {page === "profile" && <Profile user={user} profile={profileData} setProfile={saveProfile} darkMode={darkMode} />}
        {page === "assessment" && <Assessment />}
        {page === "chat" && <Chat profile={profileData} darkMode={darkMode} />}
        {page === "recommendations" && (
          <Recommendations profile={profileData} setProfile={saveProfile} setPage={setPage} setSelectedCareer={setSelectedCareer} darkMode={darkMode} />
        )}
        {page === "colleges" && <CollegeFinder darkMode={darkMode} />}
        {page === "mentor" && <MentorBooking profile={profileData} />}
        {page === "career" && <CareerAnalysis profile={profileData} setProfile={saveProfile} setPage={setPage} setSelectedCareer={setSelectedCareer} darkMode={darkMode} />}
        {page === "learning" && <LearningPath profile={profileData} selectedCareer={selectedCareer} setSelectedCareer={setSelectedCareer} />}
      </div>

      <style>{`
        .app-container { padding-top: 70px; min-height: calc(100vh - 70px); }
        .theme-switch {
          position: fixed; right: 18px; top: 88px; z-index: 999;
          width: 52px; height: 32px; background: #00b4d8; border-radius: 40px;
          display:flex; align-items:center; padding:3px; cursor:pointer;
          box-shadow: 0 6px 20px rgba(0,0,0,0.18);
        }
        .theme-switch .knob {
          width: 26px; height:26px; border-radius:50%;
          background: #fff; display:flex; align-items:center; justify-content:center;
          font-size:14px; transition: transform .25s ease;
        }
        .theme-switch .knob.on { transform: translateX(20px); }
        body.dark { 
          --bg: #0f1720; 
          --card: #0b1220; 
          --text: #e6eef6; 
          --muted:#9aa7b5; 
        }
        body.light { 
          --bg: linear-gradient(135deg,#e0f7fa,#ffffff); 
          --card: #ffffff; 
          --text: #062b3c; 
          --muted:#6b7785; 
        }
        body { 
          background: var(--bg); 
          color: var(--text); 
          transition: background .3s, color .3s; 
          font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; 
        }
      `}</style>
    </div>
  );
}

export default App;
