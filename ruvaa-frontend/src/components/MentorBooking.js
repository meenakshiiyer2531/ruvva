import React, { useState, useMemo, useEffect } from "react";
import ApiService from "../services/api";

/*
  Mentor Booking Component
  - Shows mentors
  - Computes simple compatibility percent based on profile interests
  - Allows booking sessions
  - Profile redirects to LinkedIn
*/

const fallbackMentors = [
  { id:"m1", name:"Dr. Meenakshi", expertise:["AI","Research","Python"], bio:"PhD researcher in AI", linkedin:"https://www.linkedin.com/in/dr-meenakshi", availability:["2025-09-22","2025-09-28"] },
  { id:"m2", name:"Mr. Sharma", expertise:["Problem solving","Algorithms","DSA"], bio:"Senior Engineer", linkedin:"https://www.linkedin.com/in/mr-sharma", availability:["2025-09-25","2025-10-03"] },
  { id:"m3", name:"Ms. Kapoor", expertise:["Design","Product","UX"], bio:"Product Designer", linkedin:"https://www.linkedin.com/in/ms-kapoor", availability:["2025-09-23","2025-10-02"] },
  { id:"m4", name:"Dr. Rao", expertise:["Machine Learning","Python","Data Science"], bio:"AI Scientist", linkedin:"https://www.linkedin.com/in/dr-rao", availability:["2025-09-24","2025-10-05"] },
  { id:"m5", name:"Ms. Iyer", expertise:["Web Development","React","UI/UX"], bio:"Frontend Developer", linkedin:"https://www.linkedin.com/in/ms-iyer", availability:["2025-09-22","2025-09-30"] },
  { id:"m6", name:"Mr. Verma", expertise:["Blockchain","Solidity","Smart Contracts"], bio:"Blockchain Developer", linkedin:"https://www.linkedin.com/in/mr-verma", availability:["2025-09-26","2025-10-04"] },
  { id:"m7", name:"Dr. Nair", expertise:["Robotics","AI","Automation"], bio:"Robotics Researcher", linkedin:"https://www.linkedin.com/in/dr-nair", availability:["2025-09-23","2025-09-29"] },
  { id:"m8", name:"Ms. Singh", expertise:["Marketing","Strategy","Business"], bio:"Business Consultant", linkedin:"https://www.linkedin.com/in/ms-singh", availability:["2025-09-25","2025-10-01"] },
  { id:"m9", name:"Mr. Das", expertise:["Cybersecurity","Networking","Python"], bio:"Security Analyst", linkedin:"https://www.linkedin.com/in/mr-das", availability:["2025-09-24","2025-10-03"] },
  { id:"m10", name:"Ms. Rao", expertise:["AI","Data Science","Machine Learning"], bio:"Data Scientist", linkedin:"https://www.linkedin.com/in/ms-rao", availability:["2025-09-22","2025-09-28"] },
];

export default function MentorBooking({ profile }) {
  const [selected, setSelected] = useState("");
  const [studentName, setStudentName] = useState(profile?.name || "");
  const [date, setDate] = useState("");
  const [bookings, setBookings] = useState([]);
  const [mentors, setMentors] = useState(fallbackMentors);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch mentors from backend
  useEffect(() => {
    const fetchMentors = async () => {
      console.log("🔍 Fetching mentors from backend...");
      setLoading(true);
      setError(null);

      try {
        const data = await ApiService.getMentors();
        console.log("✅ Mentors data received:", data);

        if (Array.isArray(data)) {
          setMentors(data);
        } else if (data.mentors && Array.isArray(data.mentors)) {
          setMentors(data.mentors);
        } else {
          console.warn("⚠️ Unexpected backend response format, using fallback data");
          setMentors(fallbackMentors);
        }
      } catch (err) {
        console.error("❌ Failed to fetch mentors from backend:", err.message);
        console.log("⚠️ Using local fallback mentor data");
        // Don't show error to user since fallback data works fine
        setMentors(fallbackMentors);
      } finally {
        setLoading(false);
      }
    };

    fetchMentors();
  }, []);

  const ranked = useMemo(()=> {
    const interests = (profile?.interests || []).map(i=>i.toLowerCase());
    return mentors.map(m=>{
      const match = m.expertise.reduce((acc,ex)=>{
        if(interests.some(it=> ex.toLowerCase().includes(it.split(" ")[0]))) return acc+1;
        return acc;
      },0);
      const percent = Math.min(100, Math.round((match / Math.max(1, m.expertise.length)) * 100));
      return {...m, percent};
    }).sort((a,b)=>b.percent - a.percent);
  }, [profile, mentors]);

  const book = async () => {
    if(!selected || !studentName || !date) return alert("Fill student name, mentor, and date");

    const selectedMentor = mentors.find(m => m.name === selected);
    const bookingData = {
      studentName,
      mentorId: selectedMentor?.id,
      mentorName: selected,
      date
    };

    console.log("📤 Booking mentor session:", bookingData);

    try {
      const result = await ApiService.bookMentorSession(bookingData);
      console.log("✅ Booking successful:", result);
      setBookings(b=>[...b, {student:studentName, mentor:selected, date}]);
      setStudentName(""); setDate(""); setSelected("");
      alert("Session booked successfully!");
    } catch (err) {
      console.error("❌ Booking failed:", err.message);
      // Still save locally as fallback
      setBookings(b=>[...b, {student:studentName, mentor:selected, date}]);
      setStudentName(""); setDate(""); setSelected("");
      alert("Booking saved locally. Backend connection failed.");
    }
  };

  return (
    <div style={{minHeight:"80vh", padding:20}}>
      <h2 style={{color:"#0077b6", marginBottom:20}}>Mentor Matching</h2>

      {loading && (
        <div style={{ textAlign: "center", padding: 20, color: "var(--muted)" }}>
          Loading mentors...
        </div>
      )}
      <div style={{display:"grid", gridTemplateColumns:"1fr 360px", gap:20, alignItems:"start"}}>
        <div>
          {ranked.map(m=>(
            <div key={m.id} style={{background:"var(--card)", padding:16, borderRadius:12, marginBottom:16, boxShadow:"0 2px 10px rgba(0,0,0,0.08)"}}>
              <div style={{display:"flex", justifyContent:"space-between", alignItems:"center"}}>
                <div>
                  <strong style={{fontSize:18}}>{m.name}</strong>
                  <div style={{color:"var(--muted)", fontSize:14, marginTop:4}}>{m.bio}</div>
                </div>
                <div style={{textAlign:"right"}}>
                  <div style={{width:120, height:8, background:"rgba(0,0,0,0.06)", borderRadius:8}}>
                    <div style={{width:`${m.percent}%`, height:8, background:"#00b4d8", borderRadius:8}}/>
                  </div>
                  <div style={{fontSize:12, color:"var(--muted)"}}>{m.percent}%</div>
                </div>
              </div>
              <div style={{marginTop:12, display:"flex", gap:10}}>
                <button onClick={()=>setSelected(m.name)} style={{padding:8, borderRadius:8, border:"none", background: selected===m.name ? "#0077b6" : "#00b4d8", color:"#fff", cursor:"pointer"}}>
                  Select
                </button>
                <button onClick={()=>window.open(m.linkedin, "_blank")} style={{padding:8, borderRadius:8, border:"1px solid #00b4d8", background:"#fff", color:"#0077b6", cursor:"pointer"}}>
                  Profile
                </button>
              </div>
            </div>
          ))}
        </div>

        <div style={{background:"var(--card)", padding:16, borderRadius:12, boxShadow:"0 2px 10px rgba(0,0,0,0.08)"}}>
          <h4 style={{marginBottom:12}}>Book Session</h4>
          <input placeholder="Student name" value={studentName} onChange={e=>setStudentName(e.target.value)} style={field}/>
          <input type="date" value={date} onChange={e=>setDate(e.target.value)} style={field}/>
          <div style={{marginBottom:12}}>Selected Mentor: <b>{selected || "—"}</b></div>
          <button onClick={book} style={{...btn, width:"100%"}}>Book</button>

          <div style={{marginTop:16}}>
            <h5 style={{margin:"8px 0"}}>Your bookings</h5>
            {bookings.length ? bookings.map((b,i)=>(
              <div key={i} style={{background:"rgba(0,0,0,0.03)", padding:10, borderRadius:8, marginBottom:8}}>
                <div><b>{b.mentor}</b> — {b.date}</div>
                <div style={{fontSize:13, color:"var(--muted)"}}>Student: {b.student}</div>
              </div>
            )) : <div style={{color:"var(--muted)"}}>No bookings</div>}
          </div>
        </div>
      </div>
    </div>
  );
}

const field = { padding:10, borderRadius:8, border:"1px solid #d6dbe1", width:"100%", marginBottom:10 };
const btn = { padding:10, borderRadius:8, border:"none", background:"#00b4d8", color:"#fff", cursor:"pointer" };
