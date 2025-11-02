import React, { useState, useEffect } from "react";
import ApiService from "../services/api";

/*
  Enhanced Onboarding Component with Backend Integration
  Steps:
  1. Academic & Personal Details
  2. Interest Domains & Subjects  
  3. Skills & Learning Preferences
  4. Career Goals & Work Preferences
  5. Location & Salary Expectations
  
  Integrates with Spring Boot backend to update student profile
*/

export default function Onboarding({ initial, onComplete, showToast, setPage }) {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [user] = useState(() => JSON.parse(localStorage.getItem("cc_user")) || null);
  
  const [data, setData] = useState(initial || {
    // Academic Information
    educationLevel: user?.educationLevel || "",
    institutionName: user?.institutionName || "",
    stream: user?.stream || "",
    cgpa: "",
    percentage: "",
    graduationYear: new Date().getFullYear() + 2,
    
    // Interest & Skills
    interestedDomains: [],
    skillsAssessment: [],
    learningStyle: [],
    
    // Career Goals
    currentCareerGoal: "",
    recommendedCareers: [],
    workPreference: "",
    expectedSalaryLPA: "",
    
    // Location & Languages
    preferredLocations: [],
    preferredLanguages: ["English"],
    
    // Legacy fields for compatibility
    interests: [],
    extracurriculars: [],
    skills: {},
    aspirations: ""
  });

  useEffect(() => {
    const draft = JSON.parse(localStorage.getItem("cc_onboard_draft"));
    if (draft) setData(draft);
  }, []);

  useEffect(() => localStorage.setItem("cc_onboard_draft", JSON.stringify(data)), [data]);

  const toggleDomain = (domain) => {
    setData(d => ({
      ...d,
      interestedDomains: d.interestedDomains.includes(domain) 
        ? d.interestedDomains.filter(x => x !== domain) 
        : [...d.interestedDomains, domain]
    }));
  };

  const toggleLearningStyle = (style) => {
    setData(d => ({
      ...d,
      learningStyle: d.learningStyle.includes(style)
        ? d.learningStyle.filter(x => x !== style)
        : [...d.learningStyle, style]
    }));
  };

  const toggleLocation = (location) => {
    setData(d => ({
      ...d,
      preferredLocations: d.preferredLocations.includes(location)
        ? d.preferredLocations.filter(x => x !== location)
        : [...d.preferredLocations, location]
    }));
  };

  const addSkillAssessment = (skill, rating) => {
    setData(d => ({
      ...d,
      skillsAssessment: [...d.skillsAssessment.filter(s => s.skill !== skill), { skill, rating }]
    }));
  };

  const validateStep = () => {
    switch (step) {
      case 1:
        if (!data.institutionName.trim() || !data.stream.trim()) {
          return "Please fill in your institution and stream details.";
        }
        return null;
      case 2:
        if (data.interestedDomains.length === 0) {
          return "Please select at least one domain of interest.";
        }
        return null;
      case 3:
        if (data.skillsAssessment.length === 0 || data.learningStyle.length === 0) {
          return "Please complete skills assessment and select learning preferences.";
        }
        return null;
      case 4:
        if (!data.currentCareerGoal.trim() || !data.workPreference) {
          return "Please specify your career goal and work preference.";
        }
        return null;
      case 5:
        if (data.preferredLocations.length === 0 || !data.expectedSalaryLPA) {
          return "Please select preferred locations and expected salary.";
        }
        return null;
      default:
        return null;
    }
  };

  const handleNext = () => {
  const msg = validateStep();
  if (msg) { showToast && showToast(msg,'error'); return; }
    setStep(s => s + 1);
  };

  const submit = async () => {
  const msg = validateStep();
  if (msg) { showToast && showToast(msg,'error'); return; }
    
    setLoading(true);
    
    try {
      // Prepare profile data for backend update
      const profileUpdate = {
        interestedDomains: data.interestedDomains,
        skillsAssessment: data.skillsAssessment,
        preferredLocations: data.preferredLocations,
        workPreference: data.workPreference,
        expectedSalaryLPA: parseFloat(data.expectedSalaryLPA) || 0,
        learningStyle: data.learningStyle,
        currentCareerGoal: data.currentCareerGoal,
        cgpa: parseFloat(data.cgpa) || null,
        percentage: parseFloat(data.percentage) || null,
        graduationYear: parseInt(data.graduationYear) || null,
        profileCompleted: true,
        onboardingCompleted: true
      };

      // Update profile in backend if user exists
      let serverProfile = { ...data, ...profileUpdate };
      if (user && user.id) {
        console.log("📤 Updating student profile in backend...", profileUpdate);
        const response = await ApiService.updateStudentProfile(user.id, profileUpdate);
        console.log("✅ Profile updated successfully:", response);
        // Attempt combined re-fetch to ensure freshness
        try {
          const combined = await ApiService.getStudentCombined(user.id);
          if (combined?.data?.profile) serverProfile = { ...combined.data.profile };
        } catch (e) { console.warn('⚠️ Combined fetch after onboarding failed', e.message); }
      }
      onComplete(serverProfile);
      localStorage.removeItem("cc_onboard_draft");
      showToast && showToast("Onboarding completed successfully! 🎉", 'success');
      setPage && setPage('profile');
      
    } catch (error) {
      console.error("❌ Onboarding completion failed:", error);
      showToast && showToast("Failed to save profile. Please try again.", 'error');
    } finally {
      setLoading(false);
    }
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
          <div>
            <h3 style={{ color: "#00b4d8", marginBottom: 16 }}>Academic Information</h3>
            <div style={{ display: "grid", gap: 12 }}>
              <div>
                <label style={labelStyle}>Institution Name *</label>
                <input 
                  placeholder="Enter your college/university name" 
                  value={data.institutionName} 
                  onChange={e => setData(s => ({ ...s, institutionName: e.target.value }))} 
                  style={field} 
                />
              </div>
              <div>
                <label style={labelStyle}>Stream/Major *</label>
                <input 
                  placeholder="e.g. Computer Science, Mechanical Engineering" 
                  value={data.stream} 
                  onChange={e => setData(s => ({ ...s, stream: e.target.value }))} 
                  style={field} 
                />
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12 }}>
                <div>
                  <label style={labelStyle}>CGPA (optional)</label>
                  <input 
                    type="number" 
                    step="0.01" 
                    max="10" 
                    placeholder="0.0" 
                    value={data.cgpa} 
                    onChange={e => setData(s => ({ ...s, cgpa: e.target.value }))} 
                    style={field} 
                  />
                </div>
                <div>
                  <label style={labelStyle}>Percentage (optional)</label>
                  <input 
                    type="number" 
                    max="100" 
                    placeholder="0%" 
                    value={data.percentage} 
                    onChange={e => setData(s => ({ ...s, percentage: e.target.value }))} 
                    style={field} 
                  />
                </div>
                <div>
                  <label style={labelStyle}>Graduation Year</label>
                  <input 
                    type="number" 
                    min="2020" 
                    max="2030" 
                    placeholder="2025" 
                    value={data.graduationYear} 
                    onChange={e => setData(s => ({ ...s, graduationYear: e.target.value }))} 
                    style={field} 
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {step === 2 && (
          <div>
            <h3 style={{ color: "#00b4d8", marginBottom: 16 }}>Interest Domains</h3>
            <div style={{ marginBottom: 16 }}>Select domains that interest you (click to toggle)</div>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              {[
                "Technology & Software",
                "Engineering & Manufacturing", 
                "Healthcare & Medicine",
                "Business & Finance",
                "Arts & Design",
                "Science & Research",
                "Education & Teaching",
                "Media & Communication",
                "Sports & Fitness",
                "Social Work & NGO"
              ].map((domain) => (
                <button
                  key={domain}
                  onClick={() => toggleDomain(domain)}
                  style={{
                    ...chip,
                    background: data.interestedDomains.includes(domain) ? "#00b4d8" : "rgba(255,255,255,0.06)",
                    color: data.interestedDomains.includes(domain) ? "#fff" : "var(--text)"
                  }}
                >{domain}</button>
              ))}
            </div>
          </div>
        )}

        {step === 3 && (
          <div>
            <h3 style={{ color: "#00b4d8", marginBottom: 16 }}>Skills & Learning Preferences</h3>
            
            {/* Skills Assessment */}
            <div style={{ marginBottom: 20 }}>
              <h4 style={{ marginBottom: 12 }}>Rate Your Skills (1-10)</h4>
              {[
                "Problem Solving",
                "Communication", 
                "Leadership",
                "Technical Skills",
                "Creativity",
                "Analytical Thinking"
              ].map(skill => {
                const currentRating = data.skillsAssessment.find(s => s.skill === skill)?.rating || 5;
                return (
                  <div key={skill} style={{ marginBottom: 12 }}>
                    <label style={{ display: "block", fontSize: 14, color: "var(--muted)", marginBottom: 4 }}>
                      {skill}: {currentRating}/10
                    </label>
                    <input 
                      type="range" 
                      min="1" 
                      max="10" 
                      value={currentRating} 
                      onChange={(e) => addSkillAssessment(skill, parseInt(e.target.value))} 
                      style={{ width: "100%" }}
                    />
                  </div>
                );
              })}
            </div>

            {/* Learning Preferences */}
            <div>
              <h4 style={{ marginBottom: 12 }}>Learning Style Preferences</h4>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                {["Visual", "Auditory", "Kinesthetic", "Reading/Writing", "Collaborative", "Independent"].map((style) => (
                  <button
                    key={style}
                    onClick={() => toggleLearningStyle(style)}
                    style={{
                      ...chip,
                      background: data.learningStyle.includes(style) ? "#00b4d8" : "rgba(255,255,255,0.06)",
                      color: data.learningStyle.includes(style) ? "#fff" : "var(--text)"
                    }}
                  >{style}</button>
                ))}
              </div>
            </div>
          </div>
        )}

        {step === 4 && (
          <div>
            <h3 style={{ color: "#00b4d8", marginBottom: 16 }}>Career Goals & Work Preferences</h3>
            
            {/* Career Goal */}
            <div style={{ marginBottom: 20 }}>
              <label style={labelStyle}>What is your current career goal? *</label>
              <textarea
                value={data.currentCareerGoal}
                onChange={e => setData(s => ({ ...s, currentCareerGoal: e.target.value }))}
                style={{ ...field, minHeight: 100, width: "100%" }}
                placeholder="Describe your career aspirations, dream job, or field you want to work in..."
              />
            </div>

            {/* Work Preference */}
            <div>
              <label style={labelStyle}>Work Preference *</label>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 8 }}>
                {["Remote", "On-site", "Hybrid", "Flexible"].map((pref) => (
                  <button
                    key={pref}
                    onClick={() => setData(s => ({ ...s, workPreference: pref }))}
                    style={{
                      ...chip,
                      background: data.workPreference === pref ? "#00b4d8" : "rgba(255,255,255,0.06)",
                      color: data.workPreference === pref ? "#fff" : "var(--text)"
                    }}
                  >{pref}</button>
                ))}
              </div>
            </div>
          </div>
        )}

        {step === 5 && (
          <div>
            <h3 style={{ color: "#00b4d8", marginBottom: 16 }}>Location & Salary Expectations</h3>
            
            {/* Preferred Locations */}
            <div style={{ marginBottom: 20 }}>
              <label style={labelStyle}>Preferred Work Locations *</label>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 8 }}>
                {["Mumbai", "Bangalore", "Delhi", "Hyderabad", "Chennai", "Pune", "Kolkata", "Ahmedabad", "International", "Anywhere"].map((location) => (
                  <button
                    key={location}
                    onClick={() => toggleLocation(location)}
                    style={{
                      ...chip,
                      background: data.preferredLocations.includes(location) ? "#00b4d8" : "rgba(255,255,255,0.06)",
                      color: data.preferredLocations.includes(location) ? "#fff" : "var(--text)"
                    }}
                  >{location}</button>
                ))}
              </div>
            </div>

            {/* Expected Salary */}
            <div>
              <label style={labelStyle}>Expected Salary (LPA) *</label>
              <input
                type="number"
                min="0"
                step="0.5"
                placeholder="e.g. 6.5"
                value={data.expectedSalaryLPA}
                onChange={e => setData(s => ({ ...s, expectedSalaryLPA: e.target.value }))}
                style={field}
              />
              <div style={{ fontSize: 12, color: "var(--muted)", marginTop: 4 }}>
                Enter your expected salary in lakhs per annum
              </div>
            </div>
          </div>
        )}

        <div style={{ display: "flex", gap: 8, marginTop: 12, justifyContent: "space-between" }}>
          <div>
            {step > 1 && <button onClick={() => setStep(s => s - 1)} style={smallBtn}>Back</button>}
          </div>
          <div>
            {step < 5 && <button onClick={handleNext} style={smallBtnPrimary}>Next</button>}
            {step === 5 && (
              <button 
                onClick={submit} 
                disabled={loading}
                style={{
                  ...smallBtnPrimary,
                  opacity: loading ? 0.7 : 1,
                  cursor: loading ? 'not-allowed' : 'pointer'
                }}
              >
                {loading ? "Saving..." : "Finish & Save Profile"}
              </button>
            )}
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
const labelStyle = {
  display: "block",
  fontSize: 14,
  color: "var(--text)", 
  marginBottom: 8,
  fontWeight: "500"
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
