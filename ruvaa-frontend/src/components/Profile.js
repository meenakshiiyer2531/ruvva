import React from "react";

import apiService from '../services/api';
export default function Profile({ user, profile, setProfile, darkMode, showToast }) {
  // Local deletion utility for saved careers (client-side only for now)
  const deleteCareer = (id) => {
    const updated = {
      ...profile,
      savedCareers: profile?.savedCareers?.filter(c => c.id !== id) || []
    };
    setProfile(updated);
    localStorage.setItem("cc_profile", JSON.stringify(updated));
    showToast && showToast('Removed career locally. Click Refresh to sync view.', 'info');
  };

  // Helper render arrays
  const basicFields = [
    { label: 'Name', key: 'name' },
    { label: 'Email', key: 'email' },
    { label: 'Grade Level', key: 'gradeLevel' },
    { label: 'City', key: 'city' },
    { label: 'State', key: 'state' },
    { label: 'Education Level', key: 'educationLevel' },
    { label: 'Institution', key: 'institutionName' },
    { label: 'Stream', key: 'stream' },
    { label: 'Phone', key: 'phoneNumber' },
    { label: 'Age', key: 'age' },
    { label: 'Work Preference', key: 'workPreference' },
    { label: 'Expected Salary (LPA)', key: 'expectedSalaryLPA' },
    { label: 'CGPA', key: 'cgpa' },
    { label: 'Percentage', key: 'percentage' },
    { label: 'Graduation Year', key: 'graduationYear' },
    { label: 'Career Goal', key: 'currentCareerGoal' }
  ];
  const listFields = [
    { label: 'Interested Domains', key: 'interestedDomains' },
    { label: 'Preferred Locations', key: 'preferredLocations' },
    { label: 'Learning Style', key: 'learningStyle' }
  ];
  const agreementFields = [
    { label: 'Agreed To Terms', key: 'agreeToTerms' },
    { label: 'Agreed To Privacy Policy', key: 'agreeToPrivacyPolicy' },
    { label: 'Onboarding Completed', key: 'onboardingCompleted' },
    { label: 'Profile Completed', key: 'profileCompleted' }
  ];

  // CRUD handlers (inside component to access props/state)
  const handleRefresh = async () => {
    try {
      if (!user?.id) return showToast && showToast('No user id to refresh','error');
      const resp = await apiService.getStudentCombined(user.id);
      if (resp?.data?.profile) {
        const combined = { ...resp.data.profile, email: user.email, name: user.name, gradeLevel: resp.data.data?.gradeLevel || resp.data.profile.gradeLevel };
        setProfile(combined);
        localStorage.setItem('cc_profile', JSON.stringify(combined));
        showToast && showToast('Profile refreshed','success');
      } else showToast && showToast('No profile found on server','error');
    } catch (e) { showToast && showToast('Refresh failed: ' + e.message,'error'); }
  };

  return (
    <div style={{ minHeight: "80vh", padding: 20, maxWidth: 900, margin: "0 auto" }}>
      <h2 style={{ color: "#0077b6" }}>Your Profile</h2>

      {
        <>
          <section style={sectionBox(darkMode)}>
            <h3 style={sectionTitle}>Basic Details</h3>
            <div style={gridTwo}>
              {basicFields.map(f => (
                <div key={f.key} style={infoRow}>
                  <span style={labelSpan}>{f.label}:</span>
                  <span>{(profile?.[f.key] ?? (f.key === 'email' && user?.email) ?? '—').toString()}</span>
                </div>
              ))}
            </div>
          </section>
          <section style={sectionBox(darkMode)}>
            <h3 style={sectionTitle}>Lists & Preferences</h3>
            {listFields.map(f => (
              <div key={f.key} style={{ marginBottom: 12 }}>
                <div style={labelSpan}>{f.label}:</div>
                <div style={pillRow}>
                  {(profile?.[f.key] && profile[f.key].length > 0) ? profile[f.key].map((val, idx) => (
                    <span key={idx} style={pill}>{typeof val === 'object' ? JSON.stringify(val) : String(val)}</span>
                  )) : <span style={{ opacity: 0.6 }}>None</span>}
                </div>
              </div>
            ))}
            {profile?.skillsAssessment?.length > 0 && (
              <div style={{ marginTop: 16 }}>
                <div style={labelSpan}>Skills Assessment:</div>
                <div style={pillRow}>
                  {profile.skillsAssessment.map((s, idx) => (
                    <span key={idx} style={pill}>{s.skill}: {s.rating}</span>
                  ))}
                </div>
              </div>
            )}
          </section>
          <section style={sectionBox(darkMode)}>
            <h3 style={sectionTitle}>Agreements & Status</h3>
            <div style={gridTwo}>
              {agreementFields.map(f => (
                <div key={f.key} style={infoRow}>
                  <span style={labelSpan}>{f.label}:</span>
                  <span>{profile?.[f.key] ? 'Yes' : 'No'}</span>
                </div>
              ))}
            </div>
          </section>
          <section style={sectionBox(darkMode)}>
            <h3 style={sectionTitle}>Other Fields</h3>
            <div style={infoRow}><span style={labelSpan}>Aspirations:</span> <span>{profile?.aspirations ?? '—'}</span></div>
            <div style={infoRow}><span style={labelSpan}>Saved Careers:</span> <span>{profile?.savedCareers?.length || 0}</span></div>
            {profile?.riasecScores && (
              <div style={{marginTop:16}}>
                <h4 style={{margin:'0 0 8px', color:'#0077b6'}}>RIASEC Scores</h4>
                <div style={{display:'grid', gap:8}}>
                  {Object.entries(profile.riasecScores).map(([axis, pct]) => (
                    <div key={axis} style={{display:'flex', alignItems:'center', gap:10}}>
                      <div style={{width:120}}>{axis}</div>
                      <div style={{flex:1, height:10, background:'#e2e8f0', borderRadius:6}}>
                        <div style={{width:`${pct}%`, height:10, background:'#00b4d8', borderRadius:6}} />
                      </div>
                      <div style={{width:40, textAlign:'right', fontSize:12}}>{pct}%</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {profile?.assessmentHistory && profile.assessmentHistory.length > 0 && (
              <div style={{marginTop:20}}>
                <h4 style={{margin:'0 0 8px', color:'#0077b6'}}>Assessment History</h4>
                <ul style={{margin:0, paddingLeft:18, fontSize:13}}>
                  {profile.assessmentHistory.slice().reverse().map((run, idx) => (
                    <li key={idx} style={{marginBottom:6}}>
                      <strong>{new Date(run.timestamp).toLocaleString()}</strong> – {run.riasecScores ? Object.entries(run.riasecScores).map(([a,p])=>`${a}:${p}%`).join(', ') : 'No scores'}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {(profile?.bookings || []).length > 0 && (
              <div style={{marginTop:24}}>
                <h4 style={{margin:'0 0 8px', color:'#0077b6'}}>Mentor Bookings</h4>
                <div style={{display:'grid', gap:10}}>
                  {profile.bookings.sort((a,b)=> new Date(a.date) - new Date(b.date)).map(b => {
                    const upcoming = new Date(b.date) >= new Date();
                    const fixedMeet = 'https://meet.google.com/eje-rdfq-ksk';
                    if (!b.meetingLink) b.meetingLink = fixedMeet; // UI override only
                    const hasLink = true;
                    const lightUpcoming = '#e0f7ff';
                    const lightPast = '#f1f5f9';
                    const darkUpcoming = '#0f3b4a';
                    const darkPast = '#1f2937';
                    const bg = darkMode ? (upcoming ? darkUpcoming : darkPast) : (upcoming ? lightUpcoming : lightPast);
                    const statusColor = darkMode ? '#cbd5e1' : '#555';
                    const metaColor = darkMode ? '#94a3b8' : '#64748b';
                    return (
                      <button onClick={()=> window.dispatchEvent(new CustomEvent('navigate',{ detail:{ page:'bookingDetail', bookingId: b.id }}))} key={b.id} style={{textAlign:'left', padding:12, borderRadius:10, background:bg, border:'1px solid var(--border)', cursor:'pointer', color:'var(--text)'}}>
                        <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
                          <div style={{fontSize:14}}><strong>{b.mentorName || b.mentorId}</strong> — {new Date(b.date).toLocaleDateString()}</div>
                          {hasLink && <span style={{fontSize:11, background:'#0077b6', color:'#fff', padding:'2px 6px', borderRadius:6}}>Meet Link</span>}
                        </div>
                        <div style={{fontSize:12, color:statusColor}}>Status: {b.status}</div>
                        <div style={{fontSize:11, color:metaColor, marginTop:4}}>Booked {new Date(b.createdAt).toLocaleString()}</div>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </section>
          <div style={{ display:'flex', flexWrap:'wrap', gap:8, marginTop:16 }}>
            <button onClick={() => window.dispatchEvent(new CustomEvent('navigate',{ detail: { page: 'editProfile' } }))} style={btn}>Edit Profile</button>
            <button onClick={handleRefresh} style={btnAlt}>Refresh</button>
          </div>
        </>
      }

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
// (Removed inline edit field styles no longer used)

const btn = {
  padding: "10px 16px",
  borderRadius: 10,
  border: "none",
  background: "#00b4d8",
  color: "#fff",
  cursor: "pointer"
};

// (Removed btnMuted; editing inline no longer supported here)
const deleteBtn = {
  padding: "6px 10px",
  borderRadius: 8,
  border: "none",
  background: "#ef4444",
  color: "#fff",
  cursor: "pointer"
};
const btnAlt = { ...btn, background: '#0369a1' };

// New styling helpers
const sectionBox = (dark) => ({
  marginTop: 24,
  padding: 16,
  borderRadius: 12,
  background: dark ? 'var(--card)' : '#f8fafc',
  border: dark ? '1px solid var(--border)' : '1px solid #e2e8f0',
  boxShadow: dark ? '0 1px 2px rgba(0,0,0,0.4)' : '0 1px 2px rgba(0,0,0,0.05)'
});
const sectionTitle = { margin: 0, marginBottom: 12, color: '#0077b6', fontSize: 18 };
const gridTwo = { display: 'grid', gap: 12, gridTemplateColumns: 'repeat(auto-fit,minmax(240px,1fr))' };
const infoRow = { display: 'flex', flexDirection: 'column', fontSize: 14 };
const labelSpan = { fontWeight: 600, marginBottom: 2 };
const pillRow = { display: 'flex', gap: 8, flexWrap: 'wrap', marginTop: 4 };
const pill = { padding: '4px 10px', background: '#0077b6', color: '#fff', borderRadius: 999, fontSize: 12 };

// (Removed duplicate out-of-component CRUD handlers; in-component handlers are used.)
