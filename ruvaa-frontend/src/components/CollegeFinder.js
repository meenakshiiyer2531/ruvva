import React, { useState, useEffect } from "react";
import { FaMapMarkerAlt, FaBook, FaMoon, FaSun } from "react-icons/fa";
import ApiService from "../services/api";

export default function CollegeFinder({ darkMode }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fallbackColleges = [
    { name: "IIT Bombay", location: "India", courses: ["Engineering", "Management"], url: "https://www.iitb.ac.in" },
    { name: "MIT", location: "USA", courses: ["CS", "Data Science"], url: "https://web.mit.edu" },
    { name: "ETH Zurich", location: "Switzerland", courses: ["Engineering", "AI"], url: "https://ethz.ch" },
    { name: "Oxford University", location: "UK", courses: ["CS", "Research"], url: "https://www.ox.ac.uk" },
    { name: "Stanford University", location: "USA", courses: ["Engineering", "Humanities"], url: "https://www.stanford.edu" },
    { name: "University of Delhi", location: "India", courses: ["Arts", "Commerce", "Science"], url: "https://www.du.ac.in" },
    { name: "University of Cambridge", location: "UK", courses: ["Mathematics", "Physics", "Chemistry"], url: "https://www.cam.ac.uk" },
    { name: "Harvard University", location: "USA", courses: ["Law", "Medicine", "Business"], url: "https://www.harvard.edu" },
    { name: "Indian Institute of Science (IISc)", location: "India", courses: ["Science", "Research"], url: "https://www.iisc.ac.in" },
    { name: "Jawaharlal Nehru University (JNU)", location: "India", courses: ["Arts", "Languages"], url: "https://www.jnu.ac.in" },
    { name: "University of Toronto", location: "Canada", courses: ["Engineering", "Medicine"], url: "https://www.utoronto.ca" },
    { name: "University of Melbourne", location: "Australia", courses: ["Arts", "Business", "Law"], url: "https://www.unimelb.edu.au" },
    { name: "National University of Singapore (NUS)", location: "Singapore", courses: ["CS", "Engineering"], url: "https://www.nus.edu.sg" },
    { name: "Delhi Technological University (DTU)", location: "India", courses: ["Engineering"], url: "https://dtu.ac.in" },
    { name: "Indian Institute of Technology Madras (IITM)", location: "India", courses: ["Engineering", "Humanities"], url: "https://www.iitm.ac.in" },
    { name: "Indian Institute of Technology Delhi (IITD)", location: "India", courses: ["Engineering", "Technology"], url: "https://home.iitd.ac.in" },
    { name: "Vellore Institute of Technology (VIT)", location: "India", courses: ["Engineering", "Management"], url: "https://vit.ac.in" },
    { name: "BITS Pilani", location: "India", courses: ["Engineering", "Science", "Pharmacy"], url: "https://www.bits-pilani.ac.in" },
    { name: "SRM Institute of Science and Technology", location: "India", courses: ["Engineering", "Medicine"], url: "https://www.srmist.edu.in" },
    { name: "Amity University", location: "India", courses: ["Arts", "Science", "Commerce"], url: "https://www.amity.edu" },
    { name: "Anna University", location: "India", courses: ["Engineering", "Technology"], url: "https://www.annauniv.edu" },
    { name: "Manipal Academy of Higher Education", location: "India", courses: ["Medicine", "Engineering"], url: "https://manipal.edu" },
    { name: "Christ University", location: "India", courses: ["Arts", "Science", "Business"], url: "https://christuniversity.in" },
    { name: "Jamia Millia Islamia", location: "India", courses: ["Arts", "Law", "Engineering"], url: "https://jmi.ac.in" },
    { name: "University of Mumbai", location: "India", courses: ["Arts", "Commerce", "Science"], url: "https://mu.ac.in" },
    { name: "University of Calcutta", location: "India", courses: ["Arts", "Science", "Commerce"], url: "https://www.caluniv.ac.in" },
    { name: "Banaras Hindu University (BHU)", location: "India", courses: ["Arts", "Science", "Law"], url: "https://www.bhu.ac.in" },
    { name: "Aligarh Muslim University (AMU)", location: "India", courses: ["Engineering", "Science", "Medicine"], url: "https://www.amu.ac.in" },
    { name: "IIT Kharagpur", location: "India", courses: ["Engineering", "Management"], url: "https://www.iitkgp.ac.in" },
    { name: "IIT Kanpur", location: "India", courses: ["Engineering", "Technology"], url: "https://www.iitk.ac.in" },
    { name: "IIT Roorkee", location: "India", courses: ["Engineering", "Architecture"], url: "https://www.iitr.ac.in" },
    { name: "University College London (UCL)", location: "UK", courses: ["Arts", "Science", "Engineering"], url: "https://www.ucl.ac.uk" },
    { name: "Imperial College London", location: "UK", courses: ["Science", "Engineering", "Medicine"], url: "https://www.imperial.ac.uk" },
    { name: "King's College London", location: "UK", courses: ["Arts", "Law", "Medicine"], url: "https://www.kcl.ac.uk" },
    { name: "London School of Economics (LSE)", location: "UK", courses: ["Economics", "Social Sciences"], url: "https://www.lse.ac.uk" },
    { name: "University of Edinburgh", location: "UK", courses: ["Arts", "Science", "Law"], url: "https://www.ed.ac.uk" },
    { name: "University of Manchester", location: "UK", courses: ["Arts", "Engineering", "Science"], url: "https://www.manchester.ac.uk" },
    { name: "University of Warwick", location: "UK", courses: ["Arts", "Business", "Science"], url: "https://www.warwick.ac.uk" },
    { name: "University of Bristol", location: "UK", courses: ["Engineering", "Science", "Medicine"], url: "https://www.bristol.ac.uk" },
    { name: "University of Glasgow", location: "UK", courses: ["Arts", "Science", "Engineering"], url: "https://www.gla.ac.uk" },
    { name: "McGill University", location: "Canada", courses: ["Arts", "Science", "Engineering"], url: "https://www.mcgill.ca" },
    { name: "University of British Columbia", location: "Canada", courses: ["Arts", "Science", "Business"], url: "https://www.ubc.ca" },
    { name: "University of Sydney", location: "Australia", courses: ["Arts", "Engineering", "Medicine"], url: "https://www.sydney.edu.au" },
    { name: "Australian National University (ANU)", location: "Australia", courses: ["Arts", "Science", "Business"], url: "https://www.anu.edu.au" },
    { name: "University of Tokyo", location: "Japan", courses: ["Science", "Engineering", "Arts"], url: "https://www.u-tokyo.ac.jp/en/" },
    { name: "Kyoto University", location: "Japan", courses: ["Arts", "Science", "Engineering"], url: "https://www.kyoto-u.ac.jp/en" },
    { name: "Peking University", location: "China", courses: ["Arts", "Science", "Engineering"], url: "https://english.pku.edu.cn/" },
    { name: "Tsinghua University", location: "China", courses: ["Engineering", "Science", "Arts"], url: "https://www.tsinghua.edu.cn/en/" },
    { name: "Heidelberg University", location: "Germany", courses: ["Arts", "Science", "Medicine"], url: "https://www.uni-heidelberg.de/en" },
    { name: "University of Munich (LMU)", location: "Germany", courses: ["Arts", "Science", "Medicine"], url: "https://www.lmu.de/en/" },
    { name: "Sorbonne University", location: "France", courses: ["Arts", "Science"], url: "https://www.sorbonne-universite.fr/en" },
    { name: "ParisTech", location: "France", courses: ["Engineering"], url: "https://www.paristech.fr/en/" },
    { name: "University of Amsterdam", location: "Netherlands", courses: ["Humanities", "Science"], url: "https://www.uva.nl/en" },
    { name: "Trinity College Dublin", location: "Ireland", courses: ["Arts", "Science", "Business"], url: "https://www.tcd.ie/" },
    { name: "University of Hong Kong", location: "Hong Kong", courses: ["Arts", "Business", "Engineering"], url: "https://www.hku.hk/" },
  ];

  const [colleges, setColleges] = useState(fallbackColleges);

  // Fetch colleges from backend
  useEffect(() => {
    const fetchColleges = async () => {
      console.log("🔍 Fetching colleges from backend...");
      setLoading(true);
      setError(null);

      try {
        const data = await ApiService.getColleges();
        console.log("✅ Colleges data received:", data);

        if (Array.isArray(data)) {
          setColleges(data);
        } else if (data.colleges && Array.isArray(data.colleges)) {
          setColleges(data.colleges);
        } else {
          console.warn("⚠️ Unexpected backend response format, using fallback data");
          setColleges(fallbackColleges);
        }
      } catch (err) {
        console.error("❌ Failed to fetch colleges from backend:", err.message);
        console.log("⚠️ Using local fallback college data");
        // Don't show error to user since fallback data works fine
        setColleges(fallbackColleges);
      } finally {
        setLoading(false);
      }
    };

    fetchColleges();
  }, []);

  const filtered = colleges.filter(
    (c) =>
      c.name.toLowerCase().includes(query.toLowerCase()) ||
      c.location.toLowerCase().includes(query.toLowerCase()) ||
      c.courses.some((course) => course.toLowerCase().includes(query.toLowerCase()))
  );

  const styles = {
    container: {
      minHeight: "100vh",
      padding: "40px 20px",
      background: darkMode ? "#0f1720" : "#f0f4f8",
      color: darkMode ? "#f5f5f5" : "#000",
      fontFamily: "Arial, sans-serif",
      transition: "all 0.3s",
    },
    header: {
      textAlign: "center",
      color: darkMode ? "#61dafb" : "#0077b6",
      fontSize: "36px",
      fontWeight: "bold",
      marginBottom: "20px",
    },
    input: {
      width: "100%",
      padding: "12px 16px",
      borderRadius: "12px",
      border: darkMode ? "1px solid #444" : "1px solid #dde6ec",
      marginBottom: "30px",
      fontSize: "16px",
      background: darkMode ? "#1b1b2f" : "#fff",
      color: darkMode ? "#f5f5f5" : "#000",
      transition: "all 0.3s",
    },
    grid: {
      display: "grid",
      gap: "20px",
      gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
    },
    card: {
      background: darkMode ? "#1b1b2f" : "#fff",
      padding: "20px",
      borderRadius: "16px",
      boxShadow: darkMode
        ? "0 4px 12px rgba(0,0,0,0.4)"
        : "0 4px 12px rgba(0,0,0,0.08)",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
      transition: "all 0.3s",
      cursor: "pointer",
    },
    collegeName: {
      fontSize: "20px",
      fontWeight: "bold",
      color: darkMode ? "#61dafb" : "#023e8a",
      marginBottom: "8px",
    },
    info: {
      display: "flex",
      alignItems: "center",
      color: darkMode ? "#ccc" : "#555",
      fontSize: "14px",
      marginBottom: "6px",
    },
    icon: {
      marginRight: "6px",
      color: darkMode ? "#61dafb" : "#0077b6",
    },
    visitButton: {
      marginTop: "12px",
      textAlign: "center",
      padding: "10px",
      borderRadius: "12px",
      backgroundColor: darkMode ? "#61dafb" : "#0077b6",
      color: darkMode ? "#1e1e2f" : "#fff",
      textDecoration: "none",
      fontWeight: "bold",
      display: "inline-block",
      transition: "all 0.3s",
    },
    noResult: {
      gridColumn: "1 / -1",
      textAlign: "center",
      color: darkMode ? "#aaa" : "#555",
    },
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>College Finder</h2>

      {loading && (
        <div style={{ textAlign: "center", padding: 20, color: darkMode ? "#aaa" : "#555" }}>
          Loading colleges...
        </div>
      )}

      <input
        type="text"
        placeholder="Search by name, location, or courses..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={styles.input}
      />

      <div style={styles.grid}>
        {filtered.length ? (
          filtered.map((c) => (
            <div
              key={c.name}
              style={styles.card}
              onMouseEnter={(e) => (e.currentTarget.style.transform = "translateY(-5px)")}
              onMouseLeave={(e) => (e.currentTarget.style.transform = "translateY(0)")}
            >
              <div>
                <div style={styles.collegeName}>{c.name}</div>

                <div style={styles.info}>
                  <FaMapMarkerAlt style={styles.icon} />
                  {c.location}
                </div>

                <div style={styles.info}>
                  <FaBook style={styles.icon} />
                  Courses: {c.courses.join(", ")}
                </div>
              </div>

              <a
                href={c.url}
                target="_blank"
                rel="noopener noreferrer"
                style={styles.visitButton}
              >
                Visit Website
              </a>
            </div>
          ))
        ) : (
          <div style={styles.noResult}>No colleges found.</div>
        )}
      </div>
    </div>
  );
}