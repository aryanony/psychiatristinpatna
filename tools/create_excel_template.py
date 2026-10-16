#!/usr/bin/env python3
"""
Generates the website-cms-data.xlsx Excel workbook and CSV exports
for Shanti Neuropsychiatry Centre website CMS.
"""
import os
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Prepare Data
SETTINGS_DATA = [
    ["Parameter_Key", "Value", "Description", "Category", "Example / Notes"],
    # General / Doctor Info
    ["doctor_name", "Dr. Sachchidanand Singh", "Full name of the doctor", "Doctor Profile", "Displayed in header, bio, and footer"],
    ["doctor_title", "Consultant Psychiatrist", "Doctor professional title", "Doctor Profile", "E.g. Consultant Psychiatrist"],
    ["doctor_qualifications", "MBBS (PMCH), MD Psychiatry (CIP Ranchi)", "Medical degrees and training", "Doctor Profile", "Shown in About & Credentials"],
    ["clinic_name", "Shanti Neuropsychiatry Centre", "Name of the clinic", "Clinic Info", "Displayed throughout the website"],
    ["clinic_city", "Patna, Bihar", "City and state location", "Clinic Info", "Patna, Bihar"],
    
    # Contact & Communication
    ["phone_primary", "+91 70704 74808", "Primary clinic calling number", "Contact", "Call & SMS clickable link"],
    ["phone_secondary", "+91 99054 00460", "Alternate phone number", "Contact", "Secondary clinic line"],
    ["whatsapp_number", "917070474808", "WhatsApp number with country code", "Contact", "No '+' or dashes; for direct WhatsApp booking"],
    ["clinic_email", "shantineuropsychiatry@gmail.com", "Clinic email address", "Contact", "For inquiries and correspondence"],
    ["clinic_address", "G-37, Rajni Path, in front of Savera Cancer Hospital, PC Colony, Kankarbagh, Patna 800020", "Full physical address", "Clinic Info", "Exact street address for patients"],
    ["clinic_hours_text", "Monday to Saturday: 9:00 am – 12:00 pm, 3:00 pm – 7:00 pm (Sunday Closed)", "Working hours text", "Clinic Info", "Displayed in clinic hours block"],
    ["google_maps_url", "https://www.google.com/maps/search/?api=1&query=Shanti+Neuropsychiatry+Centre+Kankarbagh+Patna", "Google Maps location link", "Contact", "Opens directions in Google Maps"],
    
    # Homepage Hero & Intro
    ["hero_title", "A calm first conversation with a psychiatrist in Patna", "Main headline on homepage", "Homepage", "Keep clear, comforting, and welcoming"],
    ["hero_lead", "Dr. Sachchidanand Singh sees patients at Shanti Neuropsychiatry Centre in Kankarbagh. Send a request and the clinic will follow up by phone to agree a time.", "Homepage sub-headline / lead text", "Homepage", "Explains what to expect"],
    ["about_doctor_summary", "Dr. Sachchidanand Singh is a consultant psychiatrist in Patna. He trained at the Central Institute of Psychiatry in Ranchi and has worked in several clinical settings since 2015. His clinical approach focuses on personalized mental health care without stigma.", "Short bio about the doctor", "Doctor Profile", "Homepage & About section summary"],
    
    # Notice & Announcement Banner
    ["banner_alert_active", "FALSE", "Set TRUE to display top notice banner, FALSE to hide", "Announcement", "TRUE or FALSE (all uppercase)"],
    ["banner_alert_text", "Notice: Clinic is open Mon-Sat. Walk-in and WhatsApp appointment requests are being accepted.", "Message text inside announcement banner", "Announcement", "E.g. Holiday hours or special announcement"],
    
    # Google Drive Images & Media
    ["doctor_photo_drive_url", "https://drive.google.com/file/d/YOUR_DOCTOR_PHOTO_ID/view?usp=sharing", "Doctor photo Google Drive share link", "Media / Images", "Paste ANY Google Drive link; system auto-converts to CDN image"],
    ["clinic_logo_drive_url", "https://drive.google.com/file/d/YOUR_LOGO_ID/view?usp=sharing", "Clinic logo Google Drive share link", "Media / Images", "Leave default or paste your Google Drive share link"],
    ["clinic_emblem_drive_url", "https://drive.google.com/file/d/YOUR_EMBLEM_ID/view?usp=sharing", "Header emblem Google Drive share link", "Media / Images", "Paste Google Drive share link"],
    
    # Social Media Links
    ["youtube_url", "https://www.youtube.com/@drsachchidanandsingh", "YouTube channel link", "Social Media", "Video talks & mental health guides"],
    ["facebook_url", "https://www.facebook.com/sachchidanand.singh.5", "Facebook page link", "Social Media", "Official Facebook profile"],
    ["instagram_url", "https://instagram.com/drsachchi", "Instagram profile link", "Social Media", "Clinic Instagram handle"]
]

SERVICES_DATA = [
    ["ID", "Service_Name", "Short_Description", "Details_Link", "Icon_Key"],
    ["SVC-01", "Psychiatric consultation", "A full assessment and diagnosis by a psychiatrist, followed by a personalized treatment plan with medicines and guidance.", "/services/", "psychiatry"],
    ["SVC-02", "Counselling", "Structured one-to-one counselling at the centre to address stress, grief, relationships, and emotional wellbeing.", "/service/counselling/", "counselling"],
    ["SVC-03", "Cognitive behaviour therapy & Assessment", "Evidence-based CBT and comprehensive psychological evaluations conducted by a qualified psychotherapist.", "/service/counselling/", "therapy"],
    ["SVC-04", "De-Addiction & Substance Rehabilitation", "Medically supervised detoxification and long-term relapse prevention programs for alcohol, tobacco, cannabis, and prescription drug dependence.", "/service/de-addiction/", "rehab"],
    ["SVC-05", "Child & Adolescent Mental Health", "Compassionate evaluation and treatment for ADHD, behavioural difficulties, childhood depression, and academic stress in youth.", "/service/child-adolescent/", "pediatric"],
    ["SVC-06", "Video or audio consultation", "Telemedicine consultations for patients unable to visit the clinic in person, adhering to national clinical guidelines.", "/service/video-consultation/", "telemedicine"]
]

APPOINTMENTS_DATA = [
    ["Timestamp", "Patient_Name", "Phone_Number", "Preferred_Date", "Preferred_Session", "Status", "Source", "Notes"],
    ["2026-10-16 10:30:00", "Demo Patient", "+91 98765 43210", "2026-10-18", "Morning, 9:00 am to 12:00 pm", "Confirmed", "Website Form", "First visit for general anxiety consultation"],
    ["2026-10-16 14:15:22", "Sample Booking", "+91 70123 45678", "2026-10-19", "Evening, 3:00 pm to 7:00 pm", "New Request", "Website WhatsApp", "Follow up discussion"]
]

def build_excel():
    wb = openpyxl.Workbook()
    # Default sheet
    ws_settings = wb.active
    ws_settings.title = "Site_Settings"
    ws_services = wb.create_sheet(title="Services")
    ws_appointments = wb.create_sheet(title="Appointments")

    # Styling helper
    header_fill = PatternFill(start_color="0E2A5A", end_color="0E2A5A", fill_type="solid")
    header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Segoe UI", size=10)
    bold_key_font = Font(name="Segoe UI", size=10, bold=True, color="0E2A5A")
    thin_border = Border(
        left=Side(style='thin', color='E0E0E0'),
        right=Side(style='thin', color='E0E0E0'),
        top=Side(style='thin', color='E0E0E0'),
        bottom=Side(style='thin', color='E0E0E0')
    )
    alt_fill = PatternFill(start_color="F7FAFC", end_color="F7FAFC", fill_type="solid")

    def format_sheet(ws, data, is_settings=False):
        for r_idx, row in enumerate(data, 1):
            ws.append(row)
            for c_idx, val in enumerate(row, 1):
                cell = ws.cell(row=r_idx, column=c_idx)
                cell.border = thin_border
                if r_idx == 1:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                else:
                    if r_idx % 2 == 1:
                        cell.fill = alt_fill
                    if is_settings and c_idx == 1:
                        cell.font = bold_key_font
                    else:
                        cell.font = data_font
                    cell.alignment = Alignment(vertical="center", wrap_text=(c_idx in [2, 3, 5]))
            ws.row_dimensions[r_idx].height = 24 if r_idx > 1 else 28

        # Auto column width
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = min(max(max_len + 4, 14), 55)

    format_sheet(ws_settings, SETTINGS_DATA, is_settings=True)
    format_sheet(ws_services, SERVICES_DATA)
    format_sheet(ws_appointments, APPOINTMENTS_DATA)

    # Save Excel in root and cms folder
    xlsx_path = os.path.join(ROOT, "website-cms-data.xlsx")
    wb.save(xlsx_path)
    print(f"Generated Excel file: {xlsx_path}")

    # Generate CSVs
    cms_dir = os.path.join(ROOT, "cms-templates")
    os.makedirs(cms_dir, exist_ok=True)

    def write_csv(filename, data):
        path = os.path.join(cms_dir, filename)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"Generated CSV: {path}")

    write_csv("Site_Settings.csv", SETTINGS_DATA)
    write_csv("Services.csv", SERVICES_DATA)
    write_csv("Appointments.csv", APPOINTMENTS_DATA)

if __name__ == "__main__":
    build_excel()
