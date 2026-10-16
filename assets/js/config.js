/**
 * =========================================================================
 * CLIENT-SIDE CONFIGURATION FOR SHANTI NEUROPSYCHIATRY CENTRE
 * =========================================================================
 * You can edit the values below directly, OR edit the .env file in the root.
 * This file will also automatically try to load and parse .env if accessible.
 */
(function() {
  window.APP_CONFIG = {
    // 1. Google Apps Script Web App URL (Recommended: Enables both Read CMS + Write Appointments)
    // Replace with your URL ending in /exec after deploying Google Apps Script
    APPS_SCRIPT_URL: 'https://script.google.com/macros/s/AKfycbx_YOUR_APPS_SCRIPT_DEPLOYMENT_ID/exec',

    // 2. Public Google Spreadsheet ID (Fallback: Instant read-only mode via CSV)
    // Example: from https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs/edit
    GOOGLE_SHEET_ID: '',

    // 3. Clinic WhatsApp Number for patient bookings & inquiries (Country code + 10 digits)
    WHATSAPP_NUMBER: '917070474808',

    // 4. Default Clinic Call Numbers
    PHONE_PRIMARY: '+91 70704 74808',
    PHONE_SECONDARY: '+91 99054 00460',

    // 5. Cache TTL in milliseconds (5 minutes = 300000ms; set to 0 for instant live reload)
    CACHE_TTL_MS: 5 * 60 * 1000
  };

  // Attempt to parse root .env if served over HTTP/HTTPS (e.g. localhost, Vercel, Netlify)
  if (window.location.protocol === 'http:' || window.location.protocol === 'https:') {
    fetch('/.env', { cache: 'no-cache' })
      .then(res => res.ok ? res.text() : '')
      .then(text => {
        if (!text) return;
        const lines = text.split('\n');
        lines.forEach(line => {
          const trimmed = line.trim();
          if (!trimmed || trimmed.startsWith('#')) return;
          const eqIdx = trimmed.indexOf('=');
          if (eqIdx === -1) return;
          const k = trimmed.substring(0, eqIdx).trim();
          const v = trimmed.substring(eqIdx + 1).trim().replace(/^["']|["']$/g, '');
          if (k === 'GOOGLE_APPS_SCRIPT_URL' && v && !v.includes('YOUR_APPS_SCRIPT_DEPLOYMENT_ID')) {
            window.APP_CONFIG.APPS_SCRIPT_URL = v;
          } else if (k === 'GOOGLE_SHEET_ID' && v) {
            window.APP_CONFIG.GOOGLE_SHEET_ID = v;
          } else if (k === 'WHATSAPP_NUMBER' && v) {
            window.APP_CONFIG.WHATSAPP_NUMBER = v.replace(/[^0-9]/g, '');
          } else if (k === 'CMS_CACHE_MINUTES' && !isNaN(v)) {
            window.APP_CONFIG.CACHE_TTL_MS = Number(v) * 60 * 1000;
          }
        });
      })
      .catch(() => {
        // Silently continue with window.APP_CONFIG defaults
      });
  }
})();
