// React-based theme editor
import React from 'react';
import ReactDOM from 'react-dom';

// Theme Editor Component
const ThemeEditor = () => {
  const [themeSettings, setThemeSettings] = React.useState({
    themeName: document.getElementById('id_theme_name').value,
    primaryColor: document.getElementById('id_primary_color').value,
    fontChoice: document.getElementById('id_font_choice').value
  });

  // Update preview when settings change
  React.useEffect(() => {
    updatePreview();
  }, [themeSettings]);

  const updatePreview = () => {
    const previewEl = document.getElementById('theme-preview');
    if (previewEl) {
      previewEl.setAttribute('data-theme', themeSettings.themeName);
      previewEl.style.setProperty('--color-primary', themeSettings.primaryColor);
      
      // Update font family based on selection
      let fontFamily = 'ui-sans-serif, system-ui, -apple-system, sans-serif';
      if (themeSettings.fontChoice === 'serif') {
        fontFamily = 'ui-serif, Georgia, Cambria, serif';
      } else if (themeSettings.fontChoice === 'mono') {
        fontFamily = 'ui-monospace, SFMono-Regular, Menlo, monospace';
      }
      previewEl.style.fontFamily = fontFamily;
    }
  };

  const handleThemeChange = (e) => {
    setThemeSettings({
      ...themeSettings,
      themeName: e.target.value
    });
  };

  const handleColorChange = (e) => {
    setThemeSettings({
      ...themeSettings,
      primaryColor: e.target.value
    });
  };

  const handleFontChange = (e) => {
    setThemeSettings({
      ...themeSettings,
      fontChoice: e.target.value
    });
  };

  // Add event listeners to form fields
  React.useEffect(() => {
    const themeNameEl = document.getElementById('id_theme_name');
    const primaryColorEl = document.getElementById('id_primary_color');
    const fontChoiceEl = document.getElementById('id_font_choice');
    
    if (themeNameEl) themeNameEl.addEventListener('change', handleThemeChange);
    if (primaryColorEl) primaryColorEl.addEventListener('input', handleColorChange);
    if (fontChoiceEl) fontChoiceEl.addEventListener('change', handleFontChange);
    
    return () => {
      if (themeNameEl) themeNameEl.removeEventListener('change', handleThemeChange);
      if (primaryColorEl) primaryColorEl.removeEventListener('input', handleColorChange);
      if (fontChoiceEl) fontChoiceEl.removeEventListener('change', handleFontChange);
    };
  }, []);

  return (
    <div className="theme-editor-preview">
      <h3>Theme Preview</h3>
      <div className="preview-container">
        <p>Your theme preview will appear here</p>
      </div>
    </div>
  );
};

// Initialize React app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  const container = document.getElementById('theme-editor-app');
  if (container) {
    ReactDOM.render(<ThemeEditor />, container);
  }
});