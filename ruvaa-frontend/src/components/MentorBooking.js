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

export default function MentorBooking({ profile, studentId }) {
  const [selected, setSelected] = useState("");
  const [studentName, setStudentName] = useState(profile?.name || "");
  const [date, setDate] = useState("");
  const [bookings, setBookings] = useState([]);
  // notifications removed
  const [mentors, setMentors] = useState(fallbackMentors);
  const [loading, setLoading] = useState(true);
  const [bookingBusy, setBookingBusy] = useState(false);

  // Initial load: mentors + existing bookings
  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      try {
        const mentorsResp = await ApiService.getMentors();
        const mentorsArray = Array.isArray(mentorsResp?.data) ? mentorsResp.data : Array.isArray(mentorsResp) ? mentorsResp : mentorsResp?.mentors || fallbackMentors;
        if (!cancelled) setMentors(mentorsArray);
        if (studentId) {
          try {
            const bookingsResp = await ApiService.listStudentBookings(studentId);
            const bookingsArray = Array.isArray(bookingsResp?.data) ? bookingsResp.data : Array.isArray(bookingsResp) ? bookingsResp : [];
            if (!cancelled) setBookings(bookingsArray);
          } catch (e) { console.warn("⚠️ Unable to load student bookings:", e.message); }
          // notifications removed
        }
      } catch (err) {
        console.error("❌ Mentor initial load failed:", err.message);
        if (!cancelled) setMentors(fallbackMentors);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    load();
    return () => { cancelled = true; };
  }, [studentId]);

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
    if(!selected || !studentName || !date) {
      window.dispatchEvent(new CustomEvent('toast', { detail: { type:'error', message:'Fill student name, mentor, and date' } }));
      return;
    }
    const selectedMentor = mentors.find(m => m.name === selected);
    if (!selectedMentor) {
      window.dispatchEvent(new CustomEvent('toast', { detail: { type:'error', message:'Mentor not found in list' } }));
      return;
    }
    setBookingBusy(true);
    const bookingPayload = { date, studentId: studentId || null, studentEmail: profile?.email || null };
    try {
      const result = await ApiService.createMentorBooking(selectedMentor.id, bookingPayload);
      const added = result?.data || result;
      setBookings(b => [...b, added]);
  window.dispatchEvent(new CustomEvent('toast', { detail: { type:'success', message:`Booked ${selectedMentor.name} on ${date}` } }));
  // Auto navigate to booking detail page, include booking object for local fallback
  window.dispatchEvent(new CustomEvent('navigate', { detail: { page:'bookingDetail', bookingId: added.id, booking: added }}));
      setDate(""); setSelected("");
    } catch (err) {
      console.error("❌ Booking failed:", err.message);
  window.dispatchEvent(new CustomEvent('toast', { detail: { type:'error', message: err.message.includes('Slot already') ? 'Slot already booked' : 'Booking failed; cached locally.' } }));
      // local optimistic fallback
  const localBooking = { id: 'local-'+Date.now(), mentorId: selectedMentor.id, mentorName: selectedMentor.name, date, status:'PENDING', createdAt: new Date().toISOString() };
  setBookings(b => [...b, localBooking]);
  // Navigate immediately to show detail with fallback booking data
  window.dispatchEvent(new CustomEvent('navigate', { detail: { page:'bookingDetail', bookingId: localBooking.id, booking: localBooking }}));
    } finally {
      setBookingBusy(false);
    }
  };

  // dispatch navigate event
  const onBookingClick = (booking) => {
    // Use window to align with global listener in App.js
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('navigate', { detail: { page: 'bookingDetail', bookingId: booking.id, booking } }));
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
          {selected && (
            <div style={{marginBottom:10}}>
              <label style={{fontSize:12, color:'var(--muted)'}}>Available Dates for {selected}</label>
              <div style={{display:'flex', flexWrap:'wrap', gap:6, marginTop:6}}>
                {(mentors.find(m=>m.name===selected)?.availability || []).map(d => {
                  const taken = bookings.some(b => b.mentorName === selected && b.date === d && b.status !== 'CANCELLED');
                  return (
                    <button key={d} disabled={taken} onClick={()=>setDate(d)} style={{padding:'6px 10px', borderRadius:6, border:'1px solid #00b4d8', background: date===d ? '#0077b6' : taken ? '#eee' : '#fff', color: date===d ? '#fff' : taken ? '#777' : '#0077b6', cursor: taken ? 'not-allowed':'pointer', fontSize:12}}>
                      {d}{taken ? ' ⛔':''}
                    </button>
                  );
                })}
              </div>
            </div>
          )}
          {!selected && <input type="date" value={date} onChange={e=>setDate(e.target.value)} style={field}/>}
          <div style={{marginBottom:12}}>Selected Mentor: <b>{selected || "—"}</b></div>
          <button onClick={book} disabled={bookingBusy} style={{...btn, width:"100%", opacity: bookingBusy?0.7:1}}>{bookingBusy? 'Booking...' : 'Book'}</button>

          <div style={{marginTop:16}}>
            <h5 style={{margin:"8px 0"}}>Your bookings</h5>
            {bookings.length ? bookings.map((b)=> {
              // Force fixed Google Meet link override
              const fixedLink = 'https://meet.google.com/eje-rdfq-ksk';
              if (!b.meetingLink) b.meetingLink = fixedLink; // non-persistent UI override
              const hasLink = true;
              return (
                <button onClick={()=>onBookingClick(b)} key={b.id || b.date+ b.mentorId} style={{textAlign:'left', width:'100%', background:"rgba(0,0,0,0.03)", padding:10, borderRadius:8, marginBottom:8, border:'1px solid #d6dbe1', cursor:'pointer'}}>
                  <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
                    <div><b>{b.mentorName || b.mentor}</b> — {b.date}</div>
                    {hasLink && (
                      <span style={{ fontSize:11, background:'#0077b6', color:'#fff', padding:'2px 6px', borderRadius:6 }}>
                        Meet Link
                      </span>
                    )}
                  </div>
                  <div style={{fontSize:12, color:"var(--muted)"}}>Status: {b.status || 'PENDING'}</div>
                </button>
              );
            }) : <div style={{color:"var(--muted)"}}>No bookings</div>}
          </div>
        </div>
      </div>
    </div>
  );
}

const field = { padding:10, borderRadius:8, border:"1px solid #d6dbe1", width:"100%", marginBottom:10 };
const btn = { padding:10, borderRadius:8, border:"none", background:"#00b4d8", color:"#fff", cursor:"pointer", fontWeight:600 };
