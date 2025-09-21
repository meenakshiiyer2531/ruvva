import React, { useState } from "react";
import { motion } from "framer-motion";
import { careers } from "./careersData";

export default function LearningPath({ profile, selectedCareer, setSelectedCareer }) {
  const [expanded, setExpanded] = useState({});

  const toggleCareer = id => setExpanded(e => ({ ...e, [id]: !e[id] }));

  const careersToShow = selectedCareer ? [selectedCareer] : careers;

  const handleRefresh = () => {
    if (setSelectedCareer) setSelectedCareer(null); // reset to show all careers
  };

  return (
    <div style={{ minHeight: "80vh", padding: 20 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <h2 style={{ color: "#0077b6" }}>Learning Path & Progress</h2>
        <button
          onClick={handleRefresh}
          style={{
            background: "transparent",
            border: "none",
            cursor: "pointer",
            fontSize: 20,
            color: "#0077b6"
          }}
          title="Show all careers"
        >
          🔄
        </button>
      </div>

      <div style={{ display: "grid", gap: 16, marginTop: 20, maxWidth: 900 }}>
        {careersToShow.map((c, i) => (
          <motion.div
            key={c.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            style={{ background: "var(--card)", padding: 16, borderRadius: 12 }}
          >
            <div
              style={{ display: "flex", justifyContent: "space-between", alignItems: "center", cursor: "pointer" }}
              onClick={() => toggleCareer(c.id)}
            >
              <strong>{c.title}</strong>
              <span style={{ fontSize: 14, color: "#0077b6" }}>{expanded[c.id] ? "▲" : "▼"}</span>
            </div>
            <p style={{ margin: "8px 0", color: "#555" }}>{c.desc}</p>

            {expanded[c.id] && c.learningPath && (
              <div style={{ marginTop: 12 }}>
                {c.learningPath.map((step, idx) => (
                  <div key={idx} style={{ marginBottom: 10 }}>
                    <strong>Step {idx + 1}: {step.step}</strong>
                    <ul style={{ marginTop: 4, marginLeft: 16 }}>
                      {step.resources.map((r, ri) => (
                        <li key={ri}>
                          <a href={r} target="_blank" rel="noopener noreferrer" style={{ color: "#00b4d8" }}>
                            {r}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
}
