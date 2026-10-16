/**
 * =========================================================================
 * SHANTI NEUROPSYCHIATRY CENTRE - DYNAMIC CMS & GOOGLE SHEETS CONNECTOR
 * =========================================================================
 * - Synchronizes site content from Google Spreadsheet.
 * - Auto-normalizes Google Drive image links to CDN viewable images.
 * - Logs appointment booking requests to the Google Spreadsheet "Appointments" tab.
 * - Opens WhatsApp with pre-filled patient booking message.
 */

(function () {
  'use strict';

  // Helper selectors
  const $ = id => document.getElementById(id);
  const $$ = sel => document.querySelectorAll(sel);

  // Storage key
  const CACHE_KEY = 'snc_cms_data_cache';

  /**
   * Normalize any Google Drive URL or File ID into a direct CDN image URL
   */
  function normalizeDriveUrl(url) {
    if (!url || typeof url !== 'string') return url;
    url = url.trim();
    if (!url) return '';

    // If it's a relative path, data URL, or standard web image URL
    if (url.startsWith('/') || url.startsWith('./') || url.startsWith('../') || url.startsWith('data:')) {
      return url;
    }

    // Check for Google Drive URL formats
    let fileId = null;
    const m1 = url.match(/\/file\/d\/([a-zA-Z0-9_-]+)/);
    const m2 = url.match(/[?&]id=([a-zA-Z0-9_-]+)/);
    const m3 = url.match(/drive\.google\.com\/open\?id=([a-zA-Z0-9_-]+)/);
    // Raw file ID (alphanumeric string between 25-50 characters)
    const m4 = url.match(/^([a-zA-Z0-9_-]{25,50})$/);

    if (m1) fileId = m1[1];
    else if (m2) fileId = m2[1];
    else if (m3) fileId = m3[1];
    else if (m4) fileId = m4[1];

    if (fileId && fileId !== 'YOUR_DOCTOR_PHOTO_ID' && fileId !== 'YOUR_LOGO_ID' && fileId !== 'YOUR_EMBLEM_ID') {
      // High performance Google User Content CDN
      return 'https://lh3.googleusercontent.com/d/' + fileId + '=w1600';
    }

    return url;
  }

  /**
   * Parse CSV string into an array of arrays
   */
  function parseCSV(text) {
    const lines = text.split(/\r?\n/);
    const result = [];
    lines.forEach(line => {
      if (!line.trim()) return;
      const row = [];
      let inQuotes = false;
      let curr = '';
      for (let i = 0; i < line.length; i++) {
        const c = line[i];
        if (c === '"') {
          if (inQuotes && line[i + 1] === '"') {
            curr += '"';
            i++;
          } else {
            inQuotes = !inQuotes;
          }
        } else if (c === ',' && !inQuotes) {
          row.push(curr.trim());
          curr = '';
        } else {
          curr += c;
        }
      }
      row.push(curr.trim());
      result.push(row);
    });
    return result;
  }

  /**
   * Apply CMS values to the DOM elements with [data-cms]
   */
  function applyCmsData(data) {
    if (!data || typeof data !== 'object') return;

    // 1. Process all [data-cms] targets
    $$('[data-cms]').forEach(el => {
      const key = el.getAttribute('data-cms');
      const attr = el.getAttribute('data-cms-attr');
      const val = data[key];

      if (val === undefined || val === null || val === '') return;

      const tagName = el.tagName.toLowerCase();

      // Image Handling
      if (tagName === 'img' || attr === 'src') {
        const normalized = normalizeDriveUrl(val);
        // Avoid dummy placeholder replacement
        if (normalized && !normalized.includes('YOUR_')) {
          const currentSrc = el.getAttribute('src');
          if (currentSrc !== normalized) {
            // Setup fallback if CDN error
            el.onerror = function () {
              const fallbackId = (val.match(/\/file\/d\/([a-zA-Z0-9_-]+)/) || [])[1];
              if (fallbackId && !el.dataset.fallbackTried) {
                el.dataset.fallbackTried = '1';
                el.src = 'https://drive.google.com/thumbnail?id=' + fallbackId + '&sz=w1600';
              }
            };
            el.src = normalized;
          }
        }
        return;
      }

      // Link Attributes
      if (attr === 'href' || tagName === 'a' && attr === 'href') {
        el.href = val;
        return;
      }
      if (attr === 'tel') {
        el.href = 'tel:' + val.replace(/[\s\-()]/g, '');
        el.textContent = val;
        return;
      }
      if (attr === 'mailto') {
        el.href = 'mailto:' + val.trim();
        el.textContent = val.trim();
        return;
      }

      // Standard Text Content
      if (attr === 'html') {
        el.innerHTML = val;
      } else {
        el.textContent = val;
      }
    });

    // 2. Alert Banner handling
    const banner = $('cms-alert-banner');
    if (banner) {
      const active = String(data.banner_alert_active || '').toUpperCase() === 'TRUE';
      const text = data.banner_alert_text || '';
      if (active && text) {
        const textEl = $('cms-alert-text') || banner;
        textEl.textContent = text;
        banner.hidden = false;
        banner.style.display = 'block';
      } else {
        banner.hidden = true;
        banner.style.display = 'none';
      }
    }

    // 3. Update WhatsApp links across site if whatsapp_number is provided
    if (data.whatsapp_number) {
      const cleanWa = String(data.whatsapp_number).replace(/[^0-9]/g, '');
      if (cleanWa) {
        $$('a[href*="wa.me/"]').forEach(a => {
          const u = new URL(a.href);
          const textParam = u.searchParams.get('text') || '';
          a.href = 'https://wa.me/' + cleanWa + (textParam ? '?text=' + encodeURIComponent(textParam) : '');
        });
      }
    }
  }

  /**
   * Fetch CMS data from Google Apps Script or Public Google Sheet CSV
   */
  async function fetchCmsData() {
    const config = window.APP_CONFIG || {};
    const scriptUrl = config.APPS_SCRIPT_URL;
    const sheetId = config.GOOGLE_SHEET_ID;

    // Check if scriptUrl is valid and configured
    if (scriptUrl && !scriptUrl.includes('YOUR_APPS_SCRIPT_DEPLOYMENT_ID')) {
      try {
        const res = await fetch(scriptUrl + '?t=' + Date.now());
        if (res.ok) {
          const json = await res.json();
          if (json && json.status === 'success' && json.settings) {
            localStorage.setItem(CACHE_KEY, JSON.stringify({
              time: Date.now(),
              data: json.settings,
              services: json.services || []
            }));
            applyCmsData(json.settings);
            return;
          }
        }
      } catch (e) {
        console.warn('Apps Script CMS fetch error, trying fallback:', e);
      }
    }

    // Fallback: Read public Google Sheet CSV directly
    if (sheetId && !sheetId.includes('YOUR_GOOGLE_SHEET_ID')) {
      try {
        const csvUrl = 'https://docs.google.com/spreadsheets/d/' + sheetId + '/gviz/tq?tqx=out:csv&sheet=Site_Settings&t=' + Date.now();
        const res = await fetch(csvUrl);
        if (res.ok) {
          const csvText = await res.text();
          const rows = parseCSV(csvText);
          const settings = {};
          // Skip header row
          for (let i = 1; i < rows.length; i++) {
            const k = (rows[i][0] || '').trim();
            const v = (rows[i][1] || '').trim();
            if (k) settings[k] = v;
          }
          localStorage.setItem(CACHE_KEY, JSON.stringify({
            time: Date.now(),
            data: settings
          }));
          applyCmsData(settings);
          return;
        }
      } catch (e) {
        console.warn('Public Google Sheet CSV fetch error:', e);
      }
    }
  }

  /**
   * Initialize CMS hydration with cache-first strategy
   */
  function initCms() {
    // 1. Instant Cache Hydration (zero layout shift)
    try {
      const cached = localStorage.getItem(CACHE_KEY);
      if (cached) {
        const parsed = JSON.parse(cached);
        if (parsed && parsed.data) {
          applyCmsData(parsed.data);
          const config = window.APP_CONFIG || {};
          const ttl = config.CACHE_TTL_MS !== undefined ? config.CACHE_TTL_MS : 300000;
          // If cache is still fresh, we're done
          if (Date.now() - parsed.time < ttl) {
            return;
          }
        }
      }
    } catch (e) {
      // Ignore cache parse error
    }

    // 2. Fetch fresh data from Google Sheets in background
    fetchCmsData();
  }

  /**
   * Enhanced Appointment Booking Form Handler
   * - Records patient data to Google Spreadsheet Appointments tab via Apps Script doPost
   * - Formats WhatsApp message and triggers WhatsApp chat with the clinic
   */
  function setupAppointmentForm() {
    const f = $('req');
    if (!f) return;

    // Check if enhanced handler is already bound
    if (f.dataset.cmsBound) return;
    f.dataset.cmsBound = '1';

    const dt = $('d');
    if (dt) {
      dt.min = new Date().toLocaleDateString('en-CA', { timeZone: 'Asia/Kolkata' });
    }

    function bad(first, id, eid, msg) {
      $(id).setAttribute('aria-invalid', 'true');
      $(eid).textContent = msg;
      return first || id;
    }

    function clear() {
      ['n', 'p', 'd'].forEach(i => {
        if ($(i)) $(i).removeAttribute('aria-invalid');
      });
      ['en', 'ep', 'ed'].forEach(i => {
        if ($(i)) $(i).textContent = '';
      });
    }

    f.addEventListener('submit', async function (e) {
      e.preventDefault();
      clear();

      const name = ($('n').value || '').replace(/\s+/g, ' ').trim();
      const ph = ($('p').value || '').replace(/[\s\-()]/g, '');
      const date = dt ? dt.value : '';
      const sess = $('s') ? $('s').value : 'No preference';
      let first = null;

      if (name.length < 2) {
        first = bad(first, 'n', 'en', 'Enter your name so the clinic knows who to ask for.');
      }
      if (!(/^(?:\+?91|0)?[6-9]\d{9}$/.test(ph) || /^\+\d{8,15}$/.test(ph))) {
        first = bad(first, 'p', 'ep', 'Enter a phone number the clinic can call, for example 7070474808.');
      }
      if (date && dt) {
        const w = new Date(date + 'T00:00:00').getDay();
        if (date < dt.min) {
          first = bad(first, 'd', 'ed', 'Choose today or a later date.');
        } else if (w === 0) {
          first = bad(first, 'd', 'ed', 'No Sunday hours are published. Choose Monday to Saturday.');
        }
      }

      if (first) {
        $(first).focus();
        return;
      }

      // UI Loading state
      const submitBtn = f.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn ? submitBtn.textContent : '';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = '⏳ Recording & preparing WhatsApp...';
      }

      // Current WhatsApp number from config or default
      const config = window.APP_CONFIG || {};
      const waNumber = config.WHATSAPP_NUMBER || '917070474808';

      // 1. WhatsApp formatted message
      const formattedMessage = [
        '🏥 *Appointment Request - Shanti Neuropsychiatry Centre*',
        '━━━━━━━━━━━━━━━━━━━━━',
        '👤 *Patient Name:* ' + name,
        '📞 *Phone Number:* ' + ph,
        '📅 *Preferred Date:* ' + (date || 'Any available day'),
        '⏰ *Preferred Session:* ' + sess,
        '🌐 *Source:* Online Website Request',
        '━━━━━━━━━━━━━━━━━━━━━',
        'Hello Dr. Singh, I would like to request an appointment at Shanti Neuropsychiatry Centre. Please confirm the available time.'
      ].join('\n');

      const waUrl = 'https://wa.me/' + waNumber + '?text=' + encodeURIComponent(formattedMessage);

      // 2. Submit to Google Spreadsheet via Apps Script (Async)
      const scriptUrl = config.APPS_SCRIPT_URL;
      let sheetLogged = false;

      if (scriptUrl && !scriptUrl.includes('YOUR_APPS_SCRIPT_DEPLOYMENT_ID')) {
        try {
          const payload = {
            name: name,
            phone: ph,
            date: date || 'Any Date',
            session: sess,
            source: 'Website Online Form',
            notes: 'Patient booking request via website'
          };

          // Use fetch with text/plain to avoid CORS preflight options
          await fetch(scriptUrl, {
            method: 'POST',
            mode: 'no-cors',
            headers: { 'Content-Type': 'text/plain;charset=utf-8' },
            body: JSON.stringify(payload)
          });
          sheetLogged = true;
        } catch (postErr) {
          console.warn('Could not post to Google Sheet:', postErr);
        }
      }

      // Restore submit button
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText || 'Prepare my request';
      }

      // 3. Display Confirmation & WhatsApp Trigger UI
      const r = $('result');
      if (r) {
        // Build reassuring confirmation notice
        let statusBadge = $('booking-sheet-status');
        if (!statusBadge) {
          statusBadge = document.createElement('div');
          statusBadge.id = 'booking-sheet-status';
          statusBadge.className = 'cms-success-badge';
          r.insertBefore(statusBadge, r.firstChild);
        }

        if (sheetLogged) {
          statusBadge.innerHTML = '<strong>✓ Logged in Clinic Spreadsheet:</strong> Your appointment request details have been saved to the clinic database. Now send directly on WhatsApp below to confirm.';
          statusBadge.style.display = 'block';
        } else {
          statusBadge.innerHTML = '<strong>Ready to Send:</strong> Send this pre-filled message directly to Dr. Singh on WhatsApp to finalize your visit time.';
          statusBadge.style.display = 'block';
        }

        if ($('msg')) $('msg').textContent = formattedMessage;
        if ($('wa')) {
          $('wa').href = waUrl;
          $('wa').textContent = 'Open WhatsApp & Send Message';
        }
        if ($('cpn')) $('cpn').textContent = '';

        r.hidden = false;
        r.focus();
        r.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        // Optionally open WhatsApp in a new tab directly
        try {
          window.open(waUrl, '_blank', 'noopener');
        } catch (popupErr) {
          // If popup blocked, the user clicks the prominent 'Open WhatsApp' button
        }
      }
    });

    // Copy message button handler
    const cpBtn = $('cp');
    if (cpBtn && !cpBtn.dataset.bound) {
      cpBtn.dataset.bound = '1';
      cpBtn.addEventListener('click', function () {
        const m = $('msg') ? $('msg').textContent : '';
        const n = $('cpn');
        if (!m || !n) return;
        (navigator.clipboard ? navigator.clipboard.writeText(m) : Promise.reject())
          .then(
            () => { n.textContent = 'Message copied to clipboard.'; },
            () => { n.textContent = 'Copying was blocked. Please select the text above and copy manually.'; }
          );
      });
    }
  }

  // Self-execute when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initCms();
      setupAppointmentForm();
    });
  } else {
    initCms();
    setupAppointmentForm();
  }

  // Expose global for manual refresh / testing
  window.refreshCmsData = function () {
    localStorage.removeItem(CACHE_KEY);
    fetchCmsData();
  };
})();
