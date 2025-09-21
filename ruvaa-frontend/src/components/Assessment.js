import React, { useState } from "react";

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

  const answer = (score) => {
    setAnswers(a=>[...a, {q:questions[idx].id, axis:questions[idx].axis, score}]);
    if(idx+1<questions.length) setIdx(idx+1);
    else setCompleted(true);
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
          <div style={{marginTop:12, color:"var(--muted)"}}>Progress {idx+1}/{questions.length}</div>
        </div>
      ) : (
        <div style={card}>
          <h2 style={{color:"#0077b6"}}>Assessment Results</h2>
          <p style={{color:"var(--muted)"}}>Here is a quick breakdown (mock scores)</p>
          <div style={{display:"grid", gap:8, maxWidth:680, marginTop:12}}>
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
          <div style={{marginTop:14}}>
            <button onClick={()=>{ setIdx(0); setAnswers([]); setCompleted(false); }} style={btn}>Restart</button>
          </div>
        </div>
      )}
    </div>
  );
}

const card = { background:"var(--card)", padding:20, borderRadius:14, boxShadow:"0 10px 30px rgba(2,6,23,0.12)", width:"90%", maxWidth:760, textAlign:"center" };
const btn = { padding:"10px 16px", borderRadius:10, border:"none", background:"#00b4d8", color:"#fff", cursor:"pointer" };
const btnMuted = { ...btn, background:"transparent", border:"1px solid #d6dbe1", color:"var(--text)" };
