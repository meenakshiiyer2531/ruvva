import React, { useState, useEffect, useRef } from 'react';
import config from '../config/config';

export default function GlobalSearchBar({ onNavigate, currentPage }) {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  
  const searchRef = useRef(null);
  const resultsRef = useRef(null);

  // Search categories and items
  const searchData = {
    pages: [
      { id: 'profile', title: 'Profile', icon: '👤', description: 'View and edit your profile' },
      { id: 'career', title: 'Career Analysis', icon: '📊', description: 'Get AI-powered career insights' },
      { id: 'recommendations', title: 'Career Recommendations', icon: '🎯', description: 'Discover matching career paths' },
      { id: 'learning', title: 'Learning Paths', icon: '📚', description: 'Personalized learning roadmaps' },
      { id: 'assessment', title: 'Assessment', icon: '📝', description: 'Take skill and personality tests' },
      { id: 'chat', title: 'AI Chat', icon: '💬', description: 'Get instant career guidance' },
      { id: 'colleges', title: 'College Finder', icon: '🏛️', description: 'Find the best colleges for you' },
      { id: 'mentor', title: 'Mentor Booking', icon: '👨‍🏫', description: 'Connect with industry experts' }
    ],
    
    features: [
      { id: 'riasec', title: 'RIASEC Assessment', icon: '🧪', description: 'Personality-based career matching', page: 'assessment' },
      { id: 'skills', title: 'Skills Analysis', icon: '⚡', description: 'Evaluate your technical skills', page: 'assessment' },
      { id: 'ai-chat', title: 'Career Counselor AI', icon: '🤖', description: '24/7 AI career guidance', page: 'chat' },
      { id: 'learning-path', title: 'Custom Learning Path', icon: '🛤️', description: 'Build your learning journey', page: 'learning' },
      { id: 'mentor-session', title: 'Book Mentor Session', icon: '📅', description: 'Schedule 1:1 mentorship', page: 'mentor' },
      { id: 'college-search', title: 'College Search', icon: '🔍', description: 'Advanced college filtering', page: 'colleges' }
    ],

    careers: [
      // Technology
      { id: 'software-engineer', title: 'Software Engineer', icon: '💻', category: 'Technology', description: 'Build software applications' },
      { id: 'data-scientist', title: 'Data Scientist', icon: '📊', category: 'Technology', description: 'Analyze data for insights' },
      { id: 'ai-engineer', title: 'AI Engineer', icon: '🤖', category: 'Technology', description: 'Develop AI solutions' },
      { id: 'cybersecurity', title: 'Cybersecurity Analyst', icon: '🔒', category: 'Technology', description: 'Protect digital assets' },
      { id: 'devops-engineer', title: 'DevOps Engineer', icon: '⚙️', category: 'Technology', description: 'Streamline development processes' },
      
      // Healthcare
      { id: 'doctor', title: 'Medical Doctor', icon: '👩‍⚕️', category: 'Healthcare', description: 'Diagnose and treat patients' },
      { id: 'nurse', title: 'Registered Nurse', icon: '🩺', category: 'Healthcare', description: 'Provide patient care' },
      { id: 'pharmacist', title: 'Pharmacist', icon: '💊', category: 'Healthcare', description: 'Dispense medications' },
      
      // Business
      { id: 'marketing-manager', title: 'Marketing Manager', icon: '📈', category: 'Business', description: 'Develop marketing strategies' },
      { id: 'product-manager', title: 'Product Manager', icon: '📱', category: 'Business', description: 'Oversee product development' },
      { id: 'consultant', title: 'Business Consultant', icon: '💼', category: 'Business', description: 'Advise organizations' },
      
      // Creative
      { id: 'graphic-designer', title: 'Graphic Designer', icon: '🎨', category: 'Creative', description: 'Create visual content' },
      { id: 'ux-designer', title: 'UX Designer', icon: '📐', category: 'Creative', description: 'Design user experiences' },
      { id: 'content-writer', title: 'Content Writer', icon: '✍️', category: 'Creative', description: 'Create written content' },
      
      // Education
      { id: 'teacher', title: 'Teacher', icon: '👨‍🏫', category: 'Education', description: 'Educate students' },
      { id: 'professor', title: 'Professor', icon: '🎓', category: 'Education', description: 'Teach at university level' },
      
      // Engineering
      { id: 'mechanical-engineer', title: 'Mechanical Engineer', icon: '⚙️', category: 'Engineering', description: 'Design mechanical systems' },
      { id: 'civil-engineer', title: 'Civil Engineer', icon: '🏗️', category: 'Engineering', description: 'Design infrastructure' },
      { id: 'electrical-engineer', title: 'Electrical Engineer', icon: '⚡', category: 'Engineering', description: 'Work with electrical systems' }
    ],

    quickActions: [
      { id: 'take-assessment', title: 'Take Assessment', icon: '🚀', description: 'Start your career assessment now', page: 'assessment' },
      { id: 'chat-ai', title: 'Ask AI', icon: '💡', description: 'Get instant career advice', page: 'chat' },
      { id: 'find-mentor', title: 'Find Mentor', icon: '🔍', description: 'Connect with a mentor', page: 'mentor' },
      { id: 'explore-careers', title: 'Explore Careers', icon: '🌟', description: 'Discover new career paths', page: 'recommendations' }
    ]
  };

  // Perform search
  const performSearch = (searchQuery) => {
    if (!searchQuery.trim()) {
      setResults([]);
      return;
    }

    const query = searchQuery.toLowerCase();
    const searchResults = [];

    // Search pages
    searchData.pages.forEach(page => {
      if (page.title.toLowerCase().includes(query) || 
          page.description.toLowerCase().includes(query)) {
        searchResults.push({ ...page, type: 'page', score: page.title.toLowerCase().includes(query) ? 10 : 5 });
      }
    });

    // Search features
    searchData.features.forEach(feature => {
      if (feature.title.toLowerCase().includes(query) || 
          feature.description.toLowerCase().includes(query)) {
        searchResults.push({ ...feature, type: 'feature', score: feature.title.toLowerCase().includes(query) ? 8 : 4 });
      }
    });

    // Search careers
    searchData.careers.forEach(career => {
      if (career.title.toLowerCase().includes(query) || 
          career.category.toLowerCase().includes(query) ||
          career.description.toLowerCase().includes(query)) {
        searchResults.push({ ...career, type: 'career', score: career.title.toLowerCase().includes(query) ? 7 : 3 });
      }
    });

    // Search quick actions
    searchData.quickActions.forEach(action => {
      if (action.title.toLowerCase().includes(query) || 
          action.description.toLowerCase().includes(query)) {
        searchResults.push({ ...action, type: 'action', score: 6 });
      }
    });

    // Sort by relevance score and limit results
    const sortedResults = searchResults
      .sort((a, b) => b.score - a.score)
      .slice(0, 10);

    setResults(sortedResults);
  };

  // Handle search input
  const handleSearch = (e) => {
    const value = e.target.value;
    setQuery(value);
    setSelectedIndex(-1);
    
    if (value.length > 0) {
      setLoading(true);
      // Debounce search
      setTimeout(() => {
        performSearch(value);
        setLoading(false);
      }, 200);
    } else {
      setResults([]);
    }
  };

  // Handle result selection
  const handleResultClick = (result) => {
    const targetPage = result.page || result.id;
    
    if (targetPage && onNavigate) {
      onNavigate(targetPage);
    }
    
    setQuery('');
    setResults([]);
    setIsOpen(false);
    setSelectedIndex(-1);
  };

  // Handle keyboard navigation
  const handleKeyDown = (e) => {
    if (!isOpen || results.length === 0) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => (prev < results.length - 1 ? prev + 1 : prev));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => (prev > 0 ? prev - 1 : -1));
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0 && selectedIndex < results.length) {
          handleResultClick(results[selectedIndex]);
        }
        break;
      case 'Escape':
        setIsOpen(false);
        setQuery('');
        setResults([]);
        setSelectedIndex(-1);
        break;
      default:
        break;
    }
  };

  // Handle focus
  const handleFocus = () => {
    setIsOpen(true);
    if (query) {
      performSearch(query);
    }
  };

  // Handle click outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setIsOpen(false);
        setSelectedIndex(-1);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Don't render if search is disabled
  if (!config.features.search) {
    return null;
  }

  return (
    <div ref={searchRef} style={containerStyle}>
      <div style={searchBoxStyle}>
        <div style={searchInputContainerStyle}>
          <span style={searchIconStyle}>🔍</span>
          <input
            type="text"
            placeholder="Search careers, features, or pages..."
            value={query}
            onChange={handleSearch}
            onFocus={handleFocus}
            onKeyDown={handleKeyDown}
            style={searchInputStyle}
            autoComplete="off"
          />
          {query && (
            <button 
              onClick={() => {
                setQuery('');
                setResults([]);
                setIsOpen(false);
              }}
              style={clearButtonStyle}
            >
              ✖️
            </button>
          )}
        </div>

        {/* Search Results */}
        {isOpen && (query || results.length > 0) && (
          <div ref={resultsRef} style={resultsContainerStyle}>
            {loading && (
              <div style={loadingStyle}>
                <span>🔄</span> Searching...
              </div>
            )}

            {!loading && results.length === 0 && query && (
              <div style={noResultsStyle}>
                <span style={noResultsIconStyle}>🤷‍♂️</span>
                <div>
                  <div style={noResultsTitleStyle}>No results found</div>
                  <div style={noResultsDescStyle}>Try a different search term</div>
                </div>
              </div>
            )}

            {!loading && results.length > 0 && (
              <div>
                <div style={resultsHeaderStyle}>
                  Search Results ({results.length})
                </div>
                {results.map((result, index) => (
                  <div
                    key={`${result.type}-${result.id}`}
                    onClick={() => handleResultClick(result)}
                    style={{
                      ...resultItemStyle,
                      background: selectedIndex === index ? '#f0f9ff' : 'transparent'
                    }}
                    onMouseEnter={() => setSelectedIndex(index)}
                  >
                    <div style={resultIconStyle}>
                      {result.icon}
                    </div>
                    <div style={resultContentStyle}>
                      <div style={resultTitleStyle}>
                        {result.title}
                        <span style={resultTypeStyle}>
                          {result.type}
                        </span>
                      </div>
                      <div style={resultDescStyle}>
                        {result.description}
                      </div>
                      {result.category && (
                        <div style={resultCategoryStyle}>
                          {result.category}
                        </div>
                      )}
                    </div>
                    <div style={resultArrowStyle}>
                      →
                    </div>
                  </div>
                ))}
              </div>
            )}

            {!query && !loading && (
              <div style={suggestionsStyle}>
                <div style={suggestionHeaderStyle}>Quick Actions</div>
                {searchData.quickActions.slice(0, 4).map((action) => (
                  <div
                    key={action.id}
                    onClick={() => handleResultClick(action)}
                    style={suggestionItemStyle}
                  >
                    <span style={suggestionIconStyle}>{action.icon}</span>
                    <span style={suggestionTitleStyle}>{action.title}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// Styles
const containerStyle = {
  position: 'relative',
  width: '100%',
  maxWidth: 400
};

const searchBoxStyle = {
  position: 'relative',
  width: '100%'
};

const searchInputContainerStyle = {
  display: 'flex',
  alignItems: 'center',
  background: 'rgba(255, 255, 255, 0.15)',
  border: '1px solid rgba(255, 255, 255, 0.3)',
  borderRadius: 12,
  padding: '8px 12px',
  backdropFilter: 'blur(10px)',
  transition: 'all 0.3s ease'
};

const searchIconStyle = {
  fontSize: 16,
  marginRight: 8,
  color: 'rgba(255, 255, 255, 0.8)'
};

const searchInputStyle = {
  flex: 1,
  background: 'none',
  border: 'none',
  outline: 'none',
  color: 'white',
  fontSize: 14,
  placeholder: 'rgba(255, 255, 255, 0.7)'
};

const clearButtonStyle = {
  background: 'none',
  border: 'none',
  color: 'rgba(255, 255, 255, 0.8)',
  cursor: 'pointer',
  fontSize: 12,
  padding: 4,
  borderRadius: 4
};

const resultsContainerStyle = {
  position: 'absolute',
  top: '100%',
  left: 0,
  right: 0,
  marginTop: 8,
  background: 'var(--card)',
  border: '1px solid #e0e0e0',
  borderRadius: 12,
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.12)',
  maxHeight: 400,
  overflowY: 'auto',
  zIndex: 1001
};

const loadingStyle = {
  padding: 16,
  textAlign: 'center',
  color: 'var(--muted)',
  fontSize: 14
};

const noResultsStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: 12,
  padding: 16,
  color: 'var(--muted)'
};

const noResultsIconStyle = {
  fontSize: 24
};

const noResultsTitleStyle = {
  fontWeight: '600',
  marginBottom: 4
};

const noResultsDescStyle = {
  fontSize: 12
};

const resultsHeaderStyle = {
  padding: '12px 16px',
  fontSize: 12,
  fontWeight: '600',
  color: 'var(--muted)',
  borderBottom: '1px solid #f0f0f0',
  background: '#f9f9f9'
};

const resultItemStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: 12,
  padding: 12,
  cursor: 'pointer',
  borderBottom: '1px solid #f0f0f0',
  transition: 'background 0.2s ease'
};

const resultIconStyle = {
  fontSize: 20,
  minWidth: 24,
  textAlign: 'center'
};

const resultContentStyle = {
  flex: 1,
  minWidth: 0
};

const resultTitleStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: 8,
  fontWeight: '600',
  fontSize: 14,
  color: 'var(--text)',
  marginBottom: 4
};

const resultTypeStyle = {
  fontSize: 10,
  padding: '2px 6px',
  background: '#e3f2fd',
  color: '#1976d2',
  borderRadius: 8,
  textTransform: 'uppercase',
  fontWeight: '500'
};

const resultDescStyle = {
  fontSize: 12,
  color: 'var(--muted)',
  lineHeight: 1.3
};

const resultCategoryStyle = {
  fontSize: 10,
  color: '#00b4d8',
  fontWeight: '500',
  marginTop: 4
};

const resultArrowStyle = {
  color: 'var(--muted)',
  fontSize: 14
};

const suggestionsStyle = {
  padding: 8
};

const suggestionHeaderStyle = {
  padding: '8px 12px',
  fontSize: 12,
  fontWeight: '600',
  color: 'var(--muted)'
};

const suggestionItemStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: 12,
  padding: '8px 12px',
  cursor: 'pointer',
  borderRadius: 8,
  transition: 'background 0.2s ease'
};

const suggestionIconStyle = {
  fontSize: 16
};

const suggestionTitleStyle = {
  fontSize: 14,
  color: 'var(--text)'
};