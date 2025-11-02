import React, { useState, useEffect } from "react";
import ApiService from "../services/api";

/* RIASEC Assessment Revamp
   - Dynamic randomized questions each session
   - RIASEC axes: Realistic, Investigative, Artistic, Social, Enterprising, Conventional
   - 5 questions per axis (configurable) drawn from pools
   - Scoring: Agree=2, Neutral=1, Disagree=0
   - Percentage score per axis = (sum / (maxPerAxis)) * 100
   - Persist results to profile (patch) under profile.riasecScores
*/

const RIASEC_AXES = ["Realistic","Investigative","Artistic","Social","Enterprising","Conventional"];

// Question pool (can expand further)
const QUESTION_POOL = {
  Realistic: [
    "I enjoy working with tools and machinery",
    "I like fixing physical objects",
    "Outdoor or hands-on tasks appeal to me",
    "I prefer practical activities over theoretical ones",
    "I feel comfortable assembling or repairing things"
  ],
  Investigative: [
    "I enjoy solving complex problems",
    "Researching why things happen interests me",
    "I like analyzing data or patterns",
    "I prefer tasks that require critical thinking",
    "I get curious about the underlying mechanics of systems"
  ],
  Artistic: [
    "I enjoy expressing ideas creatively",
    "I like experimenting with design or style",
    "I appreciate unstructured, open-ended tasks",
    "I engage in creative hobbies (music, writing, art)",
    "I prefer freedom over strict rules in projects"
  ],
  Social: [
    "I enjoy helping or teaching others",
    "I gain energy from collaborating in groups",
    "I like listening and supporting people",
    "I prefer roles that involve communication",
    "I feel fulfilled when I make a positive impact on people"
  ],
  Enterprising: [
    "I enjoy leading initiatives or teams",
    "I like persuading or influencing decisions",
    "I feel confident taking calculated risks",
    "I am motivated by achieving ambitious goals",
    "I often take charge in group situations"
  ],
  Conventional: [
    "I prefer organized, structured tasks",
    "I enjoy working with data, records or spreadsheets",
    "I like following clear procedures",
    "I pay attention to detail and accuracy",
    "I feel comfortable planning and scheduling work"
  ]
};

const QUESTIONS_PER_AXIS = parseInt(process.env.REACT_APP_RIASEC_QUESTIONS_PER_AXIS || '5');

export default function Assessment({ user, showToast, profile, setProfile }) {
  const [sessionQuestions, setSessionQuestions] = useState([]); // flattened list of {id,text,axis}
  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState([]); // {q,axis,score}
  const [completed, setCompleted] = useState(false);
  // Removed legacy loading state (not required with simplified flow)
  const [analysisResult, setAnalysisResult] = useState(null);
  const [persisting, setPersisting] = useState(false);

  // Generate randomized question set each mount
  useEffect(() => {
    const generated = [];
    let qId = 1;
    RIASEC_AXES.forEach(axis => {
      const pool = QUESTION_POOL[axis];
      const shuffled = [...pool].sort(()=>Math.random()-0.5).slice(0, QUESTIONS_PER_AXIS);
      shuffled.forEach(text => generated.push({ id: qId++, text, axis }));
    });
    // Shuffle overall order but preserve axis distribution randomness
    const finalSet = generated.sort(()=>Math.random()-0.5);
    setSessionQuestions(finalSet);
  }, []);

  const current = sessionQuestions[idx];

  const answer = async (score) => {
    if (!current) return;
    const newAnswers = [...answers, { q: current.id, axis: current.axis, score }];
    setAnswers(newAnswers);
    if (idx + 1 < sessionQuestions.length) {
      setIdx(i => i + 1);
    } else {
      // Completed answering
      try {
        // Optional backend assessment submission if endpoint exists
        if (ApiService.submitAssessment) {
          const result = await ApiService.submitAssessment({ answers: newAnswers, totalQuestions: sessionQuestions.length });
          setAnalysisResult(result);
        }
      } catch (e) {
        console.warn('Assessment submit failed, continuing with local scoring:', e.message);
      } finally {
        setCompleted(true);
      }
    }
  };

  // Aggregate scores per axis
  const axisScores = answers.reduce((acc, cur) => {
    acc[cur.axis] = (acc[cur.axis] || 0) + cur.score; return acc;
  }, {});
  const maxPerAxis = QUESTIONS_PER_AXIS * 2; // Agree=2
  const [manualAdjust, setManualAdjust] = useState({}); // axis -> percent override
  const percentScores = RIASEC_AXES.map(axis => {
    const computed = Math.round(((axisScores[axis] || 0) / maxPerAxis) * 100);
    return {
      axis,
      raw: axisScores[axis] || 0,
      percent: manualAdjust[axis] !== undefined ? manualAdjust[axis] : computed
    };
  });
  // Sort for dominant axes
  const sortedAxes = [...percentScores].sort((a,b)=>b.percent - a.percent);

  const persistResults = async () => {
    if (!user?.id) { showToast && showToast('Cannot persist: user missing','error'); return; }
    setPersisting(true);
    try {
      const riasecScores = percentScores.reduce((acc, s) => { acc[s.axis] = s.percent; return acc; }, {});
      const patch = { riasecScores, profileCompleted: true };
      const resp = await ApiService.patchStudentProfile(user.id, { ...(profile||{}), ...patch });
      let newProfile = resp?.data?.profile || resp?.profile || { ...(profile||{}), ...patch };
      // Store assessment run history (including raw answers for analytics)
      try {
        await ApiService.addAssessmentRun(user.id, { riasecScores, rawAnswers: answers, totalQuestions: sessionQuestions.length });
      } catch(e){ console.warn('Failed to store assessment run history', e.message); }
      // Attempt combined refresh
      try {
        const combined = await ApiService.getStudentCombined(user.id);
        if (combined?.data?.profile) newProfile = combined.data.profile;
      } catch (e) { /* swallow */ }
      setProfile && setProfile(newProfile);
      localStorage.setItem('cc_profile', JSON.stringify(newProfile));
      showToast && showToast('RIASEC assessment saved to profile','success');
    } catch (e) {
      console.error('Persist failed:', e);
      showToast && showToast('Failed to persist assessment','error');
    } finally { setPersisting(false); }
  };

  // Career mapping suggestions based on top axis pairs
  const axisToCareers = {
    Realistic: ["Mechanical Engineer","Field Technician","Architectural Drafter"],
    Investigative: ["Data Scientist","Research Analyst","Biomedical Scientist"],
    Artistic: ["UX Designer","Graphic Designer","Content Creator"],
    Social: ["Teacher","Counselor","Community Manager"],
    Enterprising: ["Product Manager","Entrepreneur","Sales Lead"],
    Conventional: ["Operations Analyst","Accountant","Quality Coordinator"]
  };
  const comboCareers = {
    "Investigative+Artistic": ["Data Visualization Specialist","UX Researcher"],
    "Investigative+Enterprising": ["Tech Startup Analyst","Innovation Consultant"],
    "Artistic+Social": ["Instructional Designer","Creative Workshop Facilitator"],
    "Social+Enterprising": ["Program Director","EdTech Evangelist"],
    "Realistic+Investigative": ["Robotics Engineer","Environmental Analyst"],
    "Conventional+Enterprising": ["Project Coordinator","Business Operations Lead"]
  };
  const topTwoKey = sortedAxes.length >=2 ? `${sortedAxes[0].axis}+${sortedAxes[1].axis}` : null;
  const mappedCareers = [ ...(axisToCareers[sortedAxes[0].axis]||[]), ...(topTwoKey && comboCareers[topTwoKey] ? comboCareers[topTwoKey] : []) ].slice(0,6);

  const motivationBlurb = (() => {
    if (!sortedAxes.length) return '';
    const top = sortedAxes[0];
    switch (top.axis) {
      case 'Investigative': return 'Your curiosity and analytical mindset shine. Pursue domains that let you explore data, patterns, and complex systems.';
      case 'Artistic': return 'Creative energy is a core strength. Seek roles allowing design, storytelling, or expressive innovation.';
      case 'Social': return 'You thrive when uplifting others. Collaborative and service-oriented paths can accelerate your growth.';
      case 'Enterprising': return 'Leadership and initiative drive you. Consider roles with ownership, strategy, and impact potential.';
      case 'Conventional': return 'Structure and precision empower you. Data stewardship and operational excellence may fit well.';
      case 'Realistic': return 'Hands-on practicality guides you. Explore engineering, technical craftsmanship, or applied building tasks.';
      default: return '';
    }
  })();

  return (
    <div style={{ minHeight:"80vh", display:"flex", alignItems:"center", justifyContent:"center", padding:20 }}>
      {!completed ? (
        <div style={card}>
          <h2 style={{color:"#0077b6"}}>RIASEC Career Assessment</h2>
          <p style={{fontSize:14, color:"var(--muted)", marginTop:-4}}>Session generates fresh questions every time.</p>
          {current ? (
            <>
              <div style={{marginTop:18, fontSize:18}}>{current.text}</div>
              <div style={{display:"flex", gap:12, justifyContent:"center", marginTop:18}}>
                <button style={btn} onClick={()=>answer(2)}>Agree</button>
                <button style={btnMuted} onClick={()=>answer(1)}>Neutral</button>
                <button style={btn} onClick={()=>answer(0)}>Disagree</button>
              </div>
              <div style={{marginTop:16, color:"var(--muted)"}}>Progress {idx+1}/{sessionQuestions.length}</div>
              <div style={{marginTop:4, fontSize:12, color:"var(--muted)"}}>Axis: <strong>{current.axis}</strong></div>
            </>
          ) : <div>Loading questions...</div>}
        </div>
      ) : (
        <div style={card}>
          <h2 style={{color:"#0077b6"}}>Your RIASEC Profile</h2>
          <p style={{color:"var(--muted)"}}>{analysisResult ? 'AI-enhanced interpretation' : 'Local scoring summary'}</p>
          <div style={{display:'grid', gap:10, marginTop:12}}>
            {percentScores.map(s => (
              <div key={s.axis} style={{display:'flex', alignItems:'center', gap:10}}>
                <div style={{width:130}}>{s.axis}</div>
                <div style={{flex:1, height:12, background:'#e2e8f0', borderRadius:8}}>
                  <div style={{width:`${s.percent}%`, height:12, background:'#00b4d8', borderRadius:8}}/>
                </div>
                <div style={{width:50, textAlign:'right'}}>{s.percent}%</div>
              </div>
            ))}
          </div>
          <div style={{marginTop:18, padding:16, background:'rgba(0,0,0,0.05)', borderRadius:12}}>
            <h3 style={{margin:'0 0 8px', color:'#0077b6'}}>Adjust Scores (Optional)</h3>
            <p style={{margin:'0 0 12px', fontSize:13, color:'var(--muted)'}}>Fine-tune perceived strengths before saving.</p>
            <div style={{display:'grid', gap:12}}>
              {percentScores.map(s => (
                <div key={s.axis} style={{display:'flex', flexDirection:'column'}}>
                  <label style={{fontSize:12, fontWeight:600, marginBottom:4}}>{s.axis}: {manualAdjust[s.axis] !== undefined ? manualAdjust[s.axis] : s.percent}%</label>
                  <input type='range' min='0' max='100' value={manualAdjust[s.axis] !== undefined ? manualAdjust[s.axis] : s.percent} onChange={e => setManualAdjust(m => ({...m, [s.axis]: parseInt(e.target.value)}))} />
                </div>
              ))}
            </div>
            <button style={smallResetBtn} type='button' onClick={()=>setManualAdjust({})}>Reset Adjustments</button>
          </div>
          <div style={{marginTop:18, background:'rgba(0,180,216,0.1)', padding:16, borderRadius:12}}>
            <h3 style={{margin:'0 0 8px', color:'#0077b6'}}>Top Strengths</h3>
            <ul style={{margin:0, paddingLeft:20, textAlign:'left'}}>
              {sortedAxes.slice(0,3).map(s => <li key={s.axis}>{s.axis} ({s.percent}%)</li>)}
            </ul>
          </div>
          <div style={{marginTop:18, background:'rgba(0,180,216,0.06)', padding:16, borderRadius:12, textAlign:'left'}}>
            <h3 style={{margin:'0 0 8px', color:'#0077b6'}}>Motivation Insight</h3>
            <p style={{margin:0, fontSize:14, lineHeight:1.5}}>{motivationBlurb}</p>
          </div>
          <div style={{marginTop:18, background:'rgba(0,180,216,0.08)', padding:16, borderRadius:12, textAlign:'left'}}>
            <h3 style={{margin:'0 0 8px', color:'#0077b6'}}>Career Mapping (Top Axes)</h3>
            <ul style={{margin:0, paddingLeft:20}}>
              {mappedCareers.map(c => <li key={c}>{c}</li>)}
            </ul>
          </div>
          {analysisResult && analysisResult.recommendations && (
            <div style={{marginTop:18, padding:16, background:'rgba(0,180,216,0.08)', borderRadius:12}}>
              <h3 style={{margin:'0 0 8px', color:'#0077b6'}}>Career Recommendations</h3>
              <ul style={{margin:0, paddingLeft:20, textAlign:'left'}}>
                {analysisResult.recommendations.map((rec,i)=>(<li key={i}>{rec}</li>))}
              </ul>
            </div>
          )}
          <div style={{display:'flex', flexWrap:'wrap', gap:12, marginTop:24}}>
            <button style={btn} onClick={() => {
              setIdx(0); setAnswers([]); setCompleted(false); setAnalysisResult(null); setSessionQuestions([]);
              // regenerate
              const generated=[]; let qId=1; RIASEC_AXES.forEach(axis=>{ const pool=QUESTION_POOL[axis]; const shuffled=[...pool].sort(()=>Math.random()-0.5).slice(0,QUESTIONS_PER_AXIS); shuffled.forEach(text=>generated.push({id:qId++, text, axis})); });
              setSessionQuestions(generated.sort(()=>Math.random()-0.5));
            }}>Retake Assessment</button>
            <button disabled={persisting} style={persistBtn} onClick={persistResults}>{persisting? 'Saving...' : 'Save to Profile'}</button>
          </div>
        </div>
      )}
    </div>
  );
}

const card = { background:"var(--card)", padding:24, borderRadius:16, boxShadow:"0 10px 30px rgba(2,6,23,0.15)", width:"94%", maxWidth:820, textAlign:"center" };
const btn = { padding:"10px 18px", borderRadius:10, border:"none", background:"#00b4d8", color:"#fff", cursor:"pointer", minWidth:110 };
const btnMuted = { ...btn, background:"#64748b" };
const persistBtn = { ...btn, background:'#0369a1' };
const smallResetBtn = { marginTop:12, padding:'6px 12px', border:'none', background:'#0077b6', color:'#fff', borderRadius:6, cursor:'pointer', fontSize:12, alignSelf:'flex-start' };
