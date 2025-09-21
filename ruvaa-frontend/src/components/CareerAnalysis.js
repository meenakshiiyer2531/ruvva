import React, { useState } from "react";
import { Radar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from "chart.js";
import { careers, RIASEC_INFO } from "./careersData";

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

export default function CareerAnalysis({ profile, setProfile, setPage, setSelectedCareer, darkMode }) {
  const stats = { Realistic: 60, Investigative: 80, Artistic: 55, Social: 45, Enterprising: 50, Conventional: 35 };
  
  const radarData = {
    labels: Object.keys(stats),
    datasets: [{
      label: "RIASEC",
      data: Object.values(stats),
      backgroundColor: darkMode ? "rgba(0,180,216,0.25)" : "rgba(0,180,216,0.15)",
      borderColor: "#00b4d8",
      pointBackgroundColor: "#0077b6",
      fill: true
    }]
  };

  const [search, setSearch] = useState("");

  const filteredCareers = careers.filter(c =>
    c.title.toLowerCase().includes(search.toLowerCase()) ||
    c.tags.some(t => t.toLowerCase().includes(search.toLowerCase()))
  );

  const handleSave = career => {
    if (!profile.savedCareers?.some(c => c.id === career.id)) {
      const updated = { ...profile, savedCareers: [...(profile.savedCareers || []), career] };
      setProfile(updated);
      localStorage.setItem("cc_profile", JSON.stringify(updated));
      alert(`${career.title} saved!`);
    } else alert(`${career.title} already saved!`);
  };

  const handleLearnPath = career => {
    setSelectedCareer(career);
    setPage("learning");
  };

  return (
    <div style={{
      minHeight: "90vh",
      padding: 20,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: 20,
      background: darkMode ? "#0f1720" : "#f4f8fb",
      color: darkMode ? "#e6eef6" : "#062b3c"
    }}>
      <h2 style={{ color: "#00b4d8" }}>Your Career Insights</h2>

      <div style={{
        background: darkMode ? "#0b1220" : "#fff",
        padding: 20,
        borderRadius: 16,
        width: "100%",
        maxWidth: 600,
        boxShadow: darkMode ? "0 4px 15px rgba(255,255,255,0.05)" : "0 4px 15px rgba(0,0,0,0.1)"
      }}>
        <h3 style={{ margin: 0, color: "#00b4d8" }}>RIASEC Radar</h3>
        <Radar
          data={radarData}
          options={{
            responsive: true,
            maintainAspectRatio: true,
            scales: {
              r: {
                angleLines: { color: darkMode ? "rgba(255,255,255,0.2)" : "rgba(0,0,0,0.2)" },
                grid: { color: darkMode ? "rgba(255,255,255,0.1)" : "rgba(0,0,0,0.1)" },
                pointLabels: { color: darkMode ? "#e6eef6" : "#062b3c" },
                ticks: { color: darkMode ? "#e6eef6" : "#062b3c" }
              }
            },
            plugins: {
              tooltip: {
                callbacks: {
                  label: ctx => `${ctx.label}: ${stats[ctx.label]} — ${RIASEC_INFO[ctx.label]}`
                }
              },
              legend: { labels: { color: darkMode ? "#e6eef6" : "#062b3c" } }
            }
          }}
        />
        <p style={{ marginTop: 10, fontSize: 13, color: darkMode ? "#9aa7b5" : "#555" }}>
          Hover over points to see RIASEC meaning.
        </p>
      </div>

      <input
        placeholder="Search careers by name or tag..."
        value={search}
        onChange={e => setSearch(e.target.value)}
        style={{
          width: "100%",
          maxWidth: 920,
          padding: 12,
          borderRadius: 12,
          border: darkMode ? "1px solid #333" : "1px solid #dde6ec",
          background: darkMode ? "#0b1220" : "#fff",
          color: darkMode ? "#e6eef6" : "#062b3c",
          fontSize: 16
        }}
      />

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(280px,1fr))",
        gap: 20,
        width: "100%",
        maxWidth: 920
      }}>
        {filteredCareers.map(c => (
          <div key={c.id} style={{
            padding: 20,
            borderRadius: 16,
            background: darkMode ? "#0b1220" : "#fff",
            color: darkMode ? "#e6eef6" : "#062b3c",
            boxShadow: darkMode ? "0 4px 10px rgba(255,255,255,0.05)" : "0 6px 20px rgba(0,0,0,0.1)",
            transition: "all 0.3s"
          }}>
            <h4 style={{ color: "#00b4d8" }}>{c.title}</h4>
            <p>{c.desc}</p>
            <div style={{ fontSize: 12, color: darkMode ? "#9aa7b5" : "#555" }}>Tags: {c.tags.join(", ")}</div>
            <div style={{
              marginTop: 8,
              height: 10,
              background: darkMode ? "rgba(255,255,255,0.05)" : "rgba(0,0,0,0.06)",
              borderRadius: 8
            }}>
              <div style={{
                width: `${Math.round(c.scoreMatch * 100)}%`,
                height: 10,
                background: "#00b4d8",
                borderRadius: 8
              }} />
            </div>
            <div style={{ marginTop: 4, fontSize: 12, color: darkMode ? "#9aa7b5" : "#555" }}>
              Match: {Math.round(c.scoreMatch * 100)}%
            </div>
            <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
              <button onClick={() => handleSave(c)} style={cardBtn}>Save</button>
              <button onClick={() => handleLearnPath(c)} style={cardBtn}>Learn Path</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

const cardBtn = {
  flex: 1,
  padding: "8px 10px",
  borderRadius: 8,
  border: "none",
  background: "#00b4d8",
  color: "#fff",
  fontWeight: 600,
  cursor: "pointer",
  textAlign: "center",
  transition: "background 0.2s",
  fontSize: 14
};
