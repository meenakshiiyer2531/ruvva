import React from "react";

function Navbar({ setPage }) {
  return (
    <div className="navbar">
      <span onClick={() => setPage("profile")}>Profile</span>
      <span onClick={() => setPage("assessment")}>Assessment</span>
      <span onClick={() => setPage("chat")}>Chat</span>
      <span onClick={() => setPage("recommendations")}>Recommendations</span>
      <span onClick={() => setPage("colleges")}>Colleges</span>
      <span onClick={() => setPage("mentor")}>Mentor</span>
    </div>
  );
}

export default Navbar;
