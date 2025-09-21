import React from "react";

export default function Navbar({ setPage, onLogout, profile }) {
  const displayName = profile?.name || "Guest";

  return (
    <div className="cc-nav">
      <div className="brand" onClick={() => setPage("profile")}>CareerConnect</div>
      <div className="links">
        <button onClick={() => setPage("profile")}>Profile</button>
        <button onClick={() => setPage("career")}>Analysis</button>
        <button onClick={() => setPage("recommendations")}>Careers</button>
        <button onClick={() => setPage("learning")}>Learning Path</button>
        <button onClick={() => setPage("assessment")}>Assessment</button>
        <button onClick={() => setPage("chat")}>Chat</button>
        <button onClick={() => setPage("colleges")}>College Finder</button>
        <button onClick={() => setPage("mentor")}>Mentor Booking</button>
        <button onClick={onLogout} style={{ background: "#ef4444" }}>Logout</button>
        <div className="profile-bubble" title={displayName}>
          {displayName[0]}
        </div>
      </div>

      <style>{`
        .cc-nav {
          position: fixed; top:0; left:0; right:0; height:66px; display:flex; align-items:center; justify-content:space-between;
          padding: 0 18px; background: linear-gradient(90deg, rgba(0,119,182,1) 0%, rgba(0,180,216,1) 100%);
          color:white; z-index:900; box-shadow:0 6px 20px rgba(0,0,0,0.12);
        }
        .brand { font-weight:800; cursor:pointer; }
        .links { display:flex; gap:8px; flex-wrap:wrap; align-items:center; }
        .links button {
          background: rgba(255,255,255,0.08); color:white; border:none; padding:8px 12px; border-radius:10px; cursor:pointer; font-weight:600;
        }
        .links button:hover { transform: translateY(-2px); box-shadow:0 8px 20px rgba(0,0,0,0.18); }
        .profile-bubble {
          margin-left:12px; width:32px; height:32px; border-radius:50%; background:#fff; color:#0077b6;
          display:flex; align-items:center; justify-content:center; font-weight:bold; cursor:pointer;
        }
        @media(max-width:900px){
          .links { display: grid; grid-auto-flow: column; gap:6px; overflow:auto; padding-bottom:6px; }
        }
      `}</style>
    </div>
  );
}
