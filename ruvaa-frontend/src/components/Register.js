import React, { useState } from "react";
import ApiService from "../services/api";

export default function Register({ onRegister, setPage, showToast }) {
  // Basic Information
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  
  // Additional Required Fields
  const [phoneNumber, setPhoneNumber] = useState("");
  const [age, setAge] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [educationLevel, setEducationLevel] = useState("");
  const [institutionName, setInstitutionName] = useState("");
  const [stream, setStream] = useState("");
  const [agreeToTerms, setAgreeToTerms] = useState(false);
  const [agreeToPrivacyPolicy, setAgreeToPrivacyPolicy] = useState(false);
  
  const [loading, setLoading] = useState(false);

  // Education level options
  const educationLevels = [
    { value: "HIGH_SCHOOL", label: "High School (10th/12th)" },
    { value: "BACHELOR_SCIENCE", label: "Bachelor's in Science" },
    { value: "BACHELOR_COMMERCE", label: "Bachelor's in Commerce" },
    { value: "BACHELOR_ARTS", label: "Bachelor's in Arts" },
    { value: "BACHELOR_ENGINEERING", label: "Bachelor's in Engineering" },
    { value: "MASTER_SCIENCE", label: "Master's in Science" },
    { value: "MASTER_COMMERCE", label: "Master's in Commerce" },
    { value: "MASTER_ARTS", label: "Master's in Arts" },
    { value: "MASTER_ENGINEERING", label: "Master's in Engineering" },
    { value: "PHD", label: "Ph.D" },
    { value: "DIPLOMA", label: "Diploma" },
    { value: "OTHER", label: "Other" }
  ];

  // Indian states
  const indianStates = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", 
    "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", 
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", 
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", 
    "Uttarakhand", "West Bengal", "Delhi", "Jammu and Kashmir", "Ladakh"
  ];

  const submit = async (e) => {
    e.preventDefault();

    console.log("📝 Student Registration form submitted");

    // Basic validation
    if (!fullName || !email || !password || !confirmPassword || !phoneNumber || !age || 
        !city || !state || !educationLevel || !institutionName || !stream) {
  showToast && showToast("Please fill in all required fields", 'error');
      return;
    }

    if (password !== confirmPassword) {
  showToast && showToast("Passwords do not match", 'error');
      return;
    }

    if (password.length < 8) {
  showToast && showToast("Password must be at least 8 characters long and contain uppercase, lowercase, digit, and special character", 'error');
      return;
    }

    // Phone number validation
    if (!/^[6-9]\d{9}$/.test(phoneNumber)) {
  showToast && showToast("Please enter a valid Indian mobile number (10 digits starting with 6-9)", 'error');
      return;
    }

    // Age validation
    if (parseInt(age) < 13 || parseInt(age) > 35) {
  showToast && showToast("Age must be between 13 and 35", 'error');
      return;
    }

    if (!agreeToTerms || !agreeToPrivacyPolicy) {
  showToast && showToast("Please agree to the Terms of Service and Privacy Policy", 'error');
      return;
    }

    setLoading(true);
    try {
      const studentData = {
        email: email.trim(),
        password,
        fullName: fullName.trim(),
        phoneNumber: phoneNumber.trim(),
        age: parseInt(age),
        city: city.trim(),
        state,
        educationLevel,
        institutionName: institutionName.trim(),
        stream: stream.trim(),
        agreeToTerms,
        agreeToPrivacyPolicy
      };

      console.log("📤 Sending student registration request to backend:", studentData);
      const response = await ApiService.studentRegister(studentData);
      console.log("✅ Student registration successful:", response);

      // Handle successful registration
      if (response.success && response.data) {
        const student = response.data;
        // Received profile from backend (may contain seeded fields)
        const rawProfile = student.profile || {};
        const displayName = student.name || student.fullName || fullName.trim();
        // Merge name/email for display convenience
        const mergedProfile = { 
          name: displayName, 
          email: student.email, 
          ...rawProfile 
        };
        localStorage.setItem('cc_profile', JSON.stringify(mergedProfile));
        onRegister({ 
          id: student.id, 
          name: displayName, 
          email: student.email,
          type: 'student',
          profile: mergedProfile
        });
  showToast && showToast("Registration successful! Welcome to CareerConnect!", 'success');
      } else {
  showToast && showToast("Registration completed but response format is unexpected. Please try logging in.", 'warning');
      }
    } catch (error) {
      console.error("❌ Student registration failed:", error);
  showToast && showToast("Registration failed: " + (error.message || "Unknown error"), 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={container}>
      {/* Left Image */}
      <div style={imageWrapper}>
        <img src="/login.jpg" alt="CareerConnect" style={imageStyle} />
        <div style={imageOverlay}>
          <h2 style={overlayTitle}>Join CareerConnect</h2>
          <p style={overlayText}>Start your personalized career journey today.</p>
        </div>
      </div>

      {/* Right Form */}
      <div style={formWrapper}>
        <h1 style={formTitle}>Create Account</h1>
        <p style={formSubtitle}>Sign up to discover your career path</p>

        <form onSubmit={submit} style={formStyle}>
          {/* Basic Information Section */}
          <div style={sectionStyle}>
            <h3 style={sectionHeaderStyle}>Personal Information</h3>
            <div style={formRowStyle}>
              <input
                aria-label="fullName"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Full Name *"
                style={inputStyle}
                required
              />
              <input
                aria-label="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email Address *"
                style={inputStyle}
                required
              />
            </div>
            <div style={formRowStyle}>
              <input
                aria-label="phoneNumber"
                type="tel"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                placeholder="Mobile Number (10 digits) *"
                style={inputStyle}
                maxLength="10"
                pattern="[6-9][0-9]{9}"
                required
              />
              <input
                aria-label="age"
                type="number"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                placeholder="Age *"
                style={inputStyle}
                min="13"
                max="35"
                required
              />
            </div>
          </div>

          {/* Location Information */}
          <div style={sectionStyle}>
            <h3 style={sectionHeaderStyle}>Location</h3>
            <div style={formRowStyle}>
              <input
                aria-label="city"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                placeholder="City *"
                style={inputStyle}
                required
              />
              <select
                aria-label="state"
                value={state}
                onChange={(e) => setState(e.target.value)}
                style={selectStyle}
                required
              >
                <option value="">Select State *</option>
                {indianStates.map(stateName => (
                  <option key={stateName} value={stateName}>{stateName}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Education Information */}
          <div style={sectionStyle}>
            <h3 style={sectionHeaderStyle}>Education Details</h3>
            <select
              aria-label="educationLevel"
              value={educationLevel}
              onChange={(e) => setEducationLevel(e.target.value)}
              style={{...selectStyle, marginBottom: '12px'}}
              required
            >
              <option value="">Select Education Level *</option>
              {educationLevels.map(level => (
                <option key={level.value} value={level.value}>{level.label}</option>
              ))}
            </select>
            <div style={formRowStyle}>
              <input
                aria-label="institutionName"
                value={institutionName}
                onChange={(e) => setInstitutionName(e.target.value)}
                placeholder="Institution Name *"
                style={inputStyle}
                required
              />
              <input
                aria-label="stream"
                value={stream}
                onChange={(e) => setStream(e.target.value)}
                placeholder="Stream/Field of Study *"
                style={inputStyle}
                required
              />
            </div>
          </div>

          {/* Security Section */}
          <div style={sectionStyle}>
            <h3 style={sectionHeaderStyle}>Account Security</h3>
            <input
              aria-label="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password (min 8 chars with special chars) *"
              type="password"
              style={inputStyle}
              required
            />
            <input
              aria-label="confirm-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm Password *"
              type="password"
              style={inputStyle}
              required
            />
          </div>

          {/* Agreement Section */}
          <div style={agreementSectionStyle}>
            <label style={checkboxLabelStyle}>
              <input
                type="checkbox"
                checked={agreeToTerms}
                onChange={(e) => setAgreeToTerms(e.target.checked)}
                style={checkboxStyle}
                required
              />
              I agree to the <span style={linkStyle}>Terms of Service</span>
            </label>
            <label style={checkboxLabelStyle}>
              <input
                type="checkbox"
                checked={agreeToPrivacyPolicy}
                onChange={(e) => setAgreeToPrivacyPolicy(e.target.checked)}
                style={checkboxStyle}
                required
              />
              I agree to the <span style={linkStyle}>Privacy Policy</span>
            </label>
          </div>

          <button type="submit" style={btnStyle} disabled={loading}>
            {loading ? "Creating Account..." : "Create Student Account"}
          </button>
        </form>

        <div style={linkContainer}>
          Already have an account?{" "}
          <span style={linkStyle} onClick={() => setPage("login")}>
            Sign in
          </span>
        </div>
      </div>

      <style>{`
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body { overflow-x: hidden; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        
        input:focus, select:focus { 
          outline: none; 
          border-color: #00b4d8 !important; 
          background: white !important;
          box-shadow: 0 0 0 3px rgba(0,180,216,0.1);
        }
        
        button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 10px 25px rgba(0,180,216,0.3);
        }
        
        @media(max-width: 992px) {
          div[style*="maxWidth: 1200"] {
            flex-direction: column;
            max-width: 95%;
            margin: 10px auto;
          }
          
          div[style*="flex: 1"][style*="position: relative"] { 
            min-height: 300px; 
          }
          
          div[style*="flex: 1.2"] { 
            padding: 20px 25px; 
          }
        }
        
        @media(max-width: 768px) {
          div[style*="maxWidth: 1200"] {
            flex-direction: column;
            max-width: 98%;
            margin: 5px auto;
            border-radius: 15px;
          }
          
          div[style*="flex: 1"][style*="position: relative"] { 
            min-height: 250px; 
          }
          
          div[style*="flex: 1.2"] { 
            padding: 15px 20px; 
          }
          
          div[style*="display: flex"][style*="gap: 15px"] {
            flex-direction: column;
            gap: 12px;
          }
          
          input, select {
            font-size: 16px !important; /* Prevents zoom on iOS */
          }
        }
        
        @media(max-width: 480px) {
          div[style*="flex: 1"][style*="position: relative"] { 
            display: none; 
          }
          
          div[style*="flex: 1.2"] { 
            padding: 15px; 
          }
        }
      `}</style>
    </div>
  );
}

// Styles
const container = { 
  display: "flex", 
  flexDirection: "row", 
  width: "100%", 
  maxWidth: 1200, 
  minHeight: "90vh", 
  margin: "20px auto", 
  borderRadius: 20, 
  overflow: "hidden", 
  boxShadow: "0 20px 60px rgba(2,6,23,0.15)", 
  background: "white" 
};

const imageWrapper = { 
  flex: 1, 
  position: "relative", 
  minWidth: 0,
  minHeight: "600px" 
};

const imageStyle = { 
  width: "100%", 
  height: "100%", 
  objectFit: "cover", 
  display: "block" 
};

const imageOverlay = { 
  position: "absolute", 
  top: 0, 
  left: 0, 
  width: "100%", 
  height: "100%", 
  background: "linear-gradient(135deg, rgba(0,180,216,0.8), rgba(0,119,182,0.8))", 
  display: "flex", 
  flexDirection: "column", 
  justifyContent: "center", 
  alignItems: "center", 
  color: "white", 
  textAlign: "center", 
  padding: 40 
};

const overlayTitle = { 
  margin: 0, 
  fontSize: 32, 
  fontWeight: 700,
  marginBottom: 15 
};

const overlayText = { 
  fontSize: 18, 
  opacity: 0.95,
  lineHeight: 1.5 
};

const formWrapper = { 
  flex: 1.2, 
  padding: "30px 40px", 
  display: "flex", 
  flexDirection: "column", 
  minWidth: 0, 
  boxSizing: "border-box",
  overflowY: "auto",
  maxHeight: "90vh"
};

const formTitle = { 
  margin: 0, 
  color: "#0077b6", 
  fontSize: 28,
  fontWeight: 700 
};

const formSubtitle = { 
  color: "#6c757d", 
  marginBottom: 20,
  fontSize: 16 
};

const formStyle = { 
  display: "flex", 
  flexDirection: "column", 
  gap: 0, 
  marginTop: 15 
};

const sectionStyle = {
  marginBottom: 25,
  padding: "20px 0",
  borderBottom: "1px solid #f0f0f0"
};

const sectionHeaderStyle = {
  color: "#0077b6",
  fontSize: 16,
  fontWeight: 600,
  marginBottom: 15,
  marginTop: 0
};

const formRowStyle = {
  display: "flex",
  gap: 15,
  marginBottom: 12
};

const inputStyle = { 
  padding: "14px 16px", 
  borderRadius: 12, 
  border: "2px solid #e9ecef", 
  background: "#fafbfc", 
  color: "#212529", 
  fontSize: 15,
  transition: "all 0.3s ease",
  flex: 1,
  "&:focus": {
    borderColor: "#00b4d8",
    outline: "none",
    background: "white"
  }
};

const selectStyle = { 
  ...inputStyle,
  cursor: "pointer"
};

const agreementSectionStyle = {
  marginBottom: 25,
  padding: "15px 0"
};

const checkboxLabelStyle = {
  display: "flex",
  alignItems: "center",
  marginBottom: 10,
  fontSize: 14,
  color: "#495057",
  cursor: "pointer"
};

const checkboxStyle = {
  marginRight: 10,
  transform: "scale(1.2)",
  accentColor: "#00b4d8"
};

const btnStyle = { 
  padding: "16px 20px", 
  borderRadius: 12, 
  border: "none", 
  background: "linear-gradient(135deg, #00b4d8, #0077b6)", 
  color: "white", 
  fontWeight: 700, 
  cursor: "pointer", 
  fontSize: 16,
  transition: "all 0.3s ease",
  marginTop: 10,
  "&:hover": {
    transform: "translateY(-2px)",
    boxShadow: "0 10px 25px rgba(0,180,216,0.3)"
  },
  "&:disabled": {
    opacity: 0.7,
    cursor: "not-allowed"
  }
};

const linkContainer = { 
  marginTop: 20, 
  textAlign: "center", 
  color: "#6c757d", 
  fontSize: 14 
};

const linkStyle = { 
  color: "#0077b6", 
  fontWeight: 600, 
  cursor: "pointer", 
  textDecoration: "underline" 
};
