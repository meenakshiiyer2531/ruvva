import React, { useState } from 'react';
import config from '../config/config';

export default function CareerSelector({ 
  selectedCareers = [], 
  onCareerChange, 
  availableCareers = [], 
  maxSelections = config.limits.maxCareerSelections || 2,
  showRecommendations = true 
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  
  // Career categories and extensive career database
  const careerCategories = {
    'Technology': {
      icon: '💻',
      color: '#2196f3',
      careers: [
        'Software Engineer', 'Data Scientist', 'AI Engineer', 'Cybersecurity Analyst', 'DevOps Engineer',
        'Full Stack Developer', 'Mobile App Developer', 'Cloud Architect', 'Machine Learning Engineer',
        'Blockchain Developer', 'Game Developer', 'UI/UX Designer', 'Product Manager', 'Systems Analyst',
        'Database Administrator', 'Network Engineer', 'Quality Assurance Engineer', 'Site Reliability Engineer',
        'Technical Writer', 'Solution Architect', 'Big Data Engineer', 'Computer Vision Engineer'
      ]
    },
    'Healthcare': {
      icon: '🏥',
      color: '#4caf50',
      careers: [
        'Medical Doctor', 'Registered Nurse', 'Pharmacist', 'Physical Therapist', 'Dentist',
        'Veterinarian', 'Medical Technologist', 'Radiologist', 'Surgeon', 'Psychiatrist',
        'Paramedic', 'Occupational Therapist', 'Speech Therapist', 'Nutritionist', 'Medical Researcher',
        'Healthcare Administrator', 'Biomedical Engineer', 'Clinical Psychologist', 'Optometrist',
        'Anesthesiologist', 'Cardiologist', 'Dermatologist', 'Orthopedic Surgeon', 'Pediatrician'
      ]
    },
    'Business & Finance': {
      icon: '💼',
      color: '#ff9800',
      careers: [
        'Business Analyst', 'Financial Analyst', 'Investment Banker', 'Accountant', 'Marketing Manager',
        'Sales Manager', 'Human Resources Manager', 'Management Consultant', 'Project Manager',
        'Operations Manager', 'Business Development Manager', 'Digital Marketing Specialist',
        'Financial Advisor', 'Risk Manager', 'Auditor', 'Corporate Lawyer', 'Brand Manager',
        'Supply Chain Manager', 'Market Research Analyst', 'Entrepreneur', 'CFO', 'CEO'
      ]
    },
    'Engineering': {
      icon: '⚙️',
      color: '#795548',
      careers: [
        'Mechanical Engineer', 'Civil Engineer', 'Electrical Engineer', 'Chemical Engineer',
        'Aerospace Engineer', 'Environmental Engineer', 'Industrial Engineer', 'Biomedical Engineer',
        'Petroleum Engineer', 'Nuclear Engineer', 'Materials Engineer', 'Mining Engineer',
        'Agricultural Engineer', 'Marine Engineer', 'Automotive Engineer', 'Structural Engineer',
        'Robotics Engineer', 'Manufacturing Engineer', 'Safety Engineer', 'Process Engineer'
      ]
    },
    'Creative & Design': {
      icon: '🎨',
      color: '#e91e63',
      careers: [
        'Graphic Designer', 'Interior Designer', 'Fashion Designer', 'Photographer', 'Videographer',
        'Content Writer', 'Copywriter', 'Art Director', 'Animation Artist', 'Web Designer',
        'Product Designer', 'Industrial Designer', 'Architect', 'Illustrator', 'Brand Designer',
        'Motion Graphics Designer', 'Creative Director', 'Social Media Manager', 'Film Director',
        'Music Producer', 'Sound Engineer', 'Game Designer'
      ]
    },
    'Education': {
      icon: '🎓',
      color: '#9c27b0',
      careers: [
        'Teacher', 'Professor', 'Principal', 'Education Administrator', 'Curriculum Developer',
        'Educational Consultant', 'School Counselor', 'Librarian', 'Training Specialist',
        'Instructional Designer', 'Academic Researcher', 'Education Technology Specialist',
        'Special Education Teacher', 'Early Childhood Educator', 'Corporate Trainer',
        'Educational Psychologist', 'College Admissions Counselor', 'Tutor', 'Coach'
      ]
    },
    'Science & Research': {
      icon: '🔬',
      color: '#00bcd4',
      careers: [
        'Research Scientist', 'Laboratory Technician', 'Biologist', 'Chemist', 'Physicist',
        'Environmental Scientist', 'Geologist', 'Meteorologist', 'Astronomer', 'Marine Biologist',
        'Forensic Scientist', 'Biomedical Researcher', 'Agricultural Scientist', 'Food Scientist',
        'Materials Scientist', 'Clinical Research Coordinator', 'Quality Control Analyst',
        'Patent Examiner', 'Scientific Writer', 'Research Administrator'
      ]
    },
    'Legal & Government': {
      icon: '⚖️',
      color: '#607d8b',
      careers: [
        'Lawyer', 'Judge', 'Paralegal', 'Legal Assistant', 'Court Reporter',
        'Legal Consultant', 'Corporate Counsel', 'Public Defender', 'Prosecutor',
        'Immigration Lawyer', 'Patent Attorney', 'Tax Attorney', 'Family Lawyer',
        'Criminal Defense Lawyer', 'Government Official', 'Policy Analyst', 'Diplomat',
        'Civil Servant', 'Legislative Assistant', 'Compliance Officer'
      ]
    }
  };

  // Flatten all careers with their categories
  const allCareers = Object.entries(careerCategories).flatMap(([category, data]) =>
    data.careers.map(career => ({
      name: career,
      category,
      icon: data.icon,
      color: data.color,
      id: career.toLowerCase().replace(/\s+/g, '-')
    }))
  );

  // Filter careers based on search and category
  const filteredCareers = allCareers.filter(career => {
    const matchesSearch = career.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || career.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Handle career selection/deselection
  const handleCareerToggle = (career) => {
    if (selectedCareers.some(selected => selected.id === career.id)) {
      // Remove career if already selected
      const updatedCareers = selectedCareers.filter(selected => selected.id !== career.id);
      onCareerChange(updatedCareers);
    } else if (selectedCareers.length < maxSelections) {
      // Add career if under limit
      const updatedCareers = [...selectedCareers, career];
      onCareerChange(updatedCareers);
    } else {
      // Show limit exceeded message
      alert(`You can only select up to ${maxSelections} careers. Please remove one to add another.`);
    }
  };

  // Clear all selections
  const handleClearAll = () => {
    onCareerChange([]);
  };

  // Get selection stats
  const selectionStats = {
    selected: selectedCareers.length,
    remaining: Math.max(0, maxSelections - selectedCareers.length),
    maxReached: selectedCareers.length >= maxSelections
  };

  return (
    <div style={containerStyle}>
      {/* Header */}
      <div style={headerStyle}>
        <h3 style={titleStyle}>Select Your Career Interests</h3>
        <div style={statsStyle}>
          <span style={statStyle}>
            {selectionStats.selected} / {maxSelections} selected
          </span>
          {selectionStats.maxReached && (
            <span style={limitStyle}>
              ⚠️ Limit reached
            </span>
          )}
        </div>
      </div>

      {/* Selection Display */}
      {selectedCareers.length > 0 && (
        <div style={selectedSectionStyle}>
          <div style={selectedHeaderStyle}>
            <span style={selectedTitleStyle}>Your Selected Careers</span>
            <button onClick={handleClearAll} style={clearButtonStyle}>
              Clear All
            </button>
          </div>
          <div style={selectedListStyle}>
            {selectedCareers.map(career => (
              <div key={career.id} style={selectedItemStyle}>
                <span style={selectedIconStyle}>{career.icon}</span>
                <span style={selectedNameStyle}>{career.name}</span>
                <span style={selectedCategoryStyle}>{career.category}</span>
                <button 
                  onClick={() => handleCareerToggle(career)}
                  style={removeButtonStyle}
                  title="Remove career"
                >
                  ✖️
                </button>
              </div>
            ))}
          </div>
          
          {showRecommendations && selectionStats.maxReached && (
            <div style={recommendationStyle}>
              <span style={recommendationIconStyle}>💡</span>
              <span style={recommendationTextStyle}>
                Perfect! With these {maxSelections} careers selected, our AI can provide highly targeted 
                recommendations and learning paths tailored to your interests.
              </span>
            </div>
          )}
        </div>
      )}

      {/* Search and Filter */}
      <div style={searchSectionStyle}>
        <div style={searchBoxStyle}>
          <span style={searchIconStyle}>🔍</span>
          <input
            type="text"
            placeholder="Search careers..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={searchInputStyle}
          />
        </div>
        
        <div style={categoryFilterStyle}>
          <button
            onClick={() => setSelectedCategory('all')}
            style={{
              ...categoryButtonStyle,
              background: selectedCategory === 'all' ? '#00b4d8' : 'transparent',
              color: selectedCategory === 'all' ? 'white' : 'var(--text)'
            }}
          >
            All Categories
          </button>
          {Object.entries(careerCategories).map(([category, data]) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              style={{
                ...categoryButtonStyle,
                background: selectedCategory === category ? data.color : 'transparent',
                color: selectedCategory === category ? 'white' : 'var(--text)',
                border: `1px solid ${data.color}`
              }}
            >
              {data.icon} {category}
            </button>
          ))}
        </div>
      </div>

      {/* Career Grid */}
      <div style={careerGridStyle}>
        {filteredCareers.length === 0 ? (
          <div style={noResultsStyle}>
            <span style={noResultsIconStyle}>🤷‍♂️</span>
            <div style={noResultsTextStyle}>
              No careers found matching your search criteria.
            </div>
          </div>
        ) : (
          filteredCareers.map(career => {
            const isSelected = selectedCareers.some(selected => selected.id === career.id);
            const canSelect = !isSelected && !selectionStats.maxReached;
            
            return (
              <div
                key={career.id}
                onClick={() => handleCareerToggle(career)}
                style={{
                  ...careerCardStyle,
                  borderColor: isSelected ? career.color : '#e0e0e0',
                  background: isSelected ? `${career.color}10` : 'var(--card)',
                  opacity: (!canSelect && !isSelected) ? 0.5 : 1,
                  cursor: (canSelect || isSelected) ? 'pointer' : 'not-allowed',
                  transform: isSelected ? 'scale(0.98)' : 'scale(1)'
                }}
              >
                <div style={careerIconStyle}>
                  {career.icon}
                  {isSelected && (
                    <div style={selectedBadgeStyle}>✓</div>
                  )}
                </div>
                <div style={careerNameStyle}>{career.name}</div>
                <div style={careerCategoryStyle}>{career.category}</div>
                
                {(!canSelect && !isSelected) && (
                  <div style={disabledOverlayStyle}>
                    <span style={disabledTextStyle}>Limit Reached</span>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Help Text */}
      <div style={helpStyle}>
        <span style={helpIconStyle}>💡</span>
        <span style={helpTextStyle}>
          Select up to {maxSelections} careers that interest you most. This helps our AI provide 
          better recommendations and personalized learning paths.
        </span>
      </div>
    </div>
  );
}

// Styles
const containerStyle = {
  width: '100%',
  maxWidth: 1200,
  margin: '0 auto',
  padding: 24
};

const headerStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  marginBottom: 24
};

const titleStyle = {
  fontSize: 24,
  fontWeight: 600,
  color: 'var(--text)',
  margin: 0
};

const statsStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: 12
};

const statStyle = {
  fontSize: 14,
  color: 'var(--muted)',
  background: '#f0f0f0',
  padding: '4px 12px',
  borderRadius: 16,
  fontWeight: 500
};

const limitStyle = {
  fontSize: 12,
  color: '#ff5722',
  background: '#fff3e0',
  padding: '4px 8px',
  borderRadius: 12,
  fontWeight: 600
};

const selectedSectionStyle = {
  background: 'var(--card)',
  border: '2px solid #00b4d8',
  borderRadius: 12,
  padding: 20,
  marginBottom: 24
};

const selectedHeaderStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  marginBottom: 16
};

const selectedTitleStyle = {
  fontSize: 16,
  fontWeight: 600,
  color: '#00b4d8'
};

const clearButtonStyle = {
  background: '#ff5722',
  color: 'white',
  border: 'none',
  padding: '6px 12px',
  borderRadius: 6,
  fontSize: 12,
  fontWeight: 500,
  cursor: 'pointer'
};

const selectedListStyle = {
  display: 'flex',
  flexWrap: 'wrap',
  gap: 12,
  marginBottom: 16
};

const selectedItemStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: 8,
  background: '#f0f9ff',
  border: '1px solid #00b4d8',
  borderRadius: 8,
  padding: '8px 12px',
  fontSize: 14
};

const selectedIconStyle = {
  fontSize: 16
};

const selectedNameStyle = {
  fontWeight: 500,
  color: 'var(--text)'
};

const selectedCategoryStyle = {
  fontSize: 12,
  color: 'var(--muted)',
  background: '#e3f2fd',
  padding: '2px 6px',
  borderRadius: 4
};

const removeButtonStyle = {
  background: 'none',
  border: 'none',
  color: '#ff5722',
  cursor: 'pointer',
  fontSize: 12,
  padding: 2
};

const recommendationStyle = {
  display: 'flex',
  alignItems: 'flex-start',
  gap: 12,
  background: '#e8f5e8',
  padding: 12,
  borderRadius: 8,
  border: '1px solid #4caf50'
};

const recommendationIconStyle = {
  fontSize: 16,
  marginTop: 2
};

const recommendationTextStyle = {
  fontSize: 14,
  color: '#2e7d32',
  lineHeight: 1.4
};

const searchSectionStyle = {
  marginBottom: 24
};

const searchBoxStyle = {
  display: 'flex',
  alignItems: 'center',
  background: 'var(--card)',
  border: '1px solid #ddd',
  borderRadius: 8,
  padding: '12px 16px',
  marginBottom: 16
};

const searchIconStyle = {
  fontSize: 16,
  color: 'var(--muted)',
  marginRight: 12
};

const searchInputStyle = {
  flex: 1,
  background: 'none',
  border: 'none',
  outline: 'none',
  fontSize: 14,
  color: 'var(--text)'
};

const categoryFilterStyle = {
  display: 'flex',
  gap: 8,
  flexWrap: 'wrap'
};

const categoryButtonStyle = {
  padding: '8px 16px',
  border: '1px solid #ddd',
  borderRadius: 20,
  fontSize: 14,
  fontWeight: 500,
  cursor: 'pointer',
  transition: 'all 0.3s ease',
  whiteSpace: 'nowrap'
};

const careerGridStyle = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
  gap: 16,
  marginBottom: 24
};

const noResultsStyle = {
  gridColumn: '1 / -1',
  textAlign: 'center',
  padding: 40,
  color: 'var(--muted)'
};

const noResultsIconStyle = {
  fontSize: 48,
  marginBottom: 16,
  display: 'block'
};

const noResultsTextStyle = {
  fontSize: 16
};

const careerCardStyle = {
  position: 'relative',
  background: 'var(--card)',
  border: '2px solid #e0e0e0',
  borderRadius: 12,
  padding: 16,
  textAlign: 'center',
  cursor: 'pointer',
  transition: 'all 0.3s ease',
  minHeight: 120
};

const careerIconStyle = {
  position: 'relative',
  fontSize: 32,
  marginBottom: 8
};

const selectedBadgeStyle = {
  position: 'absolute',
  top: -4,
  right: -4,
  background: '#4caf50',
  color: 'white',
  borderRadius: '50%',
  width: 20,
  height: 20,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontSize: 12,
  fontWeight: 'bold'
};

const careerNameStyle = {
  fontSize: 14,
  fontWeight: 600,
  color: 'var(--text)',
  marginBottom: 4,
  lineHeight: 1.3
};

const careerCategoryStyle = {
  fontSize: 12,
  color: 'var(--muted)',
  textTransform: 'uppercase',
  letterSpacing: 0.5
};

const disabledOverlayStyle = {
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  background: 'rgba(255, 255, 255, 0.8)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  borderRadius: 12
};

const disabledTextStyle = {
  fontSize: 12,
  fontWeight: 600,
  color: '#ff5722'
};

const helpStyle = {
  display: 'flex',
  alignItems: 'flex-start',
  gap: 12,
  background: '#f0f9ff',
  padding: 16,
  borderRadius: 8,
  border: '1px solid #e3f2fd'
};

const helpIconStyle = {
  fontSize: 16,
  marginTop: 2
};

const helpTextStyle = {
  fontSize: 14,
  color: '#1976d2',
  lineHeight: 1.4
};