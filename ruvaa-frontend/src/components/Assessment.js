import React, { useState } from "react";
import ApiService from "../services/api";

export default function Assessment(){
  const questions = [
    {id:1, text:"I enjoy solving puzzles/problems", axis:"Investigative"},
    {id:2, text:"I like building or fixing things", axis:"Realistic"},
    {id:3, text:"I enjoy creative arts (drawing, writing)", axis:"Artistic"},
    {id:4, text:"I like teaching or mentoring others", axis:"Social"},
    {id:5, text:"I prefer structured office tasks", axis:"Conventional"},
    {id:6, text:"I like leading teams and organizing", axis:"Enterprising"},
  ];

  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [completed, setCompleted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  const answer = async (score) => {
    const newAnswers = [...answers, {q:questions[idx].id, axis:questions[idx].axis, score}];
    setAnswers(newAnswers);

    if(idx+1<questions.length) {
      setIdx(idx+1);
    } else {
      setLoading(true);
      try {
        // Submit assessment to backend for analysis
        const result = await ApiService.submitAssessment({
          answers: newAnswers,
          totalQuestions: questions.length
        });
        setAnalysisResult(result);
      } catch (error) {
        console.error('Assessment submission failed:', error);
        // Continue with local analysis as fallback
      } finally {
        setLoading(false);
        setCompleted(true);
      }
    }
  };

  const grouped = answers.reduce((acc,cur)=>{
    acc[cur.axis] = (acc[cur.axis]||0) + cur.score; return acc;
  }, {});

  return (
    <div style={{minHeight:"80vh", display:"flex", alignItems:"center", justifyContent:"center", padding:20}}>
      {!completed ? (
        <div style={card}>
          <h2 style={{color:"#0077b6"}}>Quick Skills Assessment</h2>
          <p style={{fontSize:18}}>{questions[idx].text}</p>
          <div style={{display:"flex", gap:12, justifyContent:"center", marginTop:12}}>
            <button style={btn} onClick={()=>answer(2)}>Agree</button>
            <button style={btnMuted} onClick={()=>answer(1)}>Neutral</button>
            <button style={btn} onClick={()=>answer(0)}>Disagree</button>
          </div>
          <div style={{marginTop:12, color:"var(--muted)"}}>
            Progress {idx+1}/{questions.length}
            {loading && " - Analyzing your responses..."}
          </div>
        </div>
      ) : (
        <div style={card}>
          <h2 style={{color:"#0077b6"}}>Assessment Results</h2>

          {loading ? (
            <div style={{padding: 20}}>
              <p>🤔 Analyzing your responses with AI...</p>
            </div>
          ) : (
            <>
              <p style={{color:"var(--muted)"}}>
                {analysisResult ? "AI-powered analysis complete!" : "Local analysis (AI unavailable)"}
              </p>

              {analysisResult && analysisResult.recommendations && (
                <div style={{marginTop: 16, padding: 16, background: "rgba(0,180,216,0.1)", borderRadius: 12}}>
                  <h3 style={{color:"#0077b6", marginBottom: 8}}>🎯 Career Recommendations</h3>
                  <ul style={{textAlign: "left", paddingLeft: 20}}>
                    {analysisResult.recommendations.map((rec, i) => (
                      <li key={i} style={{marginBottom: 4}}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div style={{display:"grid", gap:8, maxWidth:680, marginTop:16}}>
                {Object.entries(grouped).map(([axis, sc])=> (
                  <div key={axis} style={{display:"flex", alignItems:"center", gap:12}}>
                    <div style={{width:130}}>{axis}</div>
                    <div style={{flex:1, height:12, background:"rgba(0,0,0,0.06)", borderRadius:8}}>
                      <div style={{width: `${Math.min(100, Math.round((sc/ (2*questions.length))*200 ))}%`, height:12, background:"#00b4d8", borderRadius:8}}/>
                    </div>
                    <div style={{width:42, textAlign:"right"}}>{Math.min(100, Math.round((sc/ (2*questions.length))*100))}%</div>
                  </div>
                ))}
              </div>

              {analysisResult && analysisResult.score && (
                <div style={{marginTop: 16, fontSize: 18}}>
                  Overall Assessment Score: <strong>{analysisResult.score}/100</strong>
                </div>
              )}

              <div style={{marginTop:20}}>
                <button onClick={()=>{
                  setIdx(0);
                  setAnswers([]);
                  setCompleted(false);
                  setAnalysisResult(null);
                }} style={btn}>
                  Take Assessment Again
                </button>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

const card = { background:"var(--card)", padding:20, borderRadius:14, boxShadow:"0 10px 30px rgba(2,6,23,0.12)", width:"90%", maxWidth:760, textAlign:"center" };
const btn = { padding:"10px 16px", borderRadius:10, border:"none", background:"#00b4d8", color:"#fff", cursor:"pointer" };
const btnMuted = { ...btn, background:"transparent", border:"1px solid #d6dbe1", color:"var(--text)" };
