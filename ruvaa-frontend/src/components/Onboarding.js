import React, { useState, useEffect } from "react";

/*
  Steps:
  1 Basic Info
  2 Academic interests
  3 Extracurriculars
  4 Skills assessment (quick)
  5 Aspirations
  Saves draft to localStorage; returns profile object to parent on complete
*/

export default function Onboarding({ initial, onComplete }) {
  const [step, setStep] = useState(1);
  const [data, setData] = useState(initial || {
    name: "", studentClass: "", location: "",
    interests: [], extracurriculars: [], skills: {}, aspirations: ""
  });

  useEffect(() => {
    const draft = JSON.parse(localStorage.getItem("cc_onboard_draft"));
    if (draft) setData(draft);
  }, []);

  useEffect(() => localStorage.setItem("cc_onboard_draft", JSON.stringify(data)), [data]);

  const toggleInterest = (v) => {
    setData(d => ({
      ...d,
      interests: d.interests.includes(v) ? d.interests.filter(x => x !== v) : [...d.interests, v]
    }));
  };

  const setSkill = (k, v) => setData(d => ({ ...d, skills: { ...d.skills, [k]: v } }));

  const validateStep = () => {
    switch (step) {
      case 1:
        if (!data.name.trim() || !data.studentClass.trim()) return "Please fill in your name and class/year.";
        return null;
      case 2:
        if (data.interests.length === 0) return "Please select at least one subject you like.";
        return null;
      case 3:
        if (data.extracurriculars.length === 0) return "Please mention at least one extracurricular activity.";
        return null;
      case 5:
        if (!data.aspirations.trim()) return "Please write your career aspirations or constraints.";
        return null;
      default:
        return null;
    }
  };

  const handleNext = () => {
    const msg = validateStep();
    if (msg) return alert(msg);
    setStep(s => s + 1);
  };

  const submit = () => {
    const msg = validateStep();
    if (msg) return alert(msg);
    onComplete(data);
    localStorage.removeItem("cc_onboard_draft");
  };

  return (
    <div style={{ minHeight: "80vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 20 }}>
      <div style={{
        width: "94%", maxWidth: 980, background: "var(--card)", borderRadius: 16,
        padding: 18, boxShadow: "0 10px 40px rgba(2,6,23,0.18)"
      }}>
        <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 12 }}>
          <h2 style={{ margin: 0, color: "#00b4d8" }}>Student Onboarding</h2>
          <div style={{ color: "var(--muted)" }}>Step {step} / 5</div>
        </div>

        {step === 1 && (
          <div style={{ display: "grid", gap: 10 }}>
            <input placeholder="Full name" value={data.name} onChange={e => setData(s => ({ ...s, name: e.target.value }))} style={field} />
            <input placeholder="Class / Year" value={data.studentClass} onChange={e => setData(s => ({ ...s, studentClass: e.target.value }))} style={field} />
            <input placeholder="Location (city)" value={data.location} onChange={e => setData(s => ({ ...s, location: e.target.value }))} style={field} />
          </div>
        )}

        {step === 2 && (
          <div>
            <div style={{ marginBottom: 8 }}>Choose subjects you like (click to toggle)</div>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              {["Mathematics","Physics","Biology","Chemistry","Computer Science","Economics","Arts","Commerce"].map((s) => (
                <button
                  key={s}
                  onClick={() => toggleInterest(s)}
                  style={{
                    ...chip,
                    background: data.interests.includes(s) ? "#00b4d8" : "rgba(255,255,255,0.06)",
                    color: data.interests.includes(s) ? "#fff" : "var(--text)"
                  }}
                >{s}</button>
              ))}
            </div>
          </div>
        )}

        {step === 3 && (
          <div>
            <div style={{ marginBottom: 8 }}>Extracurricular activities (comma separated)</div>
            <input
              placeholder="e.g. dance, coding club, cricket"
              value={data.extracurriculars.join(", ")}
              onChange={e => setData(s => ({
                ...s,
                extracurriculars: e.target.value.split(",").map(x => x.trim()).filter(Boolean)
              }))}
              style={field}
            />
          </div>
        )}

        {step === 4 && (
          <div>
            <div style={{ marginBottom: 8 }}>Self-rate skills (0-100)</div>
            {["Problem solving","Creativity","Communication","Technical"].map(k => (
              <div key={k} style={{ marginBottom: 10 }}>
                <label style={{ display: "block", fontSize: 13, color: "var(--muted)" }}>{k}</label>
                <input type="range" min="0" max="100" value={data.skills[k] ?? 50} onChange={(e) => setSkill(k, Number(e.target.value))} />
                <div style={{ fontSize: 13 }}>{data.skills[k] ?? 50}</div>
              </div>
            ))}
          </div>
        )}

        {step === 5 && (
          <div>
            <div style={{ marginBottom: 8 }}>Career aspirations / constraints</div>
            <textarea
              value={data.aspirations}
              onChange={e => setData(s => ({ ...s, aspirations: e.target.value }))}
              style={{ ...field, minHeight: 120, width: "100%" }}
              placeholder="What do you hope to become? Any constraints (location, finances)?"
            />
          </div>
        )}

        <div style={{ display: "flex", gap: 8, marginTop: 12, justifyContent: "space-between" }}>
          <div>
            {step > 1 && <button onClick={() => setStep(s => s - 1)} style={smallBtn}>Back</button>}
          </div>
          <div>
            {step < 5 && <button onClick={handleNext} style={smallBtnPrimary}>Next</button>}
            {step === 5 && <button onClick={submit} style={smallBtnPrimary}>Finish & Save</button>}
          </div>
        </div>
      </div>
    </div>
  );
}

const field = {
  padding: 12,
  borderRadius: 10,
  border: "1px solid #d6dbe1",
  background: "transparent",
  color: "var(--text)"
};
const chip = {
  padding: "8px 12px",
  borderRadius: 999,
  border: "none",
  cursor: "pointer"
};
const smallBtn = {
  padding: "8px 12px",
  borderRadius: 8,
  border: "1px solid #d6dbe1",
  background: "transparent",
  cursor: "pointer",
  color: "var(--text)"
};
const smallBtnPrimary = { ...smallBtn, background: "#00b4d8", color: "#fff", border: "none" };
