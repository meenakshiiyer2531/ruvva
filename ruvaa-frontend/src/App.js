import React, { useState, useEffect } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import Navbar from "./components/Navbar";
import Onboarding from "./components/Onboarding";
import Profile from "./components/Profile";
import EditProfile from "./components/EditProfile";
import Assessment from "./components/Assessment";
import Chat from "./components/Chat";
import Recommendations from "./components/Recommendations";
import CollegeFinder from "./components/CollegeFinder";
import MentorBooking from "./components/MentorBooking";
import MentorSessionDetail from "./components/MentorSessionDetail";
import CareerAnalysis from "./components/CareerAnalysis";
import LearningPath from "./components/LearningPath";
import LandingPage from "./components/LandingPage";
import LanguageSelector from "./components/LanguageSelector";
import "./i18n";
import "./global.css";

function App() {
  const [page, setPage] = useState("landing");
  const [darkMode, setDarkMode] = useState(() => JSON.parse(localStorage.getItem("cc_dark")) ?? false);
  const [bookingDetailId, setBookingDetailId] = useState(null);
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem("cc_user")) || null);
  const [profileData, setProfileData] = useState(() => JSON.parse(localStorage.getItem("cc_profile")) || null);
  const [selectedCareer, setSelectedCareer] = useState(null);
  const [toasts, setToasts] = useState([]);

  const showToast = (msg, type = 'info', ttl = 3000) => {
    const id = Date.now() + Math.random();
    setToasts(t => [...t, { id, msg, type }]);
    setTimeout(() => setToasts(t => t.filter(x => x.id !== id)), ttl);
  };

  useEffect(() => {
    document.body.className = darkMode ? "dark" : "light";
    localStorage.setItem("cc_dark", JSON.stringify(darkMode));
  }, [darkMode]);

  // Lightweight global customEvent navigation bridge
  useEffect(() => {
    const handler = (e) => {
      if (e.detail?.page) {
        setPage(e.detail.page);
        if (e.detail.page === 'bookingDetail') setBookingDetailId(e.detail.bookingId || null);
      }
    };
    window.addEventListener('navigate', handler);
    return () => window.removeEventListener('navigate', handler);
  }, []);

  const handleLogin = (u) => {
    console.log("✅ User logged in:", u);
    setUser(u);
    localStorage.setItem("cc_user", JSON.stringify(u));
    // Requirement: after login always go to profile page
    setPage("profile");
    showToast(`Welcome back ${u.name || ''}`, 'success');
  };

  const handleRegister = (u) => {
    console.log("✅ User registered:", u);
    setUser(u);
    localStorage.setItem("cc_user", JSON.stringify(u));
    // Requirement: after sign up go to onboarding page
    setPage("onboarding");
    showToast('Registration successful. Please complete onboarding.', 'success');
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
    showToast('Profile saved', 'success');
  };

  return (
    <div className="cc-app">
      {/* Navigation Bar */}
      {page !== "login" && page !== "register" && page !== "landing" && (
        <Navbar setPage={setPage} onLogout={handleLogout} profile={user} />
      )}

      {/* Professional Theme Toggle */}
      {page !== "landing" && (
        <button
          className={`cc-theme-toggle ${darkMode ? 'cc-theme-toggle--dark' : 'cc-theme-toggle--light'}`}
          onClick={() => setDarkMode(s => !s)}
          title="Toggle theme"
          aria-label="Toggle dark/light theme"
        >
          <div className="cc-theme-toggle__icon">
            {darkMode ? "🌙" : "🌞"}
          </div>
        </button>
      )}

      {/* Language Selector */}
      {page !== "landing" && (
        <div className="cc-language-selector-wrapper">
          <LanguageSelector />
        </div>
      )}

      {/* Main Application Container */}
      <main className={`cc-main ${page === "landing" ? 'cc-main--landing' : 'cc-main--app'}`}>
        {page === "landing" && <LandingPage onNavigate={setPage} />}
  {page === "login" && <Login onLogin={handleLogin} setPage={setPage} showToast={showToast} />}
  {page === "register" && <Register onRegister={handleRegister} setPage={setPage} showToast={showToast} />}
  {page === "onboarding" && <Onboarding initial={profileData} onComplete={saveProfile} showToast={showToast} setPage={setPage} />}
  {page === "profile" && <Profile user={user} profile={profileData} setProfile={saveProfile} darkMode={darkMode} showToast={showToast} />}
  {page === "editProfile" && <EditProfile user={user} profile={profileData} setProfile={saveProfile} darkMode={darkMode} showToast={showToast} setPage={setPage} />}
        {page === "assessment" && <Assessment />}
        {page === "chat" && <Chat profile={profileData} darkMode={darkMode} />}
        {page === "recommendations" && (
          <Recommendations profile={profileData} setProfile={saveProfile} setPage={setPage} setSelectedCareer={setSelectedCareer} darkMode={darkMode} />
        )}
        {page === "colleges" && <CollegeFinder darkMode={darkMode} />}
  {page === "mentor" && <MentorBooking profile={profileData} studentId={user?.id} />}
  {page === "bookingDetail" && <MentorSessionDetail bookingId={bookingDetailId} />}
        {page === "career" && <CareerAnalysis profile={profileData} setProfile={saveProfile} setPage={setPage} setSelectedCareer={setSelectedCareer} darkMode={darkMode} />}
        {page === "learning" && <LearningPath profile={profileData} selectedCareer={selectedCareer} setSelectedCareer={setSelectedCareer} />}
      </main>
      {/* Toast Container */}
      <div style={toastContainerStyle} aria-live="polite" aria-atomic="true">
        {toasts.map(t => (
          <div key={t.id} style={{ ...toastStyle, borderLeft: `4px solid ${t.type==='error'?'#dc2626':t.type==='success'?'#16a34a':'#0ea5e9'}` }}>
            <span style={{ fontWeight: 600 }}>{t.type.toUpperCase()}: </span>{t.msg}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;

const toastContainerStyle = {
  position: 'fixed',
  top: 16,
  right: 16,
  display: 'flex',
  flexDirection: 'column',
  gap: 8,
  zIndex: 9999
};
const toastStyle = {
  background: '#ffffff',
  color: '#0f172a',
  padding: '10px 14px',
  borderRadius: 8,
  boxShadow: '0 4px 12px rgba(0,0,0,0.12)',
  fontSize: 14,
  maxWidth: 320
};
