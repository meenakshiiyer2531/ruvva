import React, { useState } from "react";

function Profile({ user }) {
  const [editMode, setEditMode] = useState(false);
  const [profile, setProfile] = useState({
    name: user?.name || "",
    email: user ? `${user.name}@ruvaa.com` : "",
    membership: "Student",
  });

  if (!user) return <h3 style={{ textAlign: "center", marginTop: "50px" }}>Please login first.</h3>;

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const toggleEdit = () => setEditMode(!editMode);

  return (
    <div className="profile-page">
      <div className="profile-card">
        <div className="profile-header">
          <div className="avatar">{profile.name[0].toUpperCase()}</div>
          {editMode ? (
            <input
              name="name"
              value={profile.name}
              onChange={handleChange}
              className="edit-input"
            />
          ) : (
            <h2>{profile.name}</h2>
          )}
          <p>{profile.membership} Member</p>
        </div>

        <div className="profile-details">
          <div className="detail">
            <span>Username:</span>
            {editMode ? (
              <input
                name="name"
                value={profile.name}
                onChange={handleChange}
                className="edit-input"
              />
            ) : (
              <span>{profile.name}</span>
            )}
          </div>
          <div className="detail">
            <span>Email:</span>
            {editMode ? (
              <input
                name="email"
                value={profile.email}
                onChange={handleChange}
                className="edit-input"
              />
            ) : (
              <span>{profile.email}</span>
            )}
          </div>
          <div className="detail">
            <span>Membership:</span>
            <span>{profile.membership}</span>
          </div>
        </div>

        <button onClick={toggleEdit}>{editMode ? "Save Profile" : "Edit Profile"}</button>
      </div>

      <style>{`
        .profile-page {
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          width: 100%;
          background: linear-gradient(135deg, #e0f7fa, #ffffff);
          font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        }

        .profile-card {
          background: #ffffff;
          padding: 50px 40px;
          border-radius: 25px;
          box-shadow: 0 15px 50px rgba(0,0,0,0.2);
          max-width: 500px;
          width: 90%;
          text-align: center;
          transition: 0.3s;
        }

        .profile-card:hover {
          transform: translateY(-5px) scale(1.02);
          box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        .profile-header .avatar {
          width: 100px;
          height: 100px;
          border-radius: 50%;
          background: #00b4d8;
          color: white;
          font-size: 3rem;
          display: flex;
          align-items: center;
          justify-content: center;
          margin: 0 auto 15px;
          box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }

        h2 {
          margin-bottom: 8px;
          color: #0077b6;
        }

        p {
          color: #555;
          margin-bottom: 25px;
        }

        .profile-details {
          text-align: left;
          margin-bottom: 20px;
        }

        .detail {
          display: flex;
          justify-content: space-between;
          padding: 12px 0;
          border-bottom: 1px solid #eee;
          font-size: 1rem;
        }

        .edit-input {
          width: 60%;
          padding: 6px 10px;
          border-radius: 10px;
          border: 1px solid #ddd;
        }

        button {
          background: #00b4d8;
          color: white;
          padding: 12px 30px;
          border: none;
          border-radius: 20px;
          cursor: pointer;
          font-weight: bold;
          font-size: 1rem;
          transition: 0.3s;
        }

        button:hover {
          background: #0077b6;
          transform: translateY(-2px) scale(1.05);
          box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        @media(max-width:768px){
          .profile-card { padding: 35px 25px; }
          .profile-header .avatar { width: 80px; height: 80px; font-size: 2.2rem; }
          button { padding: 10px 25px; font-size: 0.95rem; }
        }
      `}</style>
    </div>
  );
}

export default Profile;
