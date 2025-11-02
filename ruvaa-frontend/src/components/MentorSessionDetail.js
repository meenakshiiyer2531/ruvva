import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import ApiService from '../services/api';

export default function MentorSessionDetail({ bookingId, autoJoin = true, darkMode }) {
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [platform, setPlatform] = useState('jitsi'); // 'jitsi' or 'google'
  const jitsiRoom = 'ruvaa-mentor-room';

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      if (!bookingId) { setLoading(false); return; }
      try {
        const resp = await ApiService.getBookingDetail(bookingId);
        const data = resp?.data || resp;
        if (!cancelled) setBooking(data);
      } catch (e) {
        if (!cancelled) setError(e.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    load();
    return () => { cancelled = true; };
  }, [bookingId]);

  const copyLink = () => {
    navigator.clipboard.writeText(FIXED_MEET_LINK).then(() => {
      document.dispatchEvent(new CustomEvent('toast', { detail:{ type:'success', message:'Meeting link copied'}}));
    }).catch(()=>{
      document.dispatchEvent(new CustomEvent('toast', { detail:{ type:'error', message:'Copy failed'}}));
    });
  };

  const upcoming = booking ? (new Date(booking.date) >= new Date()) : false;
  // Fixed Google Meet link override
  const FIXED_MEET_LINK = 'https://meet.google.com/eje-rdfq-ksk';

  // Auto-open fixed meeting link when session is upcoming.
  useEffect(()=> {
    if (autoJoin && booking && upcoming && platform === 'google') {
      window.open(FIXED_MEET_LINK, '_blank');
    }
  }, [autoJoin, booking, upcoming, platform]);

  if (loading) return <div style={wrap(darkMode)}>Loading session...</div>;
  if (error) return <div style={wrap(darkMode)}>Error: {error}</div>;
  if (!booking) return <div style={wrap(darkMode)}>No booking found.</div>;

  return (
    <div style={wrap(darkMode)}>
      <h2 style={{color:'#0077b6', marginTop:0}}>Mentor Session</h2>
      <div style={card(darkMode)}> 
        <h3 style={{margin:'0 0 8px'}}>{booking.mentorName}</h3>
        {booking.mentorExpertise && Array.isArray(booking.mentorExpertise) && (
          <div style={{display:'flex', flexWrap:'wrap', gap:6, marginBottom:10}}>
            {booking.mentorExpertise.map(ex => <span key={ex} style={chip}>{ex}</span>)}
          </div>
        )}
        <p style={{fontSize:13, lineHeight:1.4}}>{booking.mentorBio}</p>
        {booking.mentorLinkedin && (
          <p style={{marginTop:8}}>
            <a href={booking.mentorLinkedin} target="_blank" rel="noreferrer" style={{color:'#0077b6'}}>View LinkedIn ↗</a>
          </p>
        )}
        <div style={{marginTop:14, fontSize:14}}><strong>Session Date:</strong> {new Date(booking.date).toLocaleString()}</div>
        <div style={{marginTop:6, fontSize:14}}><strong>Status:</strong> {booking.status}</div>
        <div style={{marginTop:6, fontSize:12, color:'#64748b'}}>Booked {new Date(booking.createdAt).toLocaleString()}</div>
        <div style={{marginTop:16, display:'flex', gap:8, flexWrap:'wrap'}}>
          <div style={{display:'flex', gap:8}}>
            <select value={platform} onChange={e=> setPlatform(e.target.value)} style={selectStyle}>
              <option value="jitsi">Embedded (Jitsi)</option>
              <option value="google">Google Meet Link</option>
            </select>
            {platform === 'google' && (
              <>
                <a href={FIXED_MEET_LINK} target="_blank" rel="noreferrer" style={btnPrimary}>Open Meet</a>
                <button onClick={copyLink} style={btnSecondary}>Copy Link</button>
              </>
            )}
          </div>
        </div>
        {platform === 'jitsi' && (
          <div style={{marginTop:20}}>
            <iframe
              title="Mentor Session (Jitsi)"
              src={`https://meet.jit.si/${encodeURIComponent(jitsiRoom)}`}
              style={{width:'100%', minHeight:420, border:'1px solid #334155', borderRadius:12, background:'#000'}}
              allow="camera; microphone; display-capture"
            />
            <div style={{marginTop:8, fontSize:12, color:darkMode? '#94a3b8':'#64748b'}}>
              Jitsi room is generated client-side. Share this room name with your mentor: <code style={{background:'rgba(0,0,0,0.1)', padding:'2px 4px', borderRadius:4}}>{jitsiRoom}</code>
            </div>
          </div>
        )}
        {platform === 'google' && (
          <div style={{marginTop:20, fontSize:12, color:darkMode? '#94a3b8':'#64748b'}}>
            Google Meet cannot be embedded reliably; opened in a new tab instead.
          </div>
        )}
        {/* Meeting link always available via FIXED_MEET_LINK */}
        <div style={{marginTop:24}}>
          <button onClick={()=> {
            document.dispatchEvent(new CustomEvent('navigate',{ detail:{ page:'profile' }}));
          }} style={btnGhost}>Back to Profile</button>
          {upcoming && <span style={{marginLeft:12, fontSize:12, color:'#059669'}}>Upcoming session ready</span>}
        </div>
      </div>
    </div>
  );
}

const wrap = (dark) => ({ minHeight:'70vh', padding:20, maxWidth:760, margin:'0 auto', color: dark ? 'var(--text)' : '#0f172a' });
const card = (dark) => ({ background: dark ? 'var(--card)' : '#f8fafc', padding:20, borderRadius:16, border: dark ? '1px solid var(--border)' : '1px solid #e2e8f0', boxShadow: dark ? '0 4px 16px rgba(0,0,0,0.5)' : '0 4px 16px rgba(0,0,0,0.06)' });
const chip = { background:'#e0f2fe', color:'#0369a1', padding:'4px 8px', borderRadius:20, fontSize:11, fontWeight:600 };
const btnPrimary = { padding:'10px 16px', background:'#00b4d8', color:'#fff', borderRadius:10, textDecoration:'none', fontSize:14 };
const btnSecondary = { padding:'10px 16px', background:'#fff', color:'#0077b6', borderRadius:10, border:'1px solid #0077b6', cursor:'pointer', fontSize:14 };
const btnGhost = { padding:'8px 14px', background:'transparent', color:'#0077b6', border:'1px solid #0077b6', borderRadius:8, cursor:'pointer', fontSize:13 };
const selectStyle = { padding:'8px 10px', borderRadius:8, border:'1px solid #94a3b8', background:'var(--card)', color:'var(--text)', fontSize:13 };

MentorSessionDetail.propTypes = {
  bookingId: PropTypes.string,
  autoJoin: PropTypes.bool,
  darkMode: PropTypes.bool
};