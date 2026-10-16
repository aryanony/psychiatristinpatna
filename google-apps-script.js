/**
 * =========================================================================
 * GOOGLE APPS SCRIPT: SHANTI NEUROPSYCHIATRY WEBSITE BACKEND & CMS
 * =========================================================================
 * This script connects your Google Spreadsheet to the website.
 * 
 * FEATURES:
 * 1. Read CMS Settings & Services via doGet (JSON API).
 * 2. Record Patient Appointment Requests via doPost into the "Appointments" tab.
 * 3. Supports direct Google Drive Image links & instant live updates.
 * 
 * -------------------------------------------------------------------------
 * QUICK 1-MINUTE SETUP INSTRUCTIONS:
 * -------------------------------------------------------------------------
 * 1. Open Google Sheets (https://sheets.google.com) and create a new sheet.
 *    (Or upload the provided "website-cms-data.xlsx" directly).
 * 2. In Google Sheets top menu, click: Extensions -> Apps Script.
 * 3. Delete any code in the editor, and paste ALL of this code.
 * 4. At the top toolbar, select function "setupInitialSheets" and click "Run".
 *    (Click "Review Permissions" -> Choose your Google Account -> "Advanced" -> "Go to Untitled project (unsafe)" -> "Allow").
 *    This will automatically build and format all 3 tabs with sample data!
 * 5. Click the blue "Deploy" button (top right) -> "New deployment".
 * 6. Click the gear icon next to "Select type" -> choose "Web app".
 * 7. Set:
 *    - Description: "Website CMS & Appointments API"
 *    - Execute as: "Me" (your email)
 *    - Who has access: "Anyone" (CRITICAL: Must be "Anyone" so the website can read/write without login)
 * 8. Click "Deploy", copy the "Web app URL" (it ends with /exec).
 * 9. Paste that URL into your website's:
 *    - .env file: GOOGLE_APPS_SCRIPT_URL=...
 *    - assets/js/config.js: APPS_SCRIPT_URL: '...'
 * =========================================================================
 */

// Global Sheet Names
var SHEET_SETTINGS = "Site_Settings";
var SHEET_SERVICES = "Services";
var SHEET_APPOINTMENTS = "Appointments";

/**
 * Handle GET Requests: Serves website CMS content as JSON
 */
function doGet(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var action = e && e.parameter ? e.parameter.action : "";
    
    // Read Site_Settings
    var settingsSheet = ss.getSheetByName(SHEET_SETTINGS);
    var settings = {};
    if (settingsSheet) {
      var data = settingsSheet.getDataRange().getValues();
      // Skip header row 0: Column A is Key, Column B is Value
      for (var i = 1; i < data.length; i++) {
        var key = String(data[i][0]).trim();
        var val = data[i][1];
        if (key) {
          settings[key] = (val !== undefined && val !== null) ? String(val).trim() : "";
        }
      }
    }

    // Read Services
    var servicesSheet = ss.getSheetByName(SHEET_SERVICES);
    var services = [];
    if (servicesSheet) {
      var sData = servicesSheet.getDataRange().getValues();
      for (var j = 1; j < sData.length; j++) {
        var sId = sData[j][0];
        var sName = sData[j][1];
        var sDesc = sData[j][2];
        var sLink = sData[j][3];
        var sIcon = sData[j][4];
        if (sName) {
          services.push({
            id: sId,
            name: sName,
            description: sDesc,
            link: sLink,
            icon: sIcon
          });
        }
      }
    }

    var response = {
      status: "success",
      timestamp: new Date().toISOString(),
      settings: settings,
      services: services
    };

    return ContentService.createTextOutput(JSON.stringify(response))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Handle POST Requests: Receives patient appointment requests from website
 */
function doPost(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var appointmentsSheet = ss.getSheetByName(SHEET_APPOINTMENTS);
    
    // Auto-create sheet if missing
    if (!appointmentsSheet) {
      appointmentsSheet = ss.insertSheet(SHEET_APPOINTMENTS);
      appointmentsSheet.appendRow([
        "Timestamp", "Patient_Name", "Phone_Number", "Preferred_Date", "Preferred_Session", "Status", "Source", "Notes"
      ]);
    }

    // Parse payload
    var payload = {};
    if (e.postData && e.postData.contents) {
      try {
        payload = JSON.parse(e.postData.contents);
      } catch (jsonErr) {
        // Fallback for url-encoded form data
        payload = e.parameter || {};
      }
    } else if (e.parameter) {
      payload = e.parameter;
    }

    var name = payload.name || payload.patient_name || "Unknown Patient";
    var phone = payload.phone || payload.patient_phone || "";
    var date = payload.date || payload.preferred_date || "Any Date";
    var session = payload.session || payload.preferred_session || "No preference";
    var notes = payload.notes || payload.message || "";
    var source = payload.source || "Website Online Form";

    // Format IST Timestamp
    var istTime = Utilities.formatDate(new Date(), "Asia/Kolkata", "yyyy-MM-dd HH:mm:ss");

    // Append to sheet
    appointmentsSheet.appendRow([
      istTime,
      name,
      phone,
      date,
      session,
      "New Request",
      source,
      notes
    ]);

    // Send confirmation email to clinic if email is present (optional notification)
    try {
      var clinicEmail = ss.getSheetByName(SHEET_SETTINGS) ? getSettingValue(ss, "clinic_email") : "";
      if (clinicEmail && clinicEmail.indexOf("@") !== -1) {
        MailApp.sendEmail({
          to: clinicEmail,
          subject: "New Appointment Request: " + name + " (" + phone + ")",
          body: "A new appointment request was booked on the website:\n\n" +
                "Patient Name: " + name + "\n" +
                "Phone Number: " + phone + "\n" +
                "Preferred Date: " + date + "\n" +
                "Preferred Session: " + session + "\n" +
                "Timestamp: " + istTime + "\n\n" +
                "View and manage all appointments in your Google Sheet:\n" +
                ss.getUrl()
        });
      }
    } catch (mailErr) {
      // Continue even if mail limit is reached
      Logger.log("Mail notification skipped: " + mailErr);
    }

    var result = {
      status: "success",
      message: "Appointment successfully logged to Google Spreadsheet!",
      timestamp: istTime,
      patient: {
        name: name,
        phone: phone,
        date: date,
        session: session
      }
    };

    return ContentService.createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Helper to get a setting value from Site_Settings
 */
function getSettingValue(ss, keyName) {
  var sheet = ss.getSheetByName(SHEET_SETTINGS);
  if (!sheet) return "";
  var data = sheet.getDataRange().getValues();
  for (var i = 1; i < data.length; i++) {
    if (String(data[i][0]).trim() === keyName) {
      return String(data[i][1]).trim();
    }
  }
  return "";
}

/**
 * ONE-CLICK SETUP FUNCTION:
 * Run this function in Apps Script to automatically build and format all 3 sheets!
 */
function setupInitialSheets() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  // 1. Setup Site_Settings
  var sSheet = ss.getSheetByName(SHEET_SETTINGS);
  if (!sSheet) sSheet = ss.insertSheet(SHEET_SETTINGS);
  if (sSheet.getLastRow() === 0) {
    var settingsRows = [
      ["Parameter_Key", "Value", "Description", "Category", "Example / Notes"],
      ["doctor_name", "Dr. Sachchidanand Singh", "Full name of doctor", "Doctor Profile", "Displayed in header, bio, and footer"],
      ["doctor_title", "Consultant Psychiatrist", "Doctor title", "Doctor Profile", "Consultant Psychiatrist"],
      ["doctor_qualifications", "MBBS (PMCH), MD Psychiatry (CIP Ranchi)", "Medical degrees", "Doctor Profile", "Shown in About section"],
      ["clinic_name", "Shanti Neuropsychiatry Centre", "Name of clinic", "Clinic Info", "Displayed throughout site"],
      ["clinic_city", "Patna, Bihar", "City location", "Clinic Info", "Patna, Bihar"],
      ["phone_primary", "+91 70704 74808", "Primary phone", "Contact", "Main calling number"],
      ["phone_secondary", "+91 99054 00460", "Alternate phone", "Contact", "Secondary line"],
      ["whatsapp_number", "917070474808", "WhatsApp number with country code", "Contact", "Without '+' or dashes"],
      ["clinic_email", "shantineuropsychiatry@gmail.com", "Clinic email", "Contact", "Patient queries"],
      ["clinic_address", "G-37, Rajni Path, in front of Savera Cancer Hospital, PC Colony, Kankarbagh, Patna 800020", "Physical address", "Clinic Info", "Full address"],
      ["clinic_hours_text", "Monday to Saturday: 9:00 am – 12:00 pm, 3:00 pm – 7:00 pm (Sunday Closed)", "Hours text", "Clinic Info", "Working hours display"],
      ["google_maps_url", "https://www.google.com/maps/search/?api=1&query=Shanti+Neuropsychiatry+Centre+Kankarbagh+Patna", "Google Maps URL", "Contact", "Directions link"],
      ["hero_title", "A calm first conversation with a psychiatrist in Patna", "Homepage hero headline", "Homepage", "Main welcome headline"],
      ["hero_lead", "Dr. Sachchidanand Singh sees patients at Shanti Neuropsychiatry Centre in Kankarbagh. Send a request and the clinic will follow up by phone to agree a time.", "Homepage lead text", "Homepage", "Subtitle under headline"],
      ["about_doctor_summary", "Dr. Sachchidanand Singh is a consultant psychiatrist in Patna. He trained at the Central Institute of Psychiatry in Ranchi and has worked in several clinical settings since 2015.", "Doctor summary", "Doctor Profile", "Bio on home and about"],
      ["banner_alert_active", "FALSE", "Display notice banner (TRUE or FALSE)", "Announcement", "Set TRUE to show alert at top"],
      ["banner_alert_text", "Notice: Clinic is open Mon-Sat. Walk-in & WhatsApp appointment requests are welcome.", "Announcement text", "Announcement", "Top bar message"],
      ["doctor_photo_drive_url", "https://drive.google.com/file/d/YOUR_DOCTOR_PHOTO_ID/view?usp=sharing", "Doctor photo Google Drive share link", "Media / Images", "Direct Google Drive share link"],
      ["clinic_logo_drive_url", "https://drive.google.com/file/d/YOUR_LOGO_ID/view?usp=sharing", "Clinic logo Google Drive share link", "Media / Images", "Direct Google Drive share link"],
      ["clinic_emblem_drive_url", "https://drive.google.com/file/d/YOUR_EMBLEM_ID/view?usp=sharing", "Emblem Google Drive share link", "Media / Images", "Header emblem link"],
      ["youtube_url", "https://www.youtube.com/@drsachchidanandsingh", "YouTube link", "Social Media", "YouTube channel"],
      ["facebook_url", "https://www.facebook.com/sachchidanand.singh.5", "Facebook link", "Social Media", "Facebook profile"],
      ["instagram_url", "https://instagram.com/drsachchi", "Instagram link", "Social Media", "Instagram handle"]
    ];
    sSheet.getRange(1, 1, settingsRows.length, settingsRows[0].length).setValues(settingsRows);
    styleHeader(sSheet, 5);
  }

  // 2. Setup Services
  var svSheet = ss.getSheetByName(SHEET_SERVICES);
  if (!svSheet) svSheet = ss.insertSheet(SHEET_SERVICES);
  if (svSheet.getLastRow() === 0) {
    var servicesRows = [
      ["ID", "Service_Name", "Short_Description", "Details_Link", "Icon_Key"],
      ["SVC-01", "Psychiatric consultation", "A full assessment and diagnosis by a psychiatrist, followed by a personalized treatment plan.", "/services/", "psychiatry"],
      ["SVC-02", "Counselling", "Structured one-to-one counselling to address stress, relationships, and emotional wellbeing.", "/service/counselling/", "counselling"],
      ["SVC-03", "Cognitive behaviour therapy & Assessment", "Evidence-based CBT and psychological evaluations conducted by a qualified psychotherapist.", "/service/counselling/", "therapy"],
      ["SVC-04", "De-Addiction & Substance Rehabilitation", "Medically supervised detoxification and relapse-prevention programs for alcohol, tobacco, and substance dependence.", "/service/de-addiction/", "rehab"],
      ["SVC-05", "Child & Adolescent Mental Health", "Compassionate evaluation and treatment for ADHD, behavioural difficulties, childhood depression, and academic stress in youth.", "/service/child-adolescent/", "pediatric"],
      ["SVC-06", "Video or audio consultation", "Telemedicine consultations for patients unable to visit the clinic in person.", "/service/video-consultation/", "telemedicine"]
    ];
    svSheet.getRange(1, 1, servicesRows.length, servicesRows[0].length).setValues(servicesRows);
    styleHeader(svSheet, 5);
  }

  // 3. Setup Appointments
  var aSheet = ss.getSheetByName(SHEET_APPOINTMENTS);
  if (!aSheet) aSheet = ss.insertSheet(SHEET_APPOINTMENTS);
  if (aSheet.getLastRow() === 0) {
    var apptRows = [
      ["Timestamp", "Patient_Name", "Phone_Number", "Preferred_Date", "Preferred_Session", "Status", "Source", "Notes"],
      ["2026-10-16 10:30:00", "Demo Patient", "+91 98765 43210", "2026-10-18", "Morning, 9:00 am to 12:00 pm", "Confirmed", "Website Form", "First visit consultation"]
    ];
    aSheet.getRange(1, 1, apptRows.length, apptRows[0].length).setValues(apptRows);
    styleHeader(aSheet, 8);
  }

  SpreadsheetApp.getUi().alert("Setup complete! All 3 sheets (Site_Settings, Services, Appointments) are ready.\n\nNow click 'Deploy' -> 'New deployment' -> 'Web app' (Who has access: Anyone).");
}

function styleHeader(sheet, numCols) {
  var range = sheet.getRange(1, 1, 1, numCols);
  range.setBackground("#0E2A5A")
       .setFontColor("#FFFFFF")
       .setFontWeight("bold")
       .setFontFamily("Segoe UI");
  sheet.setFrozenRows(1);
}
