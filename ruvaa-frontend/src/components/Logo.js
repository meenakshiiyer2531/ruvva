import React from 'react';

export default function Logo({ size = 'medium', variant = 'full', className = '' }) {
  const sizes = {
    small: { width: 32, height: 32, fontSize: 16 },
    medium: { width: 48, height: 48, fontSize: 20 },
    large: { width: 64, height: 64, fontSize: 24 },
    xlarge: { width: 96, height: 96, fontSize: 32 }
  };

  const currentSize = sizes[size] || sizes.medium;

  if (variant === 'icon') {
    return (
      <div 
        className={`cc-logo-icon ${className}`}
        style={{
          width: currentSize.width,
          height: currentSize.height,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          borderRadius: '12px',
          background: 'linear-gradient(135deg, var(--cc-primary-500), var(--cc-primary-600))',
          boxShadow: 'var(--cc-shadow-md)',
          transition: 'all var(--cc-transition)'
        }}
      >
        <img 
          src="/logo192.png" 
          alt="CareerConnect" 
          style={{ 
            width: currentSize.width * 0.7, 
            height: currentSize.height * 0.7,
            filter: 'brightness(0) invert(1)'
          }}
          onError={(e) => {
            // Fallback to emoji if image fails to load
            e.target.style.display = 'none';
            e.target.parentNode.innerHTML = '🚀';
            e.target.parentNode.style.fontSize = `${currentSize.fontSize}px`;
            e.target.parentNode.style.color = 'white';
          }}
        />
      </div>
    );
  }

  return (
    <div 
      className={`cc-logo-full ${className}`}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--cc-space-3)',
        cursor: 'pointer',
        transition: 'all var(--cc-transition)'
      }}
    >
      <div 
        className="cc-logo-icon"
        style={{
          width: currentSize.width,
          height: currentSize.height,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          borderRadius: '12px',
          background: 'linear-gradient(135deg, var(--cc-primary-500), var(--cc-primary-600))',
          boxShadow: 'var(--cc-shadow-md)',
          transition: 'all var(--cc-transition)'
        }}
      >
        <img 
          src="/logo192.png" 
          alt="CareerConnect" 
          style={{ 
            width: currentSize.width * 0.7, 
            height: currentSize.height * 0.7,
            filter: 'brightness(0) invert(1)'
          }}
          onError={(e) => {
            // Fallback to emoji if image fails to load
            e.target.style.display = 'none';
            e.target.parentNode.innerHTML = '🚀';
            e.target.parentNode.style.fontSize = `${currentSize.fontSize}px`;
            e.target.parentNode.style.color = 'white';
          }}
        />
      </div>
      
      {variant === 'full' && (
        <div className="cc-logo-text">
          <h1 
            style={{
              fontSize: `${currentSize.fontSize}px`,
              fontWeight: 800,
              background: 'linear-gradient(135deg, var(--cc-primary-500), var(--cc-primary-700))',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
              letterSpacing: '-0.02em',
              lineHeight: 1,
              margin: 0
            }}
          >
            CareerConnect
          </h1>
          {size === 'large' || size === 'xlarge' ? (
            <p 
              style={{
                fontSize: `${currentSize.fontSize * 0.4}px`,
                color: 'var(--text-muted)',
                fontWeight: 500,
                margin: 0,
                letterSpacing: '0.1em',
                textTransform: 'uppercase'
              }}
            >
              AI-Powered Career Guidance
            </p>
          ) : null}
        </div>
      )}
    </div>
  );
}

export const LogoIcon = (props) => <Logo {...props} variant="icon" />;
export const LogoFull = (props) => <Logo {...props} variant="full" />;