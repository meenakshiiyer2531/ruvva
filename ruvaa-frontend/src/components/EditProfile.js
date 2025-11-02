import React, { useState, useEffect } from 'react';
import apiService from '../services/api';

// Dedicated Profile Editing Page
export default function EditProfile({ user, profile, setProfile, showToast, darkMode, setPage }) {
  const [form, setForm] = useState(() => ({ ...profile }));
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setForm({ ...profile });
  }, [profile]);

  if (!user) return <div style={wrapper}>Login required.</div>;

  const update = (key, value) => setForm(f => ({ ...f, [key]: value }));

  const submit = async (e) => {
    e.preventDefault();
    if (!user.id) return showToast && showToast('Missing user id','error');
    setSaving(true);
    try {
      // Decide between patch or create
      let resp;
      if (profile && Object.keys(profile).length) {
        resp = await apiService.patchStudentProfile(user.id, form);
      } else {
        resp = await apiService.createStudentProfile(user.id, form);
      }
      let newProfile;
      if (resp?.profile || resp?.data?.profile) newProfile = resp.profile || resp.data.profile;
      else throw new Error('Invalid server response');
      // Attempt combined re-fetch to guarantee server canonical data.
      try {
        const combined = await apiService.getStudentCombined(user.id);
        if (combined?.data?.profile) newProfile = combined.data.profile;
      } catch (e) { console.warn('⚠️ Combined fetch after save failed:', e.message); }
      setProfile({ ...newProfile });
      localStorage.setItem('cc_profile', JSON.stringify(newProfile));
      showToast && showToast('Profile saved','success');
      setPage && setPage('profile');
    } catch (err) {
      showToast && showToast('Save failed: ' + err.message,'error');
    } finally { setSaving(false); }
  };

  const cancel = () => {
    setPage && setPage('profile');
  };

  const field = (label, key, type='text') => (
    <label style={fieldWrap}>
      <span style={labelSpan}>{label}</span>
      {type === 'textarea' ? (
        <textarea value={form[key] || ''} onChange={e => update(key, e.target.value)} style={inputStyleTextArea} />
      ) : (
        <input type={type} value={form[key] || ''} onChange={e => update(key, e.target.value)} style={inputStyle} />
      )}
    </label>
  );

  // Chip editor factory for arrays
  const chipGroup = (label, key, options) => (
    <div style={chipGroupWrap}>
      <span style={labelSpan}>{label}</span>
      <div style={chipRow}>
        {options.map(opt => {
          const active = (form[key] || []).includes(opt);
          return (
            <button
              key={opt}
              type="button"
              onClick={() => update(key, active ? (form[key]||[]).filter(x=>x!==opt) : [ ...(form[key]||[]), opt ])}
              style={{ ...chip, background: active ? '#0077b6' : '#e2e8f0', color: active ? '#fff':'#0f172a' }}
            >{opt}</button>
          );
        })}
      </div>
    </div>
  );

  const boolToggle = (label, key) => (
    <label style={boolWrap}>
      <input
        type="checkbox"
        checked={!!form[key]}
        onChange={e => update(key, e.target.checked)}
        style={{ marginRight:6 }}
      />
      <span>{label}</span>
    </label>
  );

  return (
    <div style={wrapper}>
      <h2 style={{ color: '#0077b6', marginTop:0 }}>Edit Profile</h2>
      <form onSubmit={submit} style={formGrid}>
        {field('Name','name')}
        {field('Email','email','email')}
        {field('Grade Level','gradeLevel')}
        {field('City','city')}
        {field('State','state')}
        {field('Education Level','educationLevel')}
        {field('Institution','institutionName')}
        {field('Stream','stream')}
        {field('Phone','phoneNumber','tel')}
        {field('Age','age','number')}
        {field('Work Preference','workPreference')}
        {field('Expected Salary (LPA)','expectedSalaryLPA','number')}
        {field('CGPA','cgpa','number')}
        {field('Percentage','percentage','number')}
        {field('Graduation Year','graduationYear','number')}
        {field('Career Goal','currentCareerGoal')}
        {field('Aspirations','aspirations','textarea')}
        {chipGroup('Interested Domains','interestedDomains',["Technology & Software","Engineering","Healthcare","Business","Arts","Science","Education","Media","Sports","Social Work"])}
        {chipGroup('Preferred Locations','preferredLocations',["Mumbai","Bangalore","Delhi","Hyderabad","Chennai","Pune","Kolkata","International","Anywhere"])}
        {chipGroup('Learning Style','learningStyle',["Visual","Auditory","Kinesthetic","Reading/Writing","Collaborative","Independent"])}
        <div style={{ display:'flex', flexDirection:'column', gap:6, gridColumn:'1 / -1', marginTop:8 }}>
          {boolToggle('Agree To Terms','agreeToTerms')}
          {boolToggle('Agree To Privacy Policy','agreeToPrivacyPolicy')}
          {boolToggle('Onboarding Completed','onboardingCompleted')}
          {boolToggle('Profile Completed','profileCompleted')}
        </div>
        <div style={{ gridColumn:'1 / -1', display:'flex', gap:12, marginTop:12 }}>
          <button type="submit" disabled={saving} style={saveBtn}>{saving? 'Saving...' : 'Save'}</button>
          <button type="button" onClick={cancel} style={cancelBtn}>Cancel</button>
        </div>
      </form>
    </div>
  );
}

const wrapper = { maxWidth:900, margin:'0 auto', padding:20 };
const formGrid = { display:'grid', gap:16, gridTemplateColumns:'repeat(auto-fit,minmax(240px,1fr))' };
const fieldWrap = { display:'flex', flexDirection:'column', gap:6 };
const labelSpan = { fontSize:13, fontWeight:600 };
const inputStyle = { padding:10, borderRadius:8, border:'1px solid #cbd5e1', fontSize:14 };
const inputStyleTextArea = { ...inputStyle, minHeight:100, resize:'vertical' };
const saveBtn = { padding:'10px 18px', border:'none', borderRadius:8, background:'#0077b6', color:'#fff', cursor:'pointer' };
const cancelBtn = { ...saveBtn, background:'#64748b' };
const chipRow = { display:'flex', flexWrap:'wrap', gap:8, marginTop:6 };
const chip = { padding:'6px 10px', borderRadius:999, border:'none', cursor:'pointer', fontSize:12 };
const chipGroupWrap = { display:'flex', flexDirection:'column', gap:4 };
const boolWrap = { display:'flex', alignItems:'center', fontSize:14 };
