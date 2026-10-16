# Google Sheets & Google Drive Dynamic Website Guide
**Shanti Neuropsychiatry Centre — Dynamic CMS & Appointment System**

This website is equipped with a **zero-code, dynamic CMS system** powered by **Google Sheets** and **Google Drive**. Anyone from the clinic team can change content, update photos, post announcement banners, and view appointment requests without writing code or editing files.

---

## Table of Contents
1. [Overview & Files Provided](#1-overview--files-provided)
2. [Step 1: Setting Up the Google Spreadsheet](#2-step-1-setting-up-the-google-spreadsheet)
3. [Step 2: Linking Google Drive Images & Assets](#3-step-2-linking-google-drive-images--assets)
4. [Step 3: Deploying Google Apps Script (2 Minutes)](#4-step-3-deploying-google-apps-script-2-minutes)
5. [Step 4: Connecting the Website (.env & config.js)](#5-step-4-connecting-the-website-env--configjs)
6. [Alternative: Read-Only Mode (Zero Apps Script)](#6-alternative-read-only-mode-zero-apps-script)
7. [How Appointment Bookings & WhatsApp Work](#7-how-appointment-bookings--whatsapp-work)
8. [Spreadsheet Parameters Reference](#8-spreadsheet-parameters-reference)

---

## 1. Overview & Files Provided

The following files are included in the website repository/zip file:

| File | Purpose |
| :--- | :--- |
| **`website-cms-data.xlsx`** | Ready-to-use formatted Excel file with all variables and sample data. |
| **`cms-templates/`** | Individual CSV files (`Site_Settings.csv`, `Services.csv`, `Appointments.csv`) for 1-click import into Google Sheets. |
| **`google-apps-script.js`** | Apps Script code to paste into Google Sheets for reading settings & recording appointment bookings. |
| **`.env` & `.env.example`** | Environment file where you configure your Google Apps Script URL & WhatsApp number. |
| **`assets/js/config.js`** | Client configuration file linking the site to your spreadsheet. |
| **`assets/js/cms.js`** | Automatic hydration script: updates text, converts Google Drive links, and syncs appointment submissions. |

---

## 2. Step 1: Setting Up the Google Spreadsheet

### Option A: Uploading the Excel file directly (Recommended)
1. Go to [Google Drive](https://drive.google.com).
2. Click **New (+)** > **File upload**.
3. Select the file **`website-cms-data.xlsx`** from this website folder.
4. Double-click the uploaded file in Google Drive and select **Open with Google Sheets**.
5. Go to **File** > **Save as Google Sheets**.
6. At the top right, click **Share**:
   - Under *General access*, change from "Restricted" to **"Anyone with the link"** with role **Viewer**.
   - Click **Done**.

### Option B: Importing the CSV into an existing sheet
1. Create a blank Google Sheet.
2. Click **File** > **Import** > **Upload**.
3. Select `cms-templates/Site_Settings.csv` and choose **Replace current sheet**.
4. Repeat for `Services.csv` and `Appointments.csv` as new sheets/tabs.

---

## 3. Step 2: Linking Google Drive Images & Assets

You can use Google Drive as your image CDN for the doctor's photo, clinic logo, or emblem.

### How to add an image from Google Drive:
1. Upload your photo (e.g. `doctor-photo.jpg` or `clinic-logo.png`) to Google Drive.
2. Right-click the uploaded image in Google Drive and click **Share** > **Share**.
3. Under **General access**, change from "Restricted" to **"Anyone with the link"**.
4. Click **Copy link** (e.g. `https://drive.google.com/file/d/1A2B3C4D5E6F.../view?usp=sharing`).
5. Open your Google Spreadsheet, navigate to the **`Site_Settings`** sheet.
6. Paste this link into the `Value` column for:
   - `doctor_photo_drive_url` (for the doctor's picture)
   - `clinic_logo_drive_url` (for the clinic logo in footer)
   - `clinic_emblem_drive_url` (for header emblem)

> **Automatic URL Conversion:**  
> Normally, Google Drive sharing links do not display in standard `<img>` tags because they link to an HTML preview page.  
> **Our website contains a built-in normalizer (`normalizeDriveUrl`)** that automatically detects any Google Drive sharing link, extracts the file ID, and converts it instantly to Google's high-speed CDN direct image format (`https://lh3.googleusercontent.com/d/{FILE_ID}=w1600`).  
> **You can paste ANY Google Drive link format directly without manual formatting!**

---

## 4. Step 3: Deploying Google Apps Script (2 Minutes)

Google Apps Script gives your Google Spreadsheet an API endpoint so the website can:
1. Read the latest information instantly.
2. Record patient appointment requests into the **`Appointments`** sheet.

### Step-by-Step Instructions:
1. In your Google Sheet, click **Extensions** in the top navigation bar, then click **Apps Script**.
2. Delete any existing code inside the editor (`function myFunction() { ... }`).
3. Open the file **`google-apps-script.js`** from this website, copy its entire contents, and paste it into the Apps Script editor.
4. Click the **Save** icon (floppy disk) or press `Ctrl + S`.
5. *(Optional but recommended)* In the toolbar dropdown next to "Debug", select **`setupInitialSheets`** and click **Run**:
   - A dialog titled "Authorization required" will appear.
   - Click **Review permissions** > Select your Google Account.
   - Click **Advanced** > Click **Go to Untitled project (unsafe)** > Click **Allow**.
   - This automatically creates and styles any missing tabs and headers!
6. In the top right, click the blue **Deploy** button > **New deployment**.
7. Next to "Select type", click the **Gear icon (⚙)** and select **Web app**.
8. Set the following fields:
   - **Description**: `Website CMS & Booking API`
   - **Execute as**: `Me (your email)`
   - **Who has access**: **`Anyone`** *(CRITICAL: Must be "Anyone" so visitors can send appointment requests and read CMS data without logging into Google).*
9. Click **Deploy**.
10. Copy the **Web app URL** (it ends with `/exec`).  
    *Example: `https://script.google.com/macros/s/AKfycbw.../exec`*

---

## 5. Step 4: Connecting the Website (.env & config.js)

Once you have your **Web app URL**:

### 1. In `.env`:
Open the `.env` file in the website root directory and paste your URL:
```env
GOOGLE_APPS_SCRIPT_URL=https://script.google.com/macros/s/YOUR_APPS_SCRIPT_ID/exec
WHATSAPP_NUMBER=917070474808
```

### 2. In `assets/js/config.js`:
Open `assets/js/config.js` and set your URL:
```javascript
window.APP_CONFIG = {
  APPS_SCRIPT_URL: 'https://script.google.com/macros/s/YOUR_APPS_SCRIPT_ID/exec',
  GOOGLE_SHEET_ID: '',
  WHATSAPP_NUMBER: '917070474808',
  CACHE_TTL_MS: 5 * 60 * 1000 // 5 minutes cache
};
```

---

## 6. Alternative: Read-Only Mode (Zero Apps Script)

If you only want to read content from Google Sheets without setting up Google Apps Script:
1. In Google Sheets, click **Share** > set to **"Anyone with the link can view"**.
2. Copy your Sheet ID from the browser URL:
   `https://docs.google.com/spreadsheets/d/`**`1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs`**`/edit`
3. Paste the Sheet ID into `.env` and `assets/js/config.js`:
   ```javascript
   GOOGLE_SHEET_ID: '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs'
   ```
The website will parse the public sheet directly via CSV!

---

## 7. How Appointment Bookings & WhatsApp Work

When a patient visits the website and submits the **Request an Appointment** form:

```
[Patient Fills Form: Name, Phone, Date, Session]
                      │
                      ▼
       [Patient Clicks "Prepare My Request"]
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
[1. Google Spreadsheet]     [2. WhatsApp Direct Entry]
Row added to "Appointments"   Pre-filled WhatsApp message opens
tab with IST timestamp &      directly addressed to the clinic's
status: "New Request"         number: wa.me/917070474808
```

### Pre-filled WhatsApp Notification Format:
```text
🏥 *Appointment Request - Shanti Neuropsychiatry Centre*
━━━━━━━━━━━━━━━━━━━━━
👤 *Patient Name:* Rohan Sharma
📞 *Phone Number:* 9876543210
📅 *Preferred Date:* 2026-10-20
⏰ *Preferred Session:* Morning, 9:00 am to 12:00 pm
🌐 *Source:* Online Website Request
━━━━━━━━━━━━━━━━━━━━━
Hello Dr. Singh, I would like to request an appointment at Shanti Neuropsychiatry Centre. Please confirm the available time.
```

- **Doctor Benefits:**
  - You receive an **instant WhatsApp notification** directly on your phone from the patient.
  - You also have a **central permanent log** of all requests in the Google Spreadsheet `Appointments` tab.
- **Fail-Safe Reliability:**
  - Even if the patient's internet drops or Apps Script is being updated, the WhatsApp connection **always works seamlessly** so no patient booking is ever lost!

---

## 8. Spreadsheet Parameters Reference

The `Site_Settings` sheet contains simple **Key** and **Value** columns for the essential parameters:

| Parameter Key | Purpose | Example Value |
| :--- | :--- | :--- |
| `doctor_name` | Name displayed in header, bio, and footer | `Dr. Sachchidanand Singh` |
| `doctor_title` | Professional title | `Consultant Psychiatrist` |
| `doctor_qualifications` | Medical training degrees | `MBBS (PMCH), MD Psychiatry (CIP Ranchi)` |
| `clinic_name` | Official centre name | `Shanti Neuropsychiatry Centre` |
| `phone_primary` | Primary calling number | `+91 70704 74808` |
| `phone_secondary` | Alternate calling number | `+91 99054 00460` |
| `whatsapp_number` | WhatsApp number for chat & bookings | `917070474808` *(country code + number, no +)* |
| `clinic_email` | Patient query email | `shantineuropsychiatry@gmail.com` |
| `clinic_address` | Physical location | `G-37, Rajni Path, in front of Savera Cancer Hospital, PC Colony, Kankarbagh, Patna 800020` |
| `clinic_hours_text` | Working hours display | `Monday to Saturday: 9:00 am – 12:00 pm, 3:00 pm – 7:00 pm` |
| `google_maps_url` | Directions link | `https://www.google.com/maps/search/?api=1&query=Shanti+Neuropsychiatry+Centre+Kankarbagh+Patna` |
| `hero_title` | Homepage main headline | `A calm first conversation with a psychiatrist in Patna` |
| `hero_lead` | Homepage lead paragraph | `Dr. Sachchidanand Singh sees patients at Shanti Neuropsychiatry Centre in Kankarbagh...` |
| `about_doctor_summary` | Summary bio of Dr. Singh | `Dr. Sachchidanand Singh is a consultant psychiatrist in Patna...` |
| `banner_alert_active` | Top announcement bar switch | **`TRUE`** or **`FALSE`** |
| `banner_alert_text` | Announcement bar message | `Clinic is open on Saturdays. Walk-in and WhatsApp requests welcome.` |
| `doctor_photo_drive_url`| Doctor portrait photo | Google Drive share link |
| `clinic_logo_drive_url` | Clinic logo in footer | Google Drive share link |
| `clinic_emblem_drive_url`| Brand emblem in header | Google Drive share link |
| `youtube_url` | YouTube channel link | `https://www.youtube.com/@drsachchidanandsingh` |
| `facebook_url` | Facebook profile link | `https://www.facebook.com/sachchidanand.singh.5` |
| `instagram_url` | Instagram profile link | `https://instagram.com/drsachchi` |

---

## 9. Testing & Cache Refreshing

1. When you edit values in your Google Spreadsheet, they update dynamically.
2. The browser caches content for 5 minutes (`CACHE_TTL_MS`) to make the website load instantaneously.
3. To immediately see updates during testing:
   - In browser developer console (`F12`), run: `window.refreshCmsData()` OR
   - Open the site in an **Incognito / Private tab**, OR
   - Set `CACHE_TTL_MS: 0` in `assets/js/config.js` while making frequent edits.
