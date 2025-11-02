import React, { useState, useEffect } from "react";
import { useTranslation } from 'react-i18next';
import GlobalSearchBar from "./GlobalSearchBar";
import Logo from "./Logo";

export default function Navbar({ setPage, onLogout, profile }) {
  const { t, i18n } = useTranslation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [langInfo, setLangInfo] = useState({ flag: '🌐', code: (i18n.language || 'en').split('-')[0] });
  const displayName = profile?.name || profile?.fullName || "Guest";
  // Update language badge when language changes
  useEffect(() => {
    const code = (i18n.language || 'en').split('-')[0];
    // Minimal mapping of code to flag (extendable)
    const flagMap = {
      en: '🇺🇸', hi: '🇮🇳', bn: '🇧🇩', te: '🇮🇳', mr: '🇮🇳', ta: '🇮🇳', gu: '🇮🇳', kn: '🇮🇳', ml: '🇮🇳', pa: '🇮🇳',
      es: '🇪🇸', fr: '🇫🇷', de: '🇩🇪', zh: '🇨🇳', ja: '🇯🇵', ar: '🇸🇦'
    };
    setLangInfo({ flag: flagMap[code] || '🌐', code });
  }, [i18n.language]);

  const navItems = [
    { key: "profile", label: t('navigation.profile'), icon: "👤" },
    { key: "career", label: t('navigation.career'), icon: "📊" },
    { key: "recommendations", label: t('navigation.recommendations'), icon: "🎯" },
    { key: "learning", label: t('navigation.learning'), icon: "📚" },
    { key: "assessment", label: t('navigation.assessment'), icon: "📝" },
    { key: "chat", label: t('navigation.chat'), icon: "💬" },
    { key: "colleges", label: t('navigation.colleges'), icon: "🏛️" },
    { key: "mentor", label: t('navigation.mentor'), icon: "👨‍🏫" }
  ];

  const handleNavigation = (page) => {
    setPage(page);
    setMobileMenuOpen(false);
  };

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  return (
    <>
      <nav className="cc-nav">
        {/* Brand Logo */}
        <div className="nav-brand" onClick={() => handleNavigation("profile")}>
          <Logo variant="full" size="medium" />
        </div>

        {/* Search Bar */}
        <div className="nav-search">
          <GlobalSearchBar onNavigate={handleNavigation} />
        </div>

        {/* Desktop Navigation */}
        <div className="nav-desktop">
          <div className="nav-links">
            {navItems.map((item) => (
              <button
                key={item.key}
                onClick={() => handleNavigation(item.key)}
                className="nav-link"
                title={item.label}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </button>
            ))}
          </div>
          
          <div className="nav-user">
            <div className="nav-lang-badge" title={`Language: ${langInfo.code.toUpperCase()}`}> 
              <span className="nav-lang-flag">{langInfo.flag}</span>
              <span className="nav-lang-code">{langInfo.code.toUpperCase()}</span>
            </div>
            <button onClick={onLogout} className="nav-logout" title={t('navigation.logout')}>
              <span className="nav-icon">🚪</span>
              <span className="nav-label">{t('navigation.logout')}</span>
            </button>
            <div className="profile-avatar" title={displayName}>
              <span>{displayName.charAt(0).toUpperCase()}</span>
            </div>
          </div>
        </div>

        {/* Mobile Hamburger */}
        <div className="nav-mobile">
          <div className="profile-avatar-mobile" title={displayName}>
            <span>{displayName.charAt(0).toUpperCase()}</span>
          </div>
          <button
            className={`hamburger ${mobileMenuOpen ? 'active' : ''}`}
            onClick={toggleMobileMenu}
            aria-label="Toggle menu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </nav>

      {/* Mobile Menu Overlay */}
      <div className={`mobile-menu-overlay ${mobileMenuOpen ? 'active' : ''}`} onClick={toggleMobileMenu}></div>
      
      {/* Mobile Menu */}
      <div className={`mobile-menu ${mobileMenuOpen ? 'active' : ''}`}>
        <div className="mobile-menu-header">
          <div className="mobile-user-info">
            <div className="profile-avatar-large">
              <span>{displayName.charAt(0).toUpperCase()}</span>
            </div>
            <span className="user-name">{displayName}</span>
          </div>
        </div>
        
        <div className="mobile-nav-links">
          {navItems.map((item) => (
            <button
              key={item.key}
              onClick={() => handleNavigation(item.key)}
              className="mobile-nav-link"
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
              <span className="nav-arrow">→</span>
            </button>
          ))}
          
          <button onClick={() => { onLogout(); setMobileMenuOpen(false); }} className="mobile-nav-logout">
            <span className="nav-icon">🚪</span>
            <span className="nav-label">{t('navigation.logout')}</span>
            <div className="nav-arrow">→</div>
          </button>
        </div>
      </div>

      <style>{`
        /* Base Navigation Styles */
        .cc-nav {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          height: 70px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 24px;
          background: linear-gradient(135deg, #0077b6 0%, #00b4d8 50%, #0096c7 100%);
          backdrop-filter: blur(10px);
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          z-index: 1000;
          box-shadow: 0 8px 32px rgba(0, 119, 182, 0.2);
        }

        /* Brand Logo */
        .nav-brand {
          cursor: pointer;
          user-select: none;
        }

        .logo {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .logo-icon {
          font-size: 28px;
          filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.2));
        }

        .logo-text {
          font-size: 24px;
          font-weight: 800;
          background: linear-gradient(45deg, #ffffff, #e6f7ff);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          letter-spacing: -0.5px;
        }

        /* Search Bar */
        .nav-search {
          flex: 1;
          display: flex;
          justify-content: center;
          max-width: 400px;
          margin: 0 24px;
        }

        /* Desktop Navigation */
        .nav-desktop {
          display: flex;
          align-items: center;
          gap: 24px;
        }

        .nav-links {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .nav-link {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 10px 16px;
          background: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 12px;
          color: white;
          font-weight: 600;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          white-space: nowrap;
        }

        .nav-link:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateY(-2px);
          box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }

        .nav-link .nav-icon {
          font-size: 16px;
        }

        .nav-user {
          display: flex;
          align-items: center;
          gap: 16px;
        }

        .nav-logout {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 10px 16px;
          background: rgba(239, 68, 68, 0.9);
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 12px;
          color: white;
          font-weight: 600;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .nav-logout:hover {
          background: rgba(239, 68, 68, 1);
          transform: translateY(-2px);
          box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
        }

        .profile-avatar {
          width: 44px;
          height: 44px;
          border-radius: 50%;
          background: linear-gradient(135deg, #ffffff, #f0f9ff);
          color: #0077b6;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 800;
          font-size: 18px;
          cursor: pointer;
          border: 3px solid rgba(255, 255, 255, 0.3);
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
          transition: all 0.3s ease;
        }

        .nav-lang-badge {
          display: flex;
          align-items: center;
          gap: 6px;
          padding: 6px 10px;
          border-radius: 30px;
          background: rgba(255,255,255,0.15);
          border: 2px solid rgba(255,255,255,0.3);
          backdrop-filter: blur(12px) saturate(160%);
          -webkit-backdrop-filter: blur(12px) saturate(160%);
          color: #fff;
          font-size: 12px;
          font-weight: 600;
          letter-spacing: .5px;
          box-shadow: 0 4px 14px rgba(0,0,0,0.25), inset 0 2px 4px rgba(255,255,255,0.2);
          transition: all .3s ease;
        }

        .nav-lang-badge:hover {
          transform: translateY(-2px);
          background: rgba(255,255,255,0.25);
          box-shadow: 0 8px 26px rgba(0,0,0,0.3), inset 0 3px 6px rgba(255,255,255,0.25);
        }

        .nav-lang-flag { font-size: 16px; }
        .nav-lang-code { font-size: 11px; opacity: .85; }

        .profile-avatar:hover {
          transform: scale(1.1);
          border-color: rgba(255, 255, 255, 0.5);
        }

        /* Mobile Navigation */
        .nav-mobile {
          display: none;
          align-items: center;
          gap: 16px;
        }

        .profile-avatar-mobile {
          width: 36px;
          height: 36px;
          border-radius: 50%;
          background: linear-gradient(135deg, #ffffff, #f0f9ff);
          color: #0077b6;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 800;
          font-size: 16px;
          border: 2px solid rgba(255, 255, 255, 0.3);
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }

        /* Hamburger Menu */
        .hamburger {
          width: 32px;
          height: 32px;
          background: none;
          border: none;
          cursor: pointer;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          gap: 4px;
          padding: 4px;
        }

        .hamburger span {
          width: 24px;
          height: 3px;
          background: white;
          border-radius: 2px;
          transition: all 0.3s ease;
        }

        .hamburger.active span:nth-child(1) {
          transform: rotate(45deg) translate(6px, 6px);
        }

        .hamburger.active span:nth-child(2) {
          opacity: 0;
        }

        .hamburger.active span:nth-child(3) {
          transform: rotate(-45deg) translate(7px, -6px);
        }

        /* Mobile Menu Overlay */
        .mobile-menu-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.5);
          backdrop-filter: blur(4px);
          z-index: 999;
          opacity: 0;
          visibility: hidden;
          transition: all 0.3s ease;
        }

        .mobile-menu-overlay.active {
          opacity: 1;
          visibility: visible;
        }

        /* Mobile Menu */
        .mobile-menu {
          position: fixed;
          top: 0;
          right: 0;
          width: 320px;
          max-width: 85vw;
          height: 100vh;
          background: linear-gradient(180deg, #0077b6 0%, #00b4d8 100%);
          z-index: 1001;
          transform: translateX(100%);
          transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
          overflow-y: auto;
        }

        .mobile-menu.active {
          transform: translateX(0);
        }

        .mobile-menu-header {
          padding: 80px 24px 32px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          background: rgba(255, 255, 255, 0.05);
        }

        .mobile-user-info {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 16px;
        }

        .profile-avatar-large {
          width: 80px;
          height: 80px;
          border-radius: 50%;
          background: linear-gradient(135deg, #ffffff, #f0f9ff);
          color: #0077b6;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 800;
          font-size: 32px;
          border: 4px solid rgba(255, 255, 255, 0.3);
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }

        .user-name {
          color: white;
          font-size: 20px;
          font-weight: 600;
          text-align: center;
        }

        .mobile-nav-links {
          padding: 24px 0;
        }

        .mobile-nav-link,
        .mobile-nav-logout {
          display: flex;
          align-items: center;
          justify-content: space-between;
          width: 100%;
          padding: 18px 24px;
          background: none;
          border: none;
          color: white;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          transition: all 0.3s ease;
        }

        .mobile-nav-link:hover,
        .mobile-nav-logout:hover {
          background: rgba(255, 255, 255, 0.1);
          padding-left: 32px;
        }

        .mobile-nav-logout {
          color: #ffcccb;
          border-top: 2px solid rgba(255, 255, 255, 0.2);
          margin-top: 16px;
        }

        .mobile-nav-logout:hover {
          background: rgba(239, 68, 68, 0.2);
        }

        .nav-arrow {
          font-size: 18px;
          transition: transform 0.3s ease;
        }

        .mobile-nav-link:hover .nav-arrow,
        .mobile-nav-logout:hover .nav-arrow {
          transform: translateX(8px);
        }

        /* Responsive Design */
        @media (max-width: 1200px) {
          .nav-link .nav-label {
            display: none;
          }
          
          .nav-logout .nav-label {
            display: none;
          }
          
          .nav-link,
          .nav-logout {
            padding: 12px;
          }
        }

        @media (max-width: 768px) {
          .cc-nav {
            padding: 0 16px;
          }
          
          .nav-desktop {
            display: none;
          }
          
          .nav-mobile {
            display: flex;
          }
          
          .nav-search {
            display: none;
          }
          
          .logo-text {
            font-size: 20px;
          }
          
          .logo-icon {
            font-size: 24px;
          }
        }

        @media (max-width: 480px) {
          .cc-nav {
            height: 60px;
            padding: 0 12px;
          }
          
          .logo-text {
            font-size: 18px;
          }
          
          .logo-icon {
            font-size: 20px;
          }
          
          .mobile-menu {
            width: 100vw;
            max-width: 100vw;
          }
        }

        /* Smooth animations */
        * {
          box-sizing: border-box;
        }

        button {
          border: none;
          outline: none;
        }

        button:focus {
          outline: 2px solid rgba(255, 255, 255, 0.5);
          outline-offset: 2px;
        }
      `}</style>
    </>
  );
}
