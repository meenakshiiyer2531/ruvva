import React, { useState, useEffect } from "react";

export default function Profile({ user, profile, setProfile, darkMode }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(profile);

  useEffect(() => {
    setDraft(profile);
  }, [profile]);

  const save = () => {
    setProfile(draft);
    localStorage.setItem("cc_profile", JSON.stringify(draft));
    setEditing(false);
  };

  const deleteCareer = (id) => {
    const updated = {
      ...draft,
      savedCareers: draft.savedCareers?.filter(c => c.id !== id) || []
    };
    setDraft(updated);
    setProfile(updated);
    localStorage.setItem("cc_profile", JSON.stringify(updated));
  };

  return (
    <div style={{ minHeight: "80vh", padding: 20, maxWidth: 700, margin: "0 auto" }}>
      <h2 style={{ color: "#0077b6" }}>Your Profile</h2>

      {editing ? (
        <div style={{ display: "grid", gap: 12 }}>
          <input
            value={draft.name || ""}
            onChange={e => setDraft(s => ({ ...s, name: e.target.value }))}
            style={{ ...field, background: darkMode ? "#0b1220" : "#fff" }}
          />
          <input
            value={draft.studentClass || ""}
            onChange={e => setDraft(s => ({ ...s, studentClass: e.target.value }))}
            style={{ ...field, background: darkMode ? "#0b1220" : "#fff" }}
          />
          <input
            value={draft.location || ""}
            onChange={e => setDraft(s => ({ ...s, location: e.target.value }))}
            style={{ ...field, background: darkMode ? "#0b1220" : "#fff" }}
          />
          <textarea
            value={draft.aspirations || ""}
            onChange={e => setDraft(s => ({ ...s, aspirations: e.target.value }))}
            style={{ ...field, minHeight: 100, background: darkMode ? "#0b1220" : "#fff" }}
          />
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={save} style={btn}>Save</button>
            <button onClick={() => setEditing(false)} style={btnMuted}>Cancel</button>
          </div>
        </div>
      ) : (
        <div style={{ display: "grid", gap: 6 }}>
          <div><strong>Name:</strong> {profile?.name}</div>
          <div><strong>Class:</strong> {profile?.studentClass}</div>
          <div><strong>Location:</strong> {profile?.location}</div>
          <div><strong>Aspirations:</strong> {profile?.aspirations}</div>
          <button onClick={() => setEditing(true)} style={btn}>Edit Profile</button>
        </div>
      )}

      {/* Saved Careers */}
      {profile?.savedCareers?.length > 0 && (
        <div style={{ marginTop: 30 }}>
          <h3 style={{ color: "#0077b6" }}>Saved Careers</h3>
          <div style={{ display: "grid", gap: 12 }}>
            {profile.savedCareers.map(c => (
              <div
                key={c.id}
                style={{
                  padding: 12,
                  borderRadius: 10,
                  background: darkMode ? "#0b1220" : "#fff",
                  boxShadow: darkMode
                    ? "0 2px 6px rgba(255,255,255,0.05)"
                    : "0 4px 10px rgba(0,0,0,0.08)",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center"
                }}
              >
                <div>
                  <strong>{c.title}</strong>
                  <p style={{ margin: 4, fontSize: 13, color: darkMode ? "#e6eef6" : "#555" }}>
                    {c.desc}
                  </p>
                </div>
                <button onClick={() => deleteCareer(c.id)} style={deleteBtn}>Delete</button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Styles
const field = {
  padding: 12,
  borderRadius: 10,
  border: "1px solid #d6dbe1",
  color: "var(--text)",
  fontSize: 14
};

const btn = {
  padding: "10px 16px",
  borderRadius: 10,
  border: "none",
  background: "#00b4d8",
  color: "#fff",
  cursor: "pointer"
};

const btnMuted = { ...btn, background: "#888" };
const deleteBtn = {
  padding: "6px 10px",
  borderRadius: 8,
  border: "none",
  background: "#ef4444",
  color: "#fff",
  cursor: "pointer"
};
