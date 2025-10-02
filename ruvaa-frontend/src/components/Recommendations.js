import React, { useState, useMemo, useEffect } from "react";
import { careers as fallbackCareers } from "./careersData";
import ApiService from "../services/api";

export default function Recommendations({ profile, setProfile, setPage, setSelectedCareer, darkMode }) {
  const [query, setQuery] = useState("");
  const [index, setIndex] = useState(0);
  const [careers, setCareers] = useState(fallbackCareers);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch careers from backend on mount
  useEffect(() => {
    const fetchCareers = async () => {
      console.log("🔍 Fetching career recommendations from backend...");
      setLoading(true);
      setError(null);

      try {
        const data = await ApiService.getCareerRecommendations(profile);
        console.log("✅ Backend careers loaded:", data);

        // Backend should return an array of career objects
        if (Array.isArray(data)) {
          setCareers(data);
        } else if (data.careers && Array.isArray(data.careers)) {
          setCareers(data.careers);
        } else {
          console.warn("⚠️ Unexpected backend response format, using fallback data");
          setCareers(fallbackCareers);
        }
      } catch (err) {
        console.error("❌ Failed to fetch careers from backend:", err.message);
        console.log("⚠️ Using local fallback career data");
        // Don't show error to user since fallback data works fine
        setCareers(fallbackCareers);
      } finally {
        setLoading(false);
      }
    };

    fetchCareers();
  }, [profile]);

  // Filter careers based on search query
  const filtered = useMemo(
    () =>
      careers.filter(
        (c) =>
          c.title.toLowerCase().includes(query.toLowerCase()) ||
          c.desc.toLowerCase().includes(query.toLowerCase())
      ),
    [query, careers]
  );

  // Handlers for left/right buttons
  const handlePrev = () => setIndex((i) => Math.max(i - 1, 0));
  const handleNext = () =>
    setIndex((i) => (filtered.length ? (i + 1) % filtered.length : 0));

  // Save career to profile
  const handleSave = (career) => {
    if (!profile.savedCareers?.some((c) => c.id === career.id)) {
      const updated = { ...profile, savedCareers: [...(profile.savedCareers || []), career] };
      setProfile(updated);
      localStorage.setItem("cc_profile", JSON.stringify(updated));
      alert(`${career.title} saved to your profile!`);
    } else alert(`${career.title} already saved!`);
  };

  // Explore career learning path
  const handleExplore = (career) => {
    if (setSelectedCareer) setSelectedCareer(career);
    setPage("learning");
  };

  // Redirect to Career Analysis (Match Details)
  const handleMatchDetails = (career) => {
    if (setSelectedCareer) setSelectedCareer(career);
    setPage("career");
  };

  const cardBg = darkMode ? "#0b1220" : "#fff";
  const cardText = darkMode ? "#e6eef6" : "#062b3c";
  const pageBg = darkMode ? "#0f1720" : "#f4f8fb";

  return (
    <div style={{ minHeight: "80vh", padding: 20, fontFamily: "Arial, sans-serif", background: pageBg, color: cardText }}>
      <div style={{ maxWidth: 900, margin: "0 auto" }}>
        <h2 style={{ color: "#00b4d8", marginBottom: 12 }}>Career Recommendations</h2>

        {loading && (
          <div style={{ textAlign: "center", padding: 20, color: darkMode ? "#9aa7b5" : "#555" }}>
            Loading career recommendations...
          </div>
        )}

        <input
          placeholder="Search careers..."
          value={query}
          onChange={(e) => { setQuery(e.target.value); setIndex(0); }}
          style={{
            padding: 12,
            borderRadius: 10,
            border: darkMode ? "1px solid #333" : "1px solid #dde6ec",
            width: "100%",
            marginBottom: 20,
            fontSize: 16,
            background: darkMode ? "#0b1220" : "#fff",
            color: cardText,
          }}
        />

        <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 24 }}>
          <button
            onClick={handlePrev}
            style={{ ...navBtn, opacity: index === 0 ? 0.5 : 1 }}
            disabled={index === 0}
          >
            ◀
          </button>

          <div style={{ flex: 1, background: cardBg, padding: 18, borderRadius: 12, boxShadow: darkMode ? "0 2px 6px rgba(255,255,255,0.05)" : "0 2px 6px rgba(0,0,0,0.1)" }}>
            {filtered.length ? (
              <>
                <h3 style={{ margin: 0, color: cardText }}>{filtered[index % filtered.length].title}</h3>
                <p style={{ color: darkMode ? "#9aa7b5" : "#555", marginTop: 6 }}>{filtered[index % filtered.length].desc}</p>
                <div style={{ display: "flex", gap: 10, marginTop: 12 }}>
                  <button style={smallBtn} onClick={() => handleSave(filtered[index % filtered.length])}>Save</button>
                  <button style={smallBtn} onClick={() => handleExplore(filtered[index % filtered.length])}>Explore Path</button>
                  <button style={smallBtn} onClick={() => handleMatchDetails(filtered[index % filtered.length])}>Match Details</button>
                </div>
              </>
            ) : (
              <div style={{ color: "#999" }}>No results</div>
            )}
          </div>

          <button
            onClick={handleNext}
            style={{ ...navBtn, opacity: filtered.length === 0 ? 0.5 : 1 }}
            disabled={filtered.length === 0}
          >
            ▶
          </button>
        </div>

        {/* Grid view of all careers */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px,1fr))", gap: 12 }}>
          {careers.map((c) => (
            <div
              key={c.id}
              style={{
                background: cardBg,
                padding: 12,
                borderRadius: 12,
                boxShadow: darkMode ? "0 2px 6px rgba(255,255,255,0.05)" : "0 2px 6px rgba(0,0,0,0.05)",
                transition: "transform 0.2s",
                color: cardText,
                cursor: "pointer"
              }}
              onClick={() => handleMatchDetails(c)}
            >
              <h4 style={{ margin: "0 0 6px 0" }}>{c.title}</h4>
              <p style={{ fontSize: 14, margin: 0 }}>{c.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// Styles
const navBtn = {
  padding: "10px 14px",
  borderRadius: 8,
  border: "none",
  background: "#00b4d8",
  color: "#fff",
  cursor: "pointer",
  fontSize: 18,
};

const smallBtn = {
  padding: "8px 10px",
  borderRadius: 8,
  border: "none",
  background: "#0077b6",
  color: "#fff",
  cursor: "pointer",
  fontSize: 14,
  transition: "background 0.2s",
};
