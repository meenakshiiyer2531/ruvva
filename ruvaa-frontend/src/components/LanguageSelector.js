import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { getLanguageFromLocation } from '../i18n';

const LANGUAGES = [
  { code: 'en', name: 'English', flag: '🇺🇸', region: 'Global' },
  { code: 'hi', name: 'हिन्दी', flag: '🇮🇳', region: 'India' },
  { code: 'bn', name: 'বাংলা', flag: '🇧🇩', region: 'India' },
  { code: 'te', name: 'తెలుగు', flag: '🇮🇳', region: 'India' },
  { code: 'mr', name: 'मराठी', flag: '🇮🇳', region: 'India' },
  { code: 'ta', name: 'தமிழ்', flag: '🇮🇳', region: 'India' },
  { code: 'gu', name: 'ગુજરાતી', flag: '🇮🇳', region: 'India' },
  { code: 'kn', name: 'ಕನ್ನಡ', flag: '🇮🇳', region: 'India' },
  { code: 'ml', name: 'മലയാളം', flag: '🇮🇳', region: 'India' },
  { code: 'pa', name: 'ਪੰਜਾਬੀ', flag: '🇮🇳', region: 'India' },
  { code: 'es', name: 'Español', flag: '🇪🇸', region: 'Europe' },
  { code: 'fr', name: 'Français', flag: '🇫🇷', region: 'Europe' },
  { code: 'de', name: 'Deutsch', flag: '🇩🇪', region: 'Europe' },
  { code: 'zh', name: '中文', flag: '🇨🇳', region: 'Asia' },
  { code: 'ja', name: '日本語', flag: '🇯🇵', region: 'Asia' },
  { code: 'ar', name: 'العربية', flag: '🇸🇦', region: 'Middle East' }
];

export default function LanguageSelector({ className = '' }) {
  const { i18n, t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [isAutoDetect, setIsAutoDetect] = useState(!localStorage.getItem('cc_language_manual'));
  const [activeCode, setActiveCode] = useState(() => (i18n.language || 'en').split('-')[0]);
  const [search, setSearch] = useState('');
  const [expandedRegions, setExpandedRegions] = useState(() => new Set());

  // Update activeCode when i18n language changes
  useEffect(() => {
    const normalized = (i18n.language || 'en').split('-')[0];
    setActiveCode(normalized);
  }, [i18n.language]);

  const currentLanguage = LANGUAGES.find(lang => lang.code === activeCode) || LANGUAGES[0];

  // Group languages by region
  const grouped = LANGUAGES
    .filter(l => l.name.toLowerCase().includes(search.toLowerCase()) || l.code.toLowerCase().includes(search.toLowerCase()))
    .reduce((acc, lang) => {
      acc[lang.region] = acc[lang.region] || [];
      acc[lang.region].push(lang);
      return acc;
    }, {});

  const toggleRegion = (region) => {
    setExpandedRegions(prev => {
      const next = new Set(prev);
      if (next.has(region)) next.delete(region); else next.add(region);
      return next;
    });
  };

  const closeDropdown = useCallback(() => setIsOpen(false), []);

  const handleLanguageChange = useCallback((languageCode) => {
    i18n.changeLanguage(languageCode);
    localStorage.setItem('cc_language_manual', 'true');
    setIsAutoDetect(false);
    setActiveCode(languageCode);
    closeDropdown();
  }, [i18n, closeDropdown]);

  const handleAutoDetect = useCallback(() => {
    const detectedLang = getLanguageFromLocation();
    i18n.changeLanguage(detectedLang);
    localStorage.removeItem('cc_language_manual');
    setIsAutoDetect(true);
    setActiveCode(detectedLang.split('-')[0]);
    closeDropdown();
  }, [i18n, closeDropdown]);

  const toggleDropdown = useCallback(() => setIsOpen(o => !o), []);

  // Close on Esc
  useEffect(() => {
    const handler = (e) => { if (e.key === 'Escape') closeDropdown(); };
    if (isOpen) window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [isOpen, closeDropdown]);

  // Prevent scroll bleed when open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  }, [isOpen]);

  return (
    <>
      <button
        type="button"
        className="cc-language-trigger"
        onClick={toggleDropdown}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        aria-label={t('language.change', 'Change language')}
        style={triggerIconStyle}
        title={`${currentLanguage.name} (${currentLanguage.code.toUpperCase()})`}
      >
        <span style={iconGlobeStyle}>🌐</span>
        <span style={currentBadgeStyle}>{currentLanguage.flag}</span>
      </button>
      
      {isOpen && (
        <>
          <div 
            style={backdropStyle}
            onClick={closeDropdown}
          />
          
          <div className="cc-language-dropdown" style={dropdownStyle} role="listbox">
            <div style={dropdownHeaderStyle}>{t('language.select', 'Select Language')}</div>
            <div style={searchWrapperStyle}>
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder={t('language.search', 'Search language...')}
                style={searchInputStyle}
                aria-label={t('language.search', 'Search language...')}
              />
            </div>
            
            {/* AUTO-DETECT OPTION */}
            <button 
              type="button"
              onClick={handleAutoDetect}
              style={{
                ...optionStyle,
                background: isAutoDetect ? 'linear-gradient(90deg, rgba(34,197,94,0.25), rgba(16,185,129,0.20))' : 'transparent'
              }}
              className="cc-language-option"
              role="option"
              aria-selected={isAutoDetect}
            >
              <span style={iconGlobeStyle}>🌐</span>
              <div style={optionTextWrapperStyle}>
                <div style={optionTitleStyle}>{t('language.auto', 'Auto-detect')}</div>
                <div style={optionSubtitleStyle}>{t('language.auto.desc', 'Based on location')}</div>
              </div>
              {isAutoDetect && <span style={checkmarkStyle}>✓</span>}
            </button>

            {/* LANGUAGE OPTIONS */}
            {Object.keys(grouped).map(region => {
              const open = expandedRegions.has(region);
              return (
                <div key={region} style={regionBlockStyle}>
                  <button
                    type="button"
                    onClick={() => toggleRegion(region)}
                    style={{ ...regionHeaderStyle, background: open ? 'rgba(255,255,255,0.06)' : 'transparent' }}
                    aria-expanded={open}
                  >
                    <span style={regionChevronStyle}>{open ? '▾' : '▸'}</span>
                    <span style={regionTitleStyle}>{region}</span>
                    <span style={regionCountStyle}>{grouped[region].length}</span>
                  </button>
                  {open && (
                    <div style={regionLanguagesWrapperStyle}>
                      {grouped[region].map(language => {
                        const selected = !isAutoDetect && activeCode === language.code;
                        return (
                          <button
                            key={language.code}
                            type="button"
                            onClick={() => handleLanguageChange(language.code)}
                            style={{
                              ...optionStyle,
                              background: selected ? 'linear-gradient(90deg, rgba(34,197,94,0.25), rgba(16,185,129,0.18))' : 'transparent'
                            }}
                            className="cc-language-option"
                            role="option"
                            aria-selected={selected}
                          >
                            <span style={badgeWrapperStyle}>
                              <span style={badgeStyle}>{language.flag}</span>
                            </span>
                            <div style={optionTextWrapperStyle}>
                              <div style={optionTitleStyle}>{language.name}</div>
                              <div style={optionSubtitleStyle}>{language.code.toUpperCase()}</div>
                            </div>
                            {selected && <span style={checkmarkStyle}>✓</span>}
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </>
      )}
    </>
  );
}

// Styling objects
const triggerIconStyle = {
  display: 'flex', alignItems: 'center', gap: 6, padding: '8px 12px',
  background: 'linear-gradient(145deg, rgba(255,255,255,0.30), rgba(255,255,255,0.12))',
  border: 'none', borderRadius: 50, color: '#fff',
  fontWeight: 600, fontSize: 13, cursor: 'pointer', backdropFilter: 'blur(18px) saturate(170%)',
  boxShadow: '0 8px 24px rgba(0,0,0,0.25), inset 0 2px 4px rgba(255,255,255,0.25)',
  transition: 'all .35s cubic-bezier(.4,0,.2,1)'
};
const iconGlobeStyle = { fontSize: 16, filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.3))' };
const currentBadgeStyle = {
  width: 28, height: 28, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
  background: 'linear-gradient(145deg, rgba(255,255,255,0.25), rgba(0,0,0,0.15))', fontSize: 16,
  boxShadow: 'inset 0 2px 4px rgba(255,255,255,0.25), 0 4px 10px rgba(0,0,0,0.35)'
};
const backdropStyle = { position: 'fixed', inset: 0, zIndex: 1400 };
const dropdownStyle = {
  position: 'absolute', top: 'calc(100% + 10px)', right: 0, minWidth: 260,
  background: 'linear-gradient(145deg, rgba(18,18,18,0.95), rgba(30,30,30,0.92))',
  border: 'none', borderRadius: 22, padding: '4px 0 8px',
  boxShadow: '0 25px 60px rgba(0,0,0,0.6), 0 0 35px rgba(34,197,94,0.25)',
  backdropFilter: 'blur(28px) saturate(180%)', WebkitBackdropFilter: 'blur(28px) saturate(180%)',
  zIndex: 1500, animation: 'fadeSlide .35s cubic-bezier(.4,0,.2,1)'
};
const dropdownHeaderStyle = {
  padding: '14px 20px', fontWeight: 700, fontSize: 15, color: '#fff', textAlign: 'center',
  borderBottom: '1px solid rgba(255,255,255,0.08)', letterSpacing: '.5px'
};
const searchWrapperStyle = { padding: '10px 16px', borderBottom: '1px solid rgba(255,255,255,0.06)' };
const searchInputStyle = {
  width: '100%', padding: '10px 14px', borderRadius: 12, border: '1px solid rgba(255,255,255,0.25)',
  background: 'rgba(255,255,255,0.12)', color: '#fff', fontSize: 14, outline: 'none',
  backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)',
};
const optionStyle = {
  display: 'flex', alignItems: 'center', gap: 14, width: '100%', padding: '12px 18px',
  border: 'none', background: 'transparent', cursor: 'pointer', color: '#fff', textAlign: 'left',
  fontSize: 14, fontWeight: 600, position: 'relative', transition: 'background .25s, transform .25s'
};
const optionTextWrapperStyle = { flex: 1, display: 'flex', flexDirection: 'column' };
const optionTitleStyle = { fontWeight: 700, fontSize: 14 };
const optionSubtitleStyle = { fontSize: 11, opacity: 0.65, letterSpacing: '.5px' };
const checkmarkStyle = { color: '#22c55e', fontWeight: 700 };
const badgeWrapperStyle = { display: 'flex', alignItems: 'center', justifyContent: 'center' };
const badgeStyle = {
  width: 34, height: 34, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
  fontSize: 18, background: 'linear-gradient(145deg, rgba(255,255,255,0.15), rgba(0,0,0,0.15))',
  boxShadow: 'inset 0 2px 4px rgba(255,255,255,0.2), 0 4px 12px rgba(0,0,0,0.3)'
};
const regionBlockStyle = { padding: '4px 0' };
const regionHeaderStyle = {
  width: '100%', textAlign: 'left', border: 'none', cursor: 'pointer', color: '#fff', fontSize: 13,
  fontWeight: 600, padding: '8px 16px', display: 'flex', alignItems: 'center', gap: 8, transition: 'background .25s'
};
const regionChevronStyle = { fontSize: 12, opacity: 0.8 };
const regionTitleStyle = { flex: 1, letterSpacing: '.5px' };
const regionCountStyle = { fontSize: 11, background: 'rgba(255,255,255,0.15)', padding: '2px 6px', borderRadius: 12 };
const regionLanguagesWrapperStyle = { padding: '4px 4px 0 4px' };

// Hover effects via inline style injection (optional minimal CSS)
// We can add a style tag here for keyframes & button hover
if (typeof document !== 'undefined') {
  const existing = document.getElementById('cc-language-inline-style');
  if (!existing) {
    const styleEl = document.createElement('style');
    styleEl.id = 'cc-language-inline-style';
    styleEl.textContent = `@keyframes fadeSlide{0%{opacity:0;transform:translateY(-12px) scale(.95)}100%{opacity:1;transform:translateY(0) scale(1)}}
      .cc-language-option:hover{background:rgba(255,255,255,0.06);}
      .cc-language-trigger:hover{transform:translateY(-2px);box-shadow:0 15px 40px rgba(0,0,0,.35), inset 0 3px 6px rgba(255,255,255,.25);}`;
    document.head.appendChild(styleEl);
  }
}