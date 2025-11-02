import React, { useState, useEffect } from 'react';

export default function LandingPage({ onNavigate }) {
  const [currentTestimonial, setCurrentTestimonial] = useState(0);

  const features = [
    {
      icon: '🎯',
      title: 'AI-Powered Career Matching',
      description: 'Advanced algorithms analyze your skills, interests, and personality to recommend perfect career paths.'
    },
    {
      icon: '📊',
      title: 'Comprehensive Assessment',
      description: 'Take scientifically-backed assessments including RIASEC personality tests and skills evaluations.'
    },
    {
      icon: '📚',
      title: 'Personalized Learning Paths',
      description: 'Get customized roadmaps with courses, certifications, and milestones for your chosen career.'
    },
    {
      icon: '👨‍🏫',
      title: 'Expert Mentorship',
      description: 'Connect with industry professionals and get one-on-one guidance from experienced mentors.'
    },
    {
      icon: '🏛️',
      title: 'College & Course Finder',
      description: 'Discover the best colleges and courses aligned with your career goals and location preferences.'
    },
    {
      icon: '💬',
      title: '24/7 AI Career Counselor',
      description: 'Get instant answers to career questions with our intelligent chatbot trained on career guidance.'
    }
  ];

  const testimonials = [
    {
      name: 'Priya Sharma',
      role: 'Software Engineer at Google',
      image: '👩‍💻',
      location: 'Bangalore, India',
      quote: 'CareerConnect helped me transition from mechanical engineering to software development. The personalized learning path and mentorship were game-changers!'
    },
    {
      name: 'Rajesh Kumar',
      role: 'Data Scientist at Microsoft',
      image: '👨‍💼',
      location: 'Hyderabad, India',
      quote: 'The AI-powered career recommendations were spot-on! I discovered my passion for data science through their comprehensive assessment.'
    },
    {
      name: 'Anita Patel',
      role: 'UX Designer at Flipkart',
      image: '👩‍🎨',
      location: 'Mumbai, India',
      quote: 'From a confused engineering graduate to a confident UX designer - CareerConnect made my career transformation seamless and exciting.'
    },
    {
      name: 'Arjun Reddy',
      role: 'Product Manager at Zomato',
      image: '👨‍🚀',
      location: 'Delhi, India',
      quote: 'The mentor I connected with through CareerConnect became my career guide. Now I am leading product strategy at a unicorn startup!'
    }
  ];

  const stats = [
    { number: '50,000+', label: 'Students Guided' },
    { number: '150+', label: 'Career Options' },
    { number: '500+', label: 'Industry Mentors' },
    { number: '95%', label: 'Success Rate' }
  ];

  const companies = [
    { name: 'Google', logo: '🔍' },
    { name: 'Microsoft', logo: '💻' },
    { name: 'Amazon', logo: '📦' },
    { name: 'Flipkart', logo: '🛒' },
    { name: 'Zomato', logo: '🍕' },
    { name: 'Paytm', logo: '💳' },
    { name: 'BYJU\'S', logo: '📚' },
    { name: 'Swiggy', logo: '🚚' }
  ];

  // Auto-rotate testimonials
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(interval);
  }, [testimonials.length]);

  return (
    <div style={containerStyle}>
      {/* Hero Section */}
      <section style={heroSectionStyle}>
        <div style={heroContentStyle}>
          <div style={heroTextStyle}>
            <h1 style={heroTitleStyle}>
              Discover Your Perfect Career Path with <span style={brandHighlightStyle}>AI Intelligence</span>
            </h1>
            <p style={heroSubtitleStyle}>
              Join 50,000+ students who found their dream careers through our AI-powered platform. 
              Get personalized recommendations, expert mentorship, and structured learning paths.
            </p>
            <div style={heroButtonsStyle}>
              <button 
                onClick={() => onNavigate('register')} 
                style={primaryButtonStyle}
              >
                🚀 Start Your Journey
              </button>
              <button 
                onClick={() => onNavigate('login')} 
                style={secondaryButtonStyle}
              >
                👤 Sign In
              </button>
            </div>
            
            {/* Quick Stats */}
            <div style={quickStatsStyle}>
              {stats.map((stat, index) => (
                <div key={index} style={statItemStyle}>
                  <div style={statNumberStyle}>{stat.number}</div>
                  <div style={statLabelStyle}>{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
          
          <div style={heroImageStyle}>
            <div style={heroIllustrationStyle}>
              🎯🚀📊💡🌟
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section style={sectionStyle}>
        <div style={sectionHeaderStyle}>
          <h2 style={sectionTitleStyle}>Why Choose CareerConnect?</h2>
          <p style={sectionSubtitleStyle}>
            Everything you need to make the right career decisions
          </p>
        </div>
        
        <div style={featuresGridStyle}>
          {features.map((feature, index) => (
            <div key={index} style={featureCardStyle}>
              <div style={featureIconStyle}>{feature.icon}</div>
              <h3 style={featureTitleStyle}>{feature.title}</h3>
              <p style={featureDescStyle}>{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Companies Section */}
      <section style={companiesSectionStyle}>
        <h3 style={companiesTitleStyle}>Our Alumni Work At</h3>
        <div style={companiesGridStyle}>
          {companies.map((company, index) => (
            <div key={index} style={companyItemStyle}>
              <span style={companyLogoStyle}>{company.logo}</span>
              <span style={companyNameStyle}>{company.name}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Testimonials Section */}
      <section style={testimonialsSectionStyle}>
        <h2 style={sectionTitleStyle}>Success Stories</h2>
        <p style={sectionSubtitleStyle}>Real students, real transformations</p>
        
        <div style={testimonialContainerStyle}>
          <div style={testimonialCardStyle}>
            <div style={testimonialHeaderStyle}>
              <div style={testimonialAvatarStyle}>
                {testimonials[currentTestimonial].image}
              </div>
              <div style={testimonialInfoStyle}>
                <h4 style={testimonialNameStyle}>
                  {testimonials[currentTestimonial].name}
                </h4>
                <p style={testimonialRoleStyle}>
                  {testimonials[currentTestimonial].role}
                </p>
                <p style={testimonialLocationStyle}>
                  📍 {testimonials[currentTestimonial].location}
                </p>
              </div>
            </div>
            <blockquote style={testimonialQuoteStyle}>
              "{testimonials[currentTestimonial].quote}"
            </blockquote>
          </div>
          
          {/* Testimonial Navigation */}
          <div style={testimonialNavStyle}>
            {testimonials.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentTestimonial(index)}
                style={{
                  ...testimonialDotStyle,
                  background: index === currentTestimonial ? '#00b4d8' : '#ddd'
                }}
              />
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section style={ctaSectionStyle}>
        <div style={ctaContentStyle}>
          <h2 style={ctaTitleStyle}>Ready to Transform Your Future?</h2>
          <p style={ctaSubtitleStyle}>
            Join thousands of students who discovered their passion and built successful careers
          </p>
          <button 
            onClick={() => onNavigate('register')} 
            style={ctaButtonStyle}
          >
            🌟 Get Started Free
          </button>
          <p style={ctaNoticeStyle}>
            ✅ No credit card required • ✅ Free assessment • ✅ Instant results
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer style={footerStyle}>
        <div style={footerContentStyle}>
          <div style={footerBrandStyle}>
            <h3 style={footerLogoStyle}>🚀 CareerConnect</h3>
            <p style={footerTaglineStyle}>
              Empowering students to make informed career decisions with AI-powered insights.
            </p>
          </div>
          
          <div style={footerLinksStyle}>
            <div style={footerColumnStyle}>
              <h4 style={footerColumnTitleStyle}>Features</h4>
              <ul style={footerListStyle}>
                <li><button onClick={() => onNavigate('assessment')} style={footerLinkStyle}>Career Assessment</button></li>
                <li><button onClick={() => onNavigate('recommendations')} style={footerLinkStyle}>AI Recommendations</button></li>
                <li><button onClick={() => onNavigate('learning')} style={footerLinkStyle}>Learning Paths</button></li>
                <li><button onClick={() => onNavigate('mentor')} style={footerLinkStyle}>Mentorship</button></li>
              </ul>
            </div>
            
            <div style={footerColumnStyle}>
              <h4 style={footerColumnTitleStyle}>Resources</h4>
              <ul style={footerListStyle}>
                <li><button onClick={() => onNavigate('colleges')} style={footerLinkStyle}>College Finder</button></li>
                <li><button onClick={() => onNavigate('chat')} style={footerLinkStyle}>AI Counselor</button></li>
                <li><button onClick={() => onNavigate('career')} style={footerLinkStyle}>Career Analysis</button></li>
              </ul>
            </div>
          </div>
        </div>
        
        <div style={footerBottomStyle}>
          <p style={footerCopyrightStyle}>
            © 2025 CareerConnect. Built with ❤️ for Indian students.
          </p>
        </div>
      </footer>
    </div>
  );
}

// Styles
const containerStyle = {
  minHeight: '100vh',
  background: 'linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%)'
};

const heroSectionStyle = {
  padding: '120px 24px 80px',
  maxWidth: '1200px',
  margin: '0 auto'
};

const heroContentStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: 60,
  flexWrap: 'wrap'
};

const heroTextStyle = {
  flex: 1,
  minWidth: 300
};

const heroTitleStyle = {
  fontSize: 48,
  fontWeight: 800,
  lineHeight: 1.2,
  marginBottom: 24,
  color: '#062b3c'
};

const brandHighlightStyle = {
  background: 'linear-gradient(45deg, #00b4d8, #0077b6)',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text'
};

const heroSubtitleStyle = {
  fontSize: 18,
  lineHeight: 1.6,
  color: '#6b7785',
  marginBottom: 32,
  maxWidth: 500
};

const heroButtonsStyle = {
  display: 'flex',
  gap: 16,
  marginBottom: 48,
  flexWrap: 'wrap'
};

const primaryButtonStyle = {
  background: 'linear-gradient(45deg, #00b4d8, #0077b6)',
  color: 'white',
  border: 'none',
  padding: '16px 32px',
  borderRadius: 12,
  fontSize: 16,
  fontWeight: 600,
  cursor: 'pointer',
  boxShadow: '0 8px 32px rgba(0, 180, 216, 0.3)',
  transition: 'all 0.3s ease'
};

const secondaryButtonStyle = {
  background: 'transparent',
  color: '#0077b6',
  border: '2px solid #0077b6',
  padding: '14px 32px',
  borderRadius: 12,
  fontSize: 16,
  fontWeight: 600,
  cursor: 'pointer',
  transition: 'all 0.3s ease'
};

const quickStatsStyle = {
  display: 'flex',
  gap: 32,
  flexWrap: 'wrap'
};

const statItemStyle = {
  textAlign: 'center'
};

const statNumberStyle = {
  fontSize: 24,
  fontWeight: 800,
  color: '#00b4d8',
  marginBottom: 4
};

const statLabelStyle = {
  fontSize: 12,
  color: '#6b7785',
  fontWeight: 500
};

const heroImageStyle = {
  flex: 1,
  display: 'flex',
  justifyContent: 'center',
  minWidth: 300
};

const heroIllustrationStyle = {
  fontSize: 120,
  background: 'linear-gradient(45deg, #00b4d8, #0077b6)',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text',
  letterSpacing: 20
};

const sectionStyle = {
  padding: '80px 24px',
  maxWidth: '1200px',
  margin: '0 auto'
};

const sectionHeaderStyle = {
  textAlign: 'center',
  marginBottom: 64
};

const sectionTitleStyle = {
  fontSize: 36,
  fontWeight: 700,
  color: '#062b3c',
  marginBottom: 16
};

const sectionSubtitleStyle = {
  fontSize: 18,
  color: '#6b7785',
  maxWidth: 600,
  margin: '0 auto'
};

const featuresGridStyle = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
  gap: 32
};

const featureCardStyle = {
  background: 'white',
  padding: 32,
  borderRadius: 16,
  textAlign: 'center',
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.08)',
  transition: 'transform 0.3s ease'
};

const featureIconStyle = {
  fontSize: 48,
  marginBottom: 16
};

const featureTitleStyle = {
  fontSize: 20,
  fontWeight: 600,
  color: '#062b3c',
  marginBottom: 12
};

const featureDescStyle = {
  color: '#6b7785',
  lineHeight: 1.6
};

const companiesSectionStyle = {
  padding: '60px 24px',
  background: 'white',
  textAlign: 'center'
};

const companiesTitleStyle = {
  fontSize: 18,
  color: '#6b7785',
  marginBottom: 32,
  fontWeight: 500
};

const companiesGridStyle = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  gap: 40,
  flexWrap: 'wrap',
  maxWidth: '800px',
  margin: '0 auto'
};

const companyItemStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: 8,
  padding: '8px 16px',
  background: '#f8f9fa',
  borderRadius: 8
};

const companyLogoStyle = {
  fontSize: 20
};

const companyNameStyle = {
  fontWeight: 500,
  color: '#062b3c'
};

const testimonialsSectionStyle = {
  padding: '80px 24px',
  background: '#f8f9fa',
  textAlign: 'center'
};

const testimonialContainerStyle = {
  maxWidth: 600,
  margin: '0 auto'
};

const testimonialCardStyle = {
  background: 'white',
  padding: 40,
  borderRadius: 16,
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.08)',
  marginBottom: 32
};

const testimonialHeaderStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: 16,
  marginBottom: 24,
  textAlign: 'left'
};

const testimonialAvatarStyle = {
  fontSize: 48,
  background: 'linear-gradient(45deg, #00b4d8, #0077b6)',
  borderRadius: '50%',
  width: 80,
  height: 80,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center'
};

const testimonialInfoStyle = {
  flex: 1
};

const testimonialNameStyle = {
  fontSize: 18,
  fontWeight: 600,
  color: '#062b3c',
  margin: '0 0 4px 0'
};

const testimonialRoleStyle = {
  fontSize: 14,
  color: '#00b4d8',
  fontWeight: 500,
  margin: '0 0 4px 0'
};

const testimonialLocationStyle = {
  fontSize: 12,
  color: '#6b7785',
  margin: 0
};

const testimonialQuoteStyle = {
  fontSize: 16,
  lineHeight: 1.6,
  color: '#062b3c',
  fontStyle: 'italic',
  margin: 0,
  textAlign: 'left'
};

const testimonialNavStyle = {
  display: 'flex',
  justifyContent: 'center',
  gap: 12
};

const testimonialDotStyle = {
  width: 12,
  height: 12,
  borderRadius: '50%',
  border: 'none',
  cursor: 'pointer',
  transition: 'background 0.3s ease'
};

const ctaSectionStyle = {
  padding: '80px 24px',
  background: 'linear-gradient(45deg, #00b4d8, #0077b6)',
  textAlign: 'center'
};

const ctaContentStyle = {
  maxWidth: 600,
  margin: '0 auto'
};

const ctaTitleStyle = {
  fontSize: 36,
  fontWeight: 700,
  color: 'white',
  marginBottom: 16
};

const ctaSubtitleStyle = {
  fontSize: 18,
  color: 'rgba(255, 255, 255, 0.9)',
  marginBottom: 32,
  lineHeight: 1.6
};

const ctaButtonStyle = {
  background: 'white',
  color: '#0077b6',
  border: 'none',
  padding: '16px 40px',
  borderRadius: 12,
  fontSize: 18,
  fontWeight: 600,
  cursor: 'pointer',
  boxShadow: '0 8px 32px rgba(255, 255, 255, 0.2)',
  transition: 'transform 0.3s ease',
  marginBottom: 16
};

const ctaNoticeStyle = {
  fontSize: 14,
  color: 'rgba(255, 255, 255, 0.8)'
};

const footerStyle = {
  background: '#062b3c',
  color: 'white'
};

const footerContentStyle = {
  maxWidth: '1200px',
  margin: '0 auto',
  padding: '60px 24px 40px',
  display: 'flex',
  gap: 60,
  flexWrap: 'wrap'
};

const footerBrandStyle = {
  flex: 1,
  minWidth: 300
};

const footerLogoStyle = {
  fontSize: 24,
  fontWeight: 700,
  marginBottom: 16
};

const footerTaglineStyle = {
  color: 'rgba(255, 255, 255, 0.8)',
  lineHeight: 1.6,
  maxWidth: 300
};

const footerLinksStyle = {
  display: 'flex',
  gap: 60,
  flexWrap: 'wrap'
};

const footerColumnStyle = {
  minWidth: 150
};

const footerColumnTitleStyle = {
  fontSize: 16,
  fontWeight: 600,
  marginBottom: 16
};

const footerListStyle = {
  listStyle: 'none',
  padding: 0,
  margin: 0
};

const footerLinkStyle = {
  background: 'none',
  border: 'none',
  color: 'rgba(255, 255, 255, 0.8)',
  cursor: 'pointer',
  padding: '4px 0',
  fontSize: 14,
  display: 'block',
  textAlign: 'left',
  marginBottom: 8,
  transition: 'color 0.3s ease'
};

const footerBottomStyle = {
  borderTop: '1px solid rgba(255, 255, 255, 0.1)',
  padding: '20px 24px',
  textAlign: 'center'
};

const footerCopyrightStyle = {
  color: 'rgba(255, 255, 255, 0.6)',
  fontSize: 14,
  margin: 0
};