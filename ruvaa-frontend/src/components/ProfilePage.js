import React, { useEffect, useState, useCallback } from 'react';
import apiService from '../services/api';

// ProfilePage component: allows viewing & editing of a single student's profile plus listing all profiles (mock mode)
// Assumes studentId stored after registration in localStorage under 'studentId'

const ProfilePage = () => {
  const [studentId, setStudentId] = useState(localStorage.getItem('studentId') || '');
  const [profile, setProfile] = useState({});
  const extendedFields = [
    'city','state','educationLevel','institutionName','stream','phoneNumber','age',
    'goal','interest','skillLevel','focus','path'
  ];
  const [allProfiles, setAllProfiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');

  const fetchProfile = useCallback(async () => {
    if (!studentId) return;
    try {
      setLoading(true);
      const result = await apiService.getStudentProfile(studentId);
      setProfile(result?.data?.profile || {});
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [studentId]);

  const fetchAllProfiles = useCallback(async () => {
    try {
      const result = await apiService.listStudentProfiles();
      setAllProfiles(result?.data || []);
    } catch (e) {
      console.error('Failed to list profiles', e);
    }
  }, []);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  useEffect(() => {
    fetchAllProfiles();
  }, [fetchAllProfiles]);

  const handleFieldChange = (key, value) => {
    setProfile(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    if (!studentId) {
      setError('No studentId found. Please register first.');
      return;
    }
    try {
      setLoading(true);
      const result = await apiService.patchStudentProfile(studentId, profile);
      setProfile(result?.data?.profile || {});
      setSuccessMessage('Profile saved');
      fetchAllProfiles();
      setTimeout(() => setSuccessMessage(''), 2500);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReplace = async () => {
    try {
      setLoading(true);
      const result = await apiService.replaceStudentProfile(studentId, profile);
      setProfile(result?.data?.profile || {});
      setSuccessMessage('Profile replaced');
      fetchAllProfiles();
      setTimeout(() => setSuccessMessage(''), 2500);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    try {
      setLoading(true);
      await apiService.deleteStudentProfile(studentId);
      setProfile({});
      setSuccessMessage('Profile deleted');
      fetchAllProfiles();
      setTimeout(() => setSuccessMessage(''), 2500);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateIfMissing = async () => {
    try {
      setLoading(true);
      const result = await apiService.createStudentProfile(studentId, profile);
      setProfile(result?.data?.profile || {});
      setSuccessMessage('Profile created');
      fetchAllProfiles();
      setTimeout(() => setSuccessMessage(''), 2500);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '1.5rem' }}>
      <h2>Student Profile</h2>
      {!studentId && <p style={{ color: 'orange' }}>Register a student to begin editing profile.</p>}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {successMessage && <div style={{ color: 'green' }}>{successMessage}</div>}
      {loading && <div>Loading...</div>}

      <fieldset style={{ border: '1px solid #ddd', padding: '1rem', borderRadius: '6px', maxWidth: '520px', marginTop: '1rem' }}>
        <legend style={{ padding: '0 0.5rem', fontWeight: 600 }}>Profile Details</legend>
        <div style={{ display: 'grid', gap: '0.75rem', gridTemplateColumns: 'repeat(auto-fit, minmax(220px,1fr))' }}>
          {extendedFields.map(field => (
            <div key={field} style={{ display: 'flex', flexDirection: 'column' }}>
              <label style={{ fontWeight: 600, textTransform: 'capitalize' }}>{field}</label>
              <input
                type={field === 'age' ? 'number' : 'text'}
                value={profile[field] ?? ''}
                onChange={e => handleFieldChange(field, field === 'age' ? Number(e.target.value) : e.target.value)}
                placeholder={`Enter ${field}`}
              />
            </div>
          ))}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input
              type="checkbox"
              checked={!!profile.agreeToTerms}
              onChange={e => handleFieldChange('agreeToTerms', e.target.checked)}
            />
            <label>Agreed to Terms</label>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input
              type="checkbox"
              checked={!!profile.agreeToPrivacyPolicy}
              onChange={e => handleFieldChange('agreeToPrivacyPolicy', e.target.checked)}
            />
            <label>Agreed to Privacy Policy</label>
          </div>
        </div>
      </fieldset>

      <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <button onClick={handleSave} disabled={!studentId}>Patch Save</button>
        <button onClick={handleReplace} disabled={!studentId}>Replace</button>
        <button onClick={handleCreateIfMissing} disabled={!studentId}>Create (if none)</button>
        <button onClick={handleDelete} disabled={!studentId}>Delete</button>
        <button onClick={fetchProfile} disabled={!studentId}>Refresh</button>
      </div>

      <hr style={{ margin: '2rem 0' }} />
      <h3>All Profiles (Mock Mode)</h3>
      <table style={{ borderCollapse: 'collapse', width: '100%', maxWidth: '960px' }}>
        <thead>
          <tr>
            <th style={{ borderBottom: '1px solid #ccc', textAlign: 'left' }}>Student ID</th>
            <th style={{ borderBottom: '1px solid #ccc', textAlign: 'left' }}>Email</th>
            <th style={{ borderBottom: '1px solid #ccc', textAlign: 'left' }}>Profile</th>
          </tr>
        </thead>
        <tbody>
          {allProfiles.map(p => (
            <tr key={p.id} style={{ cursor: 'pointer' }} onClick={() => setStudentId(p.id)}>
              <td style={{ padding: '0.4rem 0' }}>{p.id}</td>
              <td>{p.email}</td>
              <td>
                <code style={{ fontSize: '0.85rem' }}>{JSON.stringify(p.profile)}</code>
              </td>
            </tr>
          ))}
          {allProfiles.length === 0 && (
            <tr><td colSpan={3} style={{ padding: '0.75rem', color: '#666' }}>No profiles yet.</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default ProfilePage;
