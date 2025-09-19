import React, { useState } from "react";

function CollegeFinder() {
  const [search, setSearch] = useState("");

  const colleges = [
    { name: "Govt College Srinagar", program: "BSc, BA", location: "Srinagar" },
    { name: "Govt College Jammu", program: "BCom, BCA", location: "Jammu" },
    { name: "Cluster University Srinagar", program: "BSc, BBA, BA", location: "Srinagar" },
    { name: "GC Women College Jammu", program: "BA, BCom", location: "Jammu" },
  ];

  const filteredColleges = colleges.filter(
    (c) =>
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.program.toLowerCase().includes(search.toLowerCase()) ||
      c.location.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="college-page">
      <h1 className="page-title">🏫 Find Colleges in J&K</h1>

      <input
        type="text"
        placeholder="Search by college name, program, or location..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="search-input"
      />

      <div className="college-grid">
        {filteredColleges.length > 0 ? (
          filteredColleges.map((college, idx) => (
            <div key={idx} className="college-card">
              <h2>{college.name}</h2>
              <p><strong>Programs:</strong> {college.program}</p>
              <p><strong>Location:</strong> {college.location}</p>
            </div>
          ))
        ) : (
          <p className="no-results">❌ No colleges found matching your search.</p>
        )}
      </div>

      {/* Embedded CSS */}
      <style>{`
        .college-page {
          min-height: 100vh;
          padding: 40px 20px;
          background: linear-gradient(135deg, #e0f7fa, #ffffff);
          font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
          display: flex;
          flex-direction: column;
          align-items: center;
        }

        .page-title {
          font-size: 2.5rem;
          text-align: center;
          margin-bottom: 30px;
          color: #222;
        }

        .search-input {
          width: 100%;
          max-width: 600px;
          padding: 14px 16px;
          margin-bottom: 40px;
          border-radius: 12px;
          border: 2px solid #ccc;
          font-size: 1rem;
          transition: 0.3s;
        }

        .search-input:focus {
          outline: none;
          border-color: #00b4d8;
          box-shadow: 0 0 10px rgba(0, 180, 216, 0.5);
        }

        .college-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 20px;
          width: 100%;
          max-width: 1000px;
        }

        .college-card {
          background: rgba(255, 255, 255, 0.9);
          padding: 20px;
          border-radius: 20px;
          box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
          transition: transform 0.3s, box-shadow 0.3s;
        }

        .college-card h2 {
          font-size: 1.5rem;
          margin-bottom: 10px;
          color: #0077b6;
        }

        .college-card p {
          font-size: 1rem;
          margin-bottom: 6px;
          color: #555;
        }

        .college-card:hover {
          transform: scale(1.05);
          box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
        }

        .no-results {
          grid-column: span 2;
          text-align: center;
          color: #777;
          font-size: 1.2rem;
        }

        @media (max-width: 768px) {
          .college-grid {
            grid-template-columns: 1fr;
          }
          .search-input {
            max-width: 100%;
          }
        }
      `}</style>
    </div>
  );
}

export default CollegeFinder;
