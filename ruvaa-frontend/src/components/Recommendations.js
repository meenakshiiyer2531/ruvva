import React, { useState } from "react";

function Recommendations() {
  const [search, setSearch] = useState("");

  const careers = [
    { name: "Engineer", icon: "👷‍♂️", description: "Work on building and designing things, from software to infrastructure." },
    { name: "Doctor", icon: "🩺", description: "Provide medical care, heal patients, and save lives." },
    { name: "Artist", icon: "🎨", description: "Express creativity through painting, music, or other forms of art." },
    { name: "Teacher", icon: "📚", description: "Educate and inspire students, shaping the future generation." },
    { name: "Entrepreneur", icon: "💼", description: "Start and manage your own business, innovating in different industries." },
    { name: "Scientist", icon: "🔬", description: "Explore, research, and innovate to understand the world better." }
  ];

  const filteredCareers = careers.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase()) ||
    c.description.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="recommendations-page">
      <h1 className="page-title">🌟 Career Recommendations</h1>

      <input
        type="text"
        placeholder="Search careers..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="search-input"
      />

      <div className="career-grid">
        {filteredCareers.length > 0 ? (
          filteredCareers.map((career, idx) => (
            <div key={idx} className="career-card">
              <h2>{career.icon} {career.name}</h2>
              <p>{career.description}</p>
            </div>
          ))
        ) : (
          <p className="no-results">❌ No careers found matching your search.</p>
        )}
      </div>

      {/* Embedded CSS */}
      <style>{`
        .recommendations-page {
          min-height: 100vh;
          padding: 40px 20px;
          background: linear-gradient(135deg, #f0f4ff, #ffffff);
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
          max-width: 700px;
          padding: 14px 16px;
          margin-bottom: 40px;
          border-radius: 12px;
          border: 2px solid #ccc;
          font-size: 1rem;
          transition: 0.3s;
        }

        .search-input:focus {
          outline: none;
          border-color: #0077b6;
          box-shadow: 0 0 10px rgba(0, 180, 216, 0.5);
        }

        .career-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 25px;
          width: 100%;
          max-width: 1200px;
        }

        .career-card {
          background: rgba(255, 255, 255, 0.95);
          padding: 25px;
          border-radius: 20px;
          box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
          transition: transform 0.3s, box-shadow 0.3s;
          text-align: center;
        }

        .career-card h2 {
          font-size: 1.5rem;
          margin-bottom: 12px;
          color: #0077b6;
        }

        .career-card p {
          font-size: 1rem;
          color: #555;
        }

        .career-card:hover {
          transform: translateY(-5px) scale(1.03);
          box-shadow: 0 12px 40px rgba(0,0,0,0.2);
        }

        .no-results {
          grid-column: span 3;
          text-align: center;
          font-size: 1.2rem;
          color: #777;
        }

        @media (max-width: 1024px) {
          .career-grid { grid-template-columns: repeat(2, 1fr); }
        }

        @media (max-width: 768px) {
          .career-grid { grid-template-columns: 1fr; }
          .search-input { max-width: 100%; }
        }
      `}</style>
    </div>
  );
}

export default Recommendations;
