# Shanti Neuropsychiatry Centre website

Plain HTML, CSS and JavaScript with **dynamic Google Sheets & Google Drive CMS integration**. No complex framework, zero maintenance database.

## Preview
    python -m http.server 8000      # then open http://localhost:8000

## Dynamic Google Sheets & Google Drive CMS
The website is connected to **Google Sheets** for content editing and **Google Drive** for image assets:
- **Excel CMS Template:** `website-cms-data.xlsx` (in root) and `cms-templates/*.csv` (for 1-click import into Google Sheets).
- **Google Apps Script Code:** `google-apps-script.js` (turnkey backend to read CMS settings and record appointment bookings into the sheet).
- **Setup Guide:** Complete step-by-step instructions in [GOOGLE_SHEETS_AND_DRIVE_GUIDE.md](GOOGLE_SHEETS_AND_DRIVE_GUIDE.md).
- **Google Drive Images:** Paste any public Google Drive image link into the spreadsheet (`doctor_photo_drive_url`, `clinic_logo_drive_url`); the site auto-converts it to high-speed CDN images.
- **Appointments & WhatsApp:** When a patient submits an appointment request:
  1. The entry is recorded automatically in the Google Spreadsheet's `Appointments` tab.
  2. The patient's WhatsApp opens with a pre-filled, formatted message addressed directly to the doctor's phone.

## Folder Structure
- `index.html`, `about/`, `services/`, `service/*`, `appointment/`, `contact/`, `blogs/`, `blog/*`, legal pages, `404.html`
- `assets/` css (`site.css`), js (`site.js`, `cms.js`, `config.js`), images (logo, emblem, favicons, OG image, icon sprite)
- `website-cms-data.xlsx` ready-to-use Excel workbook with 3 clean tabs: `Site_Settings`, `Services`, `Appointments`.
- `cms-templates/` CSV templates for 1-click Google Sheet import.
- `google-apps-script.js` turnkey Google Apps Script for Google Sheets.
- `.env` and `.env.example` configuration files for spreadsheet & WhatsApp connection.
- `tools/build.py` regenerates every page, the sitemap, robots, and redirects (`python tools/build.py`).

## Editing
1. **Dynamic Content:** Edit values in your Google Spreadsheet (`Site_Settings`, `Services`). Changes reflect on the website dynamically!
2. **Static Core Templates:** Edit in `tools/build.py` or `tools/src/home-main.html`, then run `python tools/build.py`.

## Staging vs launch
The shipped files are in **staging mode**: every page has `noindex` and `robots.txt` blocks all crawlers. To go live: set `REVIEWED_BY` once Dr. Singh approves the articles, then run `python tools/build.py --launch`.
