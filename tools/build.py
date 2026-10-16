#!/usr/bin/env python3
"""Generates every page. Run from the project root:  python tools/build.py   (add --launch or run directly for production launch)"""
import os, re, sys, json

# Production launch mode (active by default for final launch, unless --staging is explicitly passed)
LAUNCH = '--staging' not in sys.argv
REVIEWED_BY = 'Dr. Sachchidanand Singh, MD Psychiatry (CIP Ranchi)'
DOM = 'https://www.psychiatristinpatna.com'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLINIC = 'Shanti Neuropsychiatry Centre'
ADDR = 'G-37, Rajni Path, in front of Savera Cancer Hospital<br>PC Colony, Kankarbagh, Patna 800020'
NAV = [('Home','/'),('About','/about/'),('Services','/services/'),('Blog','/blogs/'),('Contact','/contact/')]
ICONS = open(ROOT+'/assets/img/icons.svg', encoding='utf-8').read()
home = open(ROOT+'/tools/src/home-main.html', encoding='utf-8').read()
form = re.search(r'<section class="blk" id="request">.*?</section>', home, re.S).group(0).replace('<h2>Request an appointment</h2>','<h2>Before you send</h2>')

def ic(n): return '<svg class="ic" aria-hidden="true"><use href="#i-%s"/></svg>'%n
PAGES = []

def page(path, title, desc, body, crumbs=(), schema=None, main_cls=''):
    PAGES.append(path)
    depth = 0 if path == '/' else path.strip('/').count('/') + 1
    r = '../' * depth
    def fix(m): return '%s="%s"' % (m[1], (r + m[2]) or './')
    nav = ''.join('<a href="%s"%s>%s</a>' % ((r + p.strip('/') + '/') if p != '/' else (r or './'), ' aria-current="page"' if p == path else '', l) for l, p in NAV)
    m_nav = ''.join('''<a href="%s"%s class="m-link"><span class="m-link-lead"><svg class="ic" aria-hidden="true"><use href="#%s"/></svg><span>%s</span></span><span class="m-arrow" aria-hidden="true">→</span></a>''' % (
        ((r + p.strip('/') + '/') if p != '/' else (r or './')),
        ' aria-current="page"' if p == path else '',
        ico,
        label
    ) for label, p, ico in [
        ('Home', '/', 'i-brain'),
        ('About Dr. Singh', '/about/', 'i-verified'),
        ('Specialized Services', '/services/', 'i-stethoscope'),
        ('Mental Health Blog', '/blogs/', 'i-chat'),
        ('Contact & Directions', '/contact/', 'i-pin'),
        ('Request Appointment', '/appointment/', 'i-calendar'),
    ])
    bc = ''
    gl = []
    if crumbs:
        allc = [('Home', '/')] + list(crumbs)
        bc = '<nav class="crumbs wrap" aria-label="Breadcrumb">' + ' / '.join('<a href="@/%s">%s</a>' % (p.strip('/') + '/' if p != '/' else '', l) for l, p in allc[:-1]) + ' / <span aria-current="page">%s</span></nav>' % allc[-1][0]
        gl.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": l, "item": DOM + (p if p.endswith('/') else p + '/')} for i, (l, p) in enumerate(allc)]})
    if schema: gl += schema
    ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": gl}, ensure_ascii=False) + '</script>' if gl else ''
    canon = DOM + path
    h = '''<!doctype html>
<html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>[[T]]</title><meta name="description" content="[[D]]">
[[ROBOTS]]<link rel="canonical" href="[[C]]">
<meta property="og:type" content="website"><meta property="og:site_name">
<meta property="og:title" content="[[T]]"><meta property="og:description" content="[[D]]"><meta property="og:url" content="[[C]]"><meta property="og:image" content="[[DOM]]/assets/img/dr-sachchidanand-singh.jpg"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0e2a5a"><link rel="icon" href="@/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" href="@/assets/img/favicon-64.png"><link rel="apple-touch-icon" href="@/assets/img/apple-touch-icon.png"><link rel="manifest" href="@/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Public+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="@/assets/css/site.css">[[LD]]</head>
<body><div hidden>[[ICONS]]</div><a class="skip" href="#main">Skip to content</a>
<div id="cms-alert-banner" hidden><div class="wrap"><span class="badge">Notice</span> <span id="cms-alert-text" data-cms="banner_alert_text"></span></div></div>
<header id="site-header"><div class="wrap bar"><a class="brand" href="@/"><img src="@/assets/img/emblem.png" width="46" height="41" alt="" data-cms="clinic_emblem_drive_url" data-cms-attr="src"><span><b data-cms="doctor_name">Dr. Sachchidanand Singh</b><span data-cms="clinic_name">[[CL]], Patna</span></span></a>
<nav class="desktop-nav" aria-label="Main">[[NAV]]</nav>
<a class="btn sm header-cta" href="@/appointment/">Request appointment</a>
<button class="menu-toggle" id="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Toggle navigation menu"><span class="hamburger-box"><span class="hamburger-line"></span><span class="hamburger-line"></span><span class="hamburger-line"></span></span></button>
</div>
<div class="mobile-drawer" id="mobile-nav" aria-label="Mobile Navigation" hidden>
  <div class="mobile-drawer-inner">
    <div class="mobile-drawer-head">
      <div class="mobile-drawer-brand">
        <img src="@/assets/img/emblem.png" width="38" height="34" alt="" data-cms="clinic_emblem_drive_url" data-cms-attr="src">
        <div>
          <b data-cms="doctor_name">Dr. Sachchidanand Singh</b>
          <span data-cms="clinic_name">Shanti Neuropsychiatry Centre</span>
        </div>
      </div>
      <button class="mobile-close-btn" id="mobile-close-btn" type="button" aria-label="Close navigation menu">&times;</button>
    </div>
    <nav class="mobile-links" aria-label="Mobile Menu Links">
      [[M_NAV]]
    </nav>
    <div class="mobile-drawer-actions">
      <a class="btn mobile-appt-btn" href="@/appointment/">
        <svg class="ic" aria-hidden="true"><use href="#i-calendar"/></svg>
        <span>Request Appointment</span>
      </a>
      <a class="btn alt mobile-call-btn" href="tel:+917070474808" data-cms="phone_primary" data-cms-attr="tel">
        <svg class="ic" aria-hidden="true"><use href="#i-phone"/></svg>
        <span>Call +91 70704 74808</span>
      </a>
      <a class="btn mobile-wa-btn" href="https://wa.me/917070474808" target="_blank" rel="noopener">
        <svg class="ic" aria-hidden="true"><use href="#i-whatsapp"/></svg>
        <span>Chat on WhatsApp</span>
      </a>
    </div>
    <div class="mobile-drawer-meta">
      <p class="mobile-meta-timing">
        <svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>
        <span><strong>Hours:</strong> Mon – Sat: 9am–12pm & 3pm–7pm</span>
      </p>
      <p class="mobile-meta-location">
        <svg class="ic" aria-hidden="true"><use href="#i-pin"/></svg>
        <span>G-37, Rajni Path, PC Colony, Kankarbagh, Patna</span>
      </p>
      <div class="mobile-drawer-socials">
        <a href="https://maps.app.goo.gl/DeZgu7aFKnqsi6L69" target="_blank" rel="noopener" aria-label="Google Maps"><svg class="ic" aria-hidden="true"><use href="#i-google-map"/></svg></a>
        <a href="https://www.youtube.com/@drsachchidanandsingh" target="_blank" rel="noopener" aria-label="YouTube"><svg class="ic" aria-hidden="true"><use href="#i-youtube"/></svg></a>
        <a href="https://www.facebook.com/sachchidanand.singh.5" target="_blank" rel="noopener" aria-label="Facebook"><svg class="ic" aria-hidden="true"><use href="#i-facebook"/></svg></a>
        <a href="https://instagram.com/drsachchi" target="_blank" rel="noopener" aria-label="Instagram"><svg class="ic" aria-hidden="true"><use href="#i-instagram"/></svg></a>
        <a href="https://in.linkedin.com/in/dr-sachchidanand-singh-28724647" target="_blank" rel="noopener" aria-label="LinkedIn"><svg class="ic" aria-hidden="true"><use href="#i-linkedin"/></svg></a>
      </div>
    </div>
  </div>
  <div class="mobile-drawer-backdrop" id="mobile-backdrop"></div>
</div>
</header>
[[BC]]<main id="main" class="[[MC]]">[[BODY]]</main>
<footer><div class="wrap cols">
<div>
  <img src="@/assets/img/logo-full.png" width="170" height="170" alt="Dr. Sachchidanand Singh, Psychiatrist, Patna. Better Mind, Healthier Life." loading="lazy" data-cms="clinic_logo_drive_url" data-cms-attr="src">
  <div style="margin-top:1rem;font-size:.9rem;line-height:1.5">
    <p style="margin:0 0 .5rem"><strong>Shanti Neuropsychiatry Centre</strong><br>Consultant Neuropsychiatrist & De-Addiction Specialist</p>
    <p style="margin:0"><span class="badge" style="background:#f59e0b;color:#000;font-weight:700;padding:.2rem .5rem;border-radius:3px">4.9 ★</span> Over 1,600+ Patient Reviews</p>
  </div>
</div>
<div>
  <h2>Contact & Location</h2>
  <p><a href="tel:+917070474808" data-cms="phone_primary" data-cms-attr="tel">+91 70704 74808</a><br><a href="tel:+919905400460" data-cms="phone_secondary" data-cms-attr="tel">+91 99054 00460</a><br><a href="mailto:shantineuropsychiatry@gmail.com" data-cms="clinic_email" data-cms-attr="mailto">shantineuropsychiatry@gmail.com</a></p>
  <p data-cms="clinic_address">[[ADDR]]</p>
  <div class="social-links" style="margin-top:.75rem">
    <a class="social-btn wa" href="https://wa.me/917070474808" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-whatsapp"/></svg> WhatsApp</a>
    <a class="social-btn gmb" href="https://maps.app.goo.gl/DeZgu7aFKnqsi6L69" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-google-map"/></svg> Google Maps</a>
    <a class="social-btn yt" href="https://www.youtube.com/@drsachchidanandsingh" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-youtube"/></svg> YouTube</a>
    <a class="social-btn fb" href="https://www.facebook.com/sachchidanand.singh.5" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-facebook"/></svg> Facebook</a>
    <a class="social-btn insta" href="https://instagram.com/drsachchi" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-instagram"/></svg> Instagram</a>
    <a class="social-btn in" href="https://in.linkedin.com/in/dr-sachchidanand-singh-28724647" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-linkedin"/></svg> LinkedIn</a>
  </div>
</div>
<div>
  <h2>Consultation Hours & Notice</h2>
  <p><strong>Mon – Sat:</strong> 9:00 am – 12:00 pm, 3:00 pm – 7:00 pm<br><strong>Sunday:</strong> Closed</p>
  <p>This website provides general information and is not personal medical advice. The request form and WhatsApp are not emergency services. In an emergency go to the nearest hospital emergency department.</p>
  <div class="flinks"><a href="@/privacy/">Privacy</a><a href="@/terms/">Terms</a><a href="@/accessibility/">Accessibility</a><a href="@/medical-disclaimer/">Medical disclaimer</a></div>
</div></div></footer>
<script src="@/assets/js/config.js"></script>
<script src="@/assets/js/cms.js" defer></script>
<script src="@/assets/js/site.js" defer></script></body></html>'''
    h = h.replace('[[T]]', title).replace('[[D]]', desc).replace('[[C]]', canon).replace('[[DOM]]', DOM).replace('[[LD]]', ld).replace('[[ICONS]]', ICONS).replace('[[CL]]', CLINIC).replace('[[NAV]]', nav).replace('[[M_NAV]]', m_nav).replace('[[BC]]', bc).replace('[[MC]]', main_cls).replace('[[ADDR]]', ADDR.replace('<br>', ', ')).replace('<meta property="og:site_name">', '<meta property="og:site_name" content="%s">' % CLINIC)
    h = h.replace('[[ROBOTS]]', '' if LAUNCH else '<meta name="robots" content="noindex, nofollow">\n').replace('[[BODY]]', body)
    h = re.sub(r'(href|src)="@/([^"]*)"', fix, h)
    d = ROOT + ('' if path == '/' else path)
    os.makedirs(d, exist_ok=True)
    open(d + '/index.html', 'w', encoding='utf-8').write(h)

def head(h1, lead=''): return '<div class="wrap pagehead"><h1>%s</h1>%s</div>' % (h1, '<p>%s</p>' % lead if lead else '')
def cta(t='Ready to talk to someone?'): return '<div class="band"><div class="wrap"><p>%s</p><div class="acts"><a class="btn" href="@/appointment/">Request an appointment</a><a class="btn alt" href="tel:+917070474808" data-cms="phone_primary" data-cms-attr="tel">Call +91 70704 74808</a></div></div></div>' % t
def prose(x): return '<div class="wrap"><div class="prose">%s</div></div>' % x

CLIN = {
    "@type": "MedicalClinic",
    "@id": DOM + "/#clinic",
    "name": CLINIC,
    "url": DOM + "/",
    "telephone": "+91-7070474808",
    "email": "shantineuropsychiatry@gmail.com",
    "image": DOM + "/assets/img/dr-sachchidanand-singh.jpg",
    "medicalSpecialty": "Psychiatric",
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "1620",
        "bestRating": "5",
        "worstRating": "1"
    },
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "G-37, Rajni Path, in front of Savera Cancer Hospital, PC Colony, Kankarbagh",
        "addressLocality": "Patna",
        "addressRegion": "Bihar",
        "postalCode": "800020",
        "addressCountry": "IN"
    },
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:00", "closes": "12:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "15:00", "closes": "19:00"}
    ],
    "hasMap": "https://maps.app.goo.gl/DeZgu7aFKnqsi6L69",
    "sameAs": [
        "https://www.youtube.com/@drsachchidanandsingh",
        "https://www.facebook.com/sachchidanand.singh.5",
        "https://instagram.com/drsachchi",
        "https://in.linkedin.com/in/dr-sachchidanand-singh-28724647",
        "https://share.google/f71kgcyca5U7wbLtC",
        "https://maps.app.goo.gl/DeZgu7aFKnqsi6L69"
    ]
}

DOC = {
    "@type": "Physician",
    "name": "Dr. Sachchidanand Singh",
    "jobTitle": "Consultant Neuropsychiatrist",
    "medicalSpecialty": "Psychiatric",
    "worksFor": {"@id": DOM + "/#clinic"},
    "image": DOM + "/assets/img/dr-sachchidanand-singh.jpg",
    "url": DOM + "/about/"
}

FAQ_SCHEMA = {
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": "Do I need a doctor's referral to book an appointment?", "acceptedAnswer": {"@type": "Answer", "text": "No referral is required. Patients and family members can directly request a visit using the online appointment form, via WhatsApp, or by calling the clinic during working hours."}},
        {"@type": "Question", "name": "What happens during the first consultation?", "acceptedAnswer": {"@type": "Answer", "text": "The first visit is an in-depth conversation focused on understanding what you or your loved one is experiencing. Dr. Singh listens to the history, symptoms, lifestyle factors, and previous treatments. A clear diagnosis and personalized treatment plan are explained openly."}},
        {"@type": "Question", "name": "Are mental health consultations confidential?", "acceptedAnswer": {"@type": "Answer", "text": "Yes, strict medical confidentiality is maintained. Your conversations, diagnosis, and treatment records are private and never shared without your explicit consent."}},
        {"@type": "Question", "name": "Can I consult online via video if I live outside Patna?", "acceptedAnswer": {"@type": "Answer", "text": "Yes, telemedicine video consultations are available for follow-up patients and individuals residing in remote locations who cannot travel to Kankarbagh, subject to national telemedicine regulatory guidelines."}},
        {"@type": "Question", "name": "What are the clinic days and timings?", "acceptedAnswer": {"@type": "Answer", "text": "Shanti Neuropsychiatry Centre operates Monday to Saturday in two sessions: Morning from 9:00 am to 12:00 pm, and Evening from 3:00 pm to 7:00 pm. The clinic is closed on Sundays."}}
    ]
}

# 1. HOME PAGE
hm = home.replace('what the patient prefers.</p>', 'what the patient prefers.</p><p><a href="@/services/">See all specialized services</a></p>', 1)
page('/', 'Dr. Sachchidanand Singh | Top Psychiatrist in Kankarbagh, Patna | Shanti Neuropsychiatry Centre', 'Dr. Sachchidanand Singh (MBBS PMCH, MD Psychiatry CIP Ranchi), senior consultant neuropsychiatrist at Shanti Neuropsychiatry Centre, Kankarbagh, Patna. 15+ years experience. 4.9 star rated. Request an appointment.', hm, schema=[CLIN, DOC, FAQ_SCHEMA])

# 2. ABOUT PAGE
about_body = '''
<div class="wrap" style="padding-top:1rem">
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2.5rem;align-items:start">
    <div style="background:#fff;border:1px solid var(--line);border-radius:8px;padding:1.25rem;box-shadow:0 8px 24px rgba(14,42,90,.06)">
      <div style="border-radius:6px;overflow:hidden;background:var(--mist);margin-bottom:1rem">
        <img src="@/assets/img/dr-sachchidanand-singh.jpg" alt="Dr. Sachchidanand Singh" style="display:block;width:100%;height:auto" data-cms="doctor_photo_drive_url" data-cms-attr="src">
      </div>
      <h3 style="font:600 1.35rem Newsreader,Georgia,serif;color:var(--navy);margin-bottom:.3rem" data-cms="doctor_name">Dr. Sachchidanand Singh</h3>
      <p style="color:var(--soft);margin-bottom:.75rem"><strong>MBBS (Patna), MD Psychiatry (CIP Ranchi)</strong></p>
      <div style="font-size:.9rem;color:var(--navy);line-height:1.6;border-top:1px solid var(--line);padding-top:.75rem">
        <p style="margin:0 0 .3rem"><strong>Reg. No:</strong> 37058 (Bihar Medical Council)</p>
        <p style="margin:0 0 .3rem"><strong>Experience:</strong> 15+ Years Clinical Practice</p>
        <p style="margin:0 0 .3rem"><strong>Former Post:</strong> Assistant Professor, PMCH</p>
        <p style="margin:0"><strong>Clinic:</strong> Shanti Neuropsychiatry Centre, Patna</p>
      </div>
    </div>
    <div class="prose" style="padding-bottom:0">
      <p class="lead" style="font-size:1.15rem;color:var(--navy);font-weight:500" data-cms="about_doctor_summary">Dr. Sachchidanand Singh is one of Bihar's most reputable consultant neuropsychiatrists, known for his clinical rigor, thorough diagnostic assessments, and humane, empathetic patient care.</p>
      <p>He completed his MBBS from Patna Medical College & Hospital (PMCH) in 2007, followed by postgraduate M.D. in Psychiatry from the legendary Central Institute of Psychiatry (CIP), Kanke, Ranchi in 2013 — one of Asia's premier institutions for psychiatric training and neuropsychiatric research.</p>
      
      <h2>Academic & Clinical Appointments</h2>
      <ul class="tick">
        <li><strong>Senior Resident (Psychiatry):</strong> Central Institute of Psychiatry (CIP), Ranchi (2013 – 2015)</li>
        <li><strong>Senior Resident (Psychiatry):</strong> Patna Medical College & Hospital (PMCH), Patna (2015 – 2018)</li>
        <li><strong>Assistant Professor (Psychiatry):</strong> Patna Medical College & Hospital (PMCH), Patna</li>
        <li><strong>Founder & Chief Consultant:</strong> Shanti Neuropsychiatry Centre, Kankarbagh, Patna (2015 – Present)</li>
      </ul>

      <h2>Professional Memberships</h2>
      <ul class="tick">
        <li>Life Fellow, Indian Psychiatric Society (IPS)</li>
        <li>Member, Indian Medical Association (IMA)</li>
        <li>Registered with Bihar Medical Council (Reg. No. 37058)</li>
      </ul>

      <h2>Philosophy of Treatment</h2>
      <p>Mental illnesses are multifaceted, involving neurochemical balance, psychological coping mechanisms, family dynamics, and environmental stressors. Dr. Singh's consultation is never rushed. He dedicates time to listen without stigma, examine medical history, explain diagnoses transparently to patients and relatives, and design a rational management plan combining minimal necessary medications with psychological therapy and lifestyle modifications.</p>

      <h2>About Shanti Neuropsychiatry Centre</h2>
      <p><span data-cms="clinic_name">Shanti Neuropsychiatry Centre</span> was established in 2015 on Rajni Path, PC Colony, Kankarbagh (directly opposite Savera Cancer Hospital). The facility is equipped to provide full psychiatric consultations, one-to-one counseling, cognitive behaviour therapy (CBT), psychological testing, addiction rehabilitation support, and telemedicine services.</p>
    </div>
  </div>
</div>
'''
page('/about/', 'About Dr. Sachchidanand Singh | Neuropsychiatrist in Patna', 'Learn about Dr. Sachchidanand Singh (MBBS PMCH, MD CIP Ranchi). 15+ years experience, qualifications, hospital appointments, and psychiatric philosophy.',
head('About <span data-cms="doctor_name">Dr. Sachchidanand Singh</span>', 'Consultant Psychiatrist & Neuropsychiatrist at Shanti Neuropsychiatry Centre, Kankarbagh, Patna.') + about_body + cta(),
[('About', '/about/')], [DOC])

# 3. SERVICES OVERVIEW
SV = [
    ('Psychiatric Evaluation & Consultation', '/services/', 'assets/img/brain-neuropsychiatry.jpg', 'brain', 'Detailed clinical evaluation by Dr. Sachchidanand Singh for depression, anxiety, OCD, panic disorder, bipolar illness, schizophrenia, and sleep disorders. Includes personalized medical treatment planning.'),
    ('Counselling & Psychotherapy', '/service/counselling/', 'assets/img/counselling-therapy.jpg', 'counselling', 'Structured one-to-one psychological sessions to process emotional distress, relationship strain, grief, burnout, and build healthy coping mechanisms.'),
    ('Cognitive Behaviour Therapy (CBT)', '/service/counselling/', 'assets/img/calm-mind-wellness.jpg', 'cbt', 'Evidence-based CBT and psychological assessment conducted by qualified therapists to identify and restructure unhelpful thought patterns and behaviours.'),
    ('De-Addiction & Substance Rehabilitation', '/service/de-addiction/', 'assets/img/deaddiction-care.jpg', 'deaddiction', 'Medically supervised detoxification and long-term relapse prevention programs for alcohol, tobacco, cannabis, and prescription drug dependence.'),
    ('Child & Adolescent Psychiatry', '/service/child-adolescent/', 'assets/img/child-support.jpg', 'child', 'Compassionate evaluation and treatment for ADHD, behavioural difficulties, childhood depression, and academic stress in children and teenagers.'),
    ('Video & Telemedicine Consultation', '/service/video-consultation/', 'assets/img/doctor-video-thumbnail.png', 'video', 'Remote tele-consultations for patients across Bihar and outside Patna who cannot travel in person, conducted in compliance with national telemedicine regulations.')
]

sv_cards_html = '<div class="wrap"><div class="svc-cards">' + ''.join('''
<div class="svc-card">
  <img src="@/%s" alt="%s" class="svc-card-img" loading="lazy">
  <div>
    <div class="svc-head">
      <svg class="ic" aria-hidden="true"><use href="#i-%s"/></svg>
      <h3>%s</h3>
    </div>
    <p>%s</p>
  </div>
  <a class="more" href="@/%s">Learn more <svg class="ic" style="width:1rem;height:1rem" aria-hidden="true"><use href="#i-arrow-right"/></svg></a>
</div>''' % (img, t, ico, t, d, p.strip('/') + '/') for t, p, img, ico, d in SV) + '</div></div>'

page('/services/', 'Mental Health Services in Patna | Shanti Neuropsychiatry Centre', 'Comprehensive neuropsychiatry services in Patna: psychiatric consultation, counselling, CBT, de-addiction, child psychiatry, and video consultations.',
head('Specialized Clinical Services', 'Personalized, evidence-based mental healthcare by Dr. Sachchidanand Singh.') +
sv_cards_html +
prose('''<h2>Conditions Assessed & Treated</h2>
<p>Patients consult Dr. Singh for major depressive disorder, generalized anxiety, OCD, panic attacks, insomnia, bipolar mood disorder, schizophrenia and psychosis, ADHD, headache and migraine, epilepsy, and alcohol or substance addiction. The first clinical consultation determines whether medication, psychotherapy, or a combination will offer the most effective recovery path.</p>
<h2>Clinic Facilities & Care Standards</h2>
<ul class="tick">
  <li>In-depth, unhurried initial clinical evaluation (30–45 minutes)</li>
  <li>Judicious, evidence-based pharmacotherapy prioritizing patient safety</li>
  <li>Confidential, dedicated psychotherapy chambers</li>
  <li>Dual follow-up convenience: in-person clinic visits and secure telemedicine video sessions</li>
  <li>Accessible premises opposite Savera Cancer Hospital, Kankarbagh with parking</li>
</ul>''') + cta(),
[('Services', '/services/')])

# 4. COUNSELLING & CBT
page('/service/counselling/', 'Counselling and CBT in Kankarbagh, Patna | Shanti Neuropsychiatry Centre', 'Professional counselling, cognitive behaviour therapy (CBT), and psychological testing in Patna with trained clinicians.',
head('Counselling & Cognitive Behaviour Therapy', 'Structured conversations and psychological strategies to understand emotions and rebuild life.') + prose('''
<h2>Who Can Benefit from Counselling?</h2>
<p>Counselling provides a safe, confidential environment to work through low mood, chronic worry, workplace burnout, relationship conflicts, bereavement, and low self-esteem. It is often integrated alongside medical treatments or utilized independently for situational stressors.</p>

<h2>Cognitive Behaviour Therapy (CBT)</h2>
<p>CBT is one of the most rigorously researched psychological treatments globally. It focuses on the bidirectional relationship between thoughts, emotions, and physical behaviours. During CBT sessions, you work collaboratively with the therapist to:</p>
<ul class="tick">
  <li>Identify automatic negative thoughts and cognitive distortions that fuel anxiety or depression.</li>
  <li>Practice behavioural experiments and thought-reframing techniques.</li>
  <li>Implement Exposure and Response Prevention (ERP) for obsessive compulsive disorder (OCD).</li>
  <li>Develop sustainable stress-management and problem-solving skills for everyday life.</li>
</ul>

<h2>Psychological & Psychometric Assessment</h2>
<p>Certain conditions require standardized psychological assessments to clarify diagnosis or measure cognitive function. The centre provides evaluations including intelligence tests (IQ), personality assessments, anxiety and depression rating scales, and diagnostic assessments for ADHD and learning difficulties.</p>

<h2>Scheduling a Session</h2>
<p>You can request a counselling appointment through the <a href="@/appointment/">online appointment form</a> or by calling the clinic. Our staff will coordinate the suitable session timing.</p>
''') + cta(), [('Services', '/services/'), ('Counselling & CBT', '/service/counselling/')])

# 5. DE-ADDICTION SERVICE
page('/service/de-addiction/', 'De-Addiction Centre in Patna | Alcohol & Substance Rehabilitation', 'Evidence-based de-addiction treatment in Patna by Dr. Sachchidanand Singh. Safe medical detox, anti-craving therapy, and relapse prevention.',
head('De-Addiction & Substance Rehabilitation', 'Medically assisted recovery and compassionate guidance for overcoming substance dependence.') + prose('''
<p>Addiction is a complex, treatable brain disorder — not a moral failure or a lack of willpower. Over time, repeated substance use alters neural reward pathways, making cessation extremely challenging without structured medical guidance.</p>

<h2>Substances Treated</h2>
<ul class="tick">
  <li><strong>Alcohol Dependence:</strong> Safe management of alcohol withdrawal symptoms (tremors, insomnia, hallucinations, delirium tremens) followed by anti-craving medications and relapse-prevention therapy.</li>
  <li><strong>Tobacco & Nicotine Addiction:</strong> Pharmacotherapy (nicotine replacement, varenicline, bupropion) coupled with behavioural coping strategies.</li>
  <li><strong>Cannabis & Sedatives:</strong> Structured withdrawal tapering and psychological rehabilitation.</li>
  <li><strong>Prescription Drug Abuse:</strong> Detoxification from opioids, sleeping pills, and pain medications under medical supervision.</li>
</ul>

<h2>Our Treatment Approach</h2>
<ol>
  <li><strong>Comprehensive Medical Evaluation:</strong> Assessing the patient\'s physical health, liver function, duration of use, and co-occurring psychiatric conditions like depression or anxiety.</li>
  <li><strong>Medical Detoxification:</strong> Administering targeted medications to minimize uncomfortable withdrawal symptoms safely.</li>
  <li><strong>Anti-Craving Pharmacotherapy:</strong> Utilizing proven medications to dampen the neurological urge to use substances.</li>
  <li><strong>Family Counseling & Relapse Prevention:</strong> Educating family members on how to support long-term sobriety without triggering conflicts.</li>
</ol>
''') + cta(), [('Services', '/services/'), ('De-addiction', '/service/de-addiction/')])

# 6. CHILD & ADOLESCENT PSYCHIATRY
page('/service/child-adolescent/', 'Child & Adolescent Psychiatrist in Patna | ADHD, Anxiety & Behavioural Care', 'Child and adolescent mental health care in Patna by Dr. Sachchidanand Singh. Care for ADHD, exam stress, anger, and mood issues.',
head('Child & Adolescent Mental Health', 'Gentle, empathetic care supporting children and young people through emotional and behavioural challenges.') + prose('''
<p>Children and adolescents experience emotional struggles differently from adults. Rather than expressing sadness, a young person may show sudden academic decline, irritability, excessive defiance, social withdrawal, or physical complaints like headaches and stomach aches.</p>

<h2>Common Conditions Addressed</h2>
<ul class="tick">
  <li><strong>Attention-Deficit/Hyperactivity Disorder (ADHD):</strong> Inattention, excessive restlessness, impulsivity, and difficulty finishing tasks at school and home.</li>
  <li><strong>Exam & Academic Anxiety:</strong> Intense panic before tests, fear of failure, and chronic school refusal.</li>
  <li><strong>Adolescent Mood & Depressive Disorders:</strong> Prolonged sadness, irritability, loss of interest in hobbies, and changes in sleep or appetite.</li>
  <li><strong>Obsessive Thoughts & Rituals:</strong> Repetitive checking, excessive washing, or intrusive fears in children.</li>
  <li><strong>Screen Addiction & Sleep Disruptions:</strong> Excessive gaming or smartphone use interfering with daily functioning.</li>
</ul>

<h2>How Consultations Work</h2>
<p>Consultations are conducted in a warm, child-friendly atmosphere. Dr. Singh interacts with both the parents and the child separately and together, ensuring the young person feels heard and understood rather than blamed. Treatment emphasizes behavioural strategies, parental guidance, and school coordination, with medications considered only when strictly necessary.</p>
''') + cta(), [('Services', '/services/'), ('Child Psychiatry', '/service/child-adolescent/')])

# 7. VIDEO CONSULTATION
page('/service/video-consultation/', 'Online Video Consultation with Psychiatrist | Patna, Bihar', 'Book an online video consultation with Dr. Sachchidanand Singh for patients unable to visit the clinic in person.',
head('Online Video Consultation', 'Telemedicine mental health care from the comfort and privacy of your home.') + prose('''
<p>If travelling to Kankarbagh is difficult due to distance, medical frailty, or busy schedules, Dr. Sachchidanand Singh offers remote video consultations. Telemedicine provides accessible follow-ups and initial reviews, adhering to national telemedicine practice regulations.</p>

<h2>How to Arrange an Online Consultation</h2>
<ol>
  <li><strong>Submit a Request:</strong> Fill out the <a href="@/appointment/">online appointment form</a> or call <a href="tel:+917070474808" data-cms="phone_primary" data-cms-attr="tel">+91 70704 74808</a>.</li>
  <li><strong>Coordination by Staff:</strong> Clinic staff will contact you to explain the consultation fee, digital prescription process, and confirm a suitable video slot.</li>
  <li><strong>Secure Video Session:</strong> Connect via WhatsApp Video or Google Meet from a quiet, private room with a stable internet connection.</li>
  <li><strong>Digital Prescription:</strong> Following the consultation, an authorized digital prescription and follow-up guidance are shared directly via WhatsApp/email.</li>
</ol>

<h2>Important Guidelines</h2>
<ul>
  <li>Telemedicine is strictly for outpatient consultations and not for psychiatric emergencies. In emergency situations, visit the nearest hospital emergency department immediately.</li>
  <li>Ensure you are in a quiet, private room where you can talk openly and without interruption.</li>
</ul>
''') + cta(), [('Services', '/services/'), ('Video Consultation', '/service/video-consultation/')])

# 8. CONTACT PAGE
contact_html = '''<div class="wrap" style="padding-bottom:3rem">
  <div class="gmb-badge-row">
    <span class="gmb-badge"><svg class="ic" aria-hidden="true"><use href="#i-star"/></svg> 4.9 ★ Rating on Google & Justdial (1,600+ Reviews)</span>
    <span class="gmb-verified"><svg class="ic" aria-hidden="true"><use href="#i-verified"/></svg> Verified Google My Business Profile</span>
  </div>

  <div class="cols" style="align-items:start">
    <div>
      <ul class="clist">
        <li>[[IC_PHONE]]<div><b>Phone Numbers</b><a href="tel:+917070474808" data-cms="phone_primary" data-cms-attr="tel">+91 70704 74808</a><br><a href="tel:+919905400460" data-cms="phone_secondary" data-cms-attr="tel">+91 99054 00460</a></div></li>
        <li>[[IC_MAIL]]<div><b>Email Address</b><a href="mailto:shantineuropsychiatry@gmail.com" data-cms="clinic_email" data-cms-attr="mailto">shantineuropsychiatry@gmail.com</a></div></li>
        <li>[[IC_PIN]]<div><b>Clinic Location</b><span data-cms="clinic_address">[[ADDR]]</span></div></li>
        <li>[[IC_CLOCK]]<div><b>Consultation Hours</b><span data-cms="clinic_hours_text">Monday to Saturday<br>Morning: 9:00 am to 12:00 pm<br>Evening: 3:00 pm to 7:00 pm<br>Sunday: Closed</span><br><span class="state" id="state" style="margin:.4rem 0 0"><span class="dot"></span><span id="state-t">Checking hours</span></span></div></li>
      </ul>

      <div class="acts" style="margin-top:1.5rem">
        <a class="btn" href="https://maps.app.goo.gl/DeZgu7aFKnqsi6L69" target="_blank" rel="noopener"><svg class="ic" style="color:#fff;width:1.1rem;height:1.1rem;margin-right:.3rem" aria-hidden="true"><use href="#i-directions"/></svg> Open in Google Maps</a>
        <a class="btn alt" href="https://share.google/f71kgcyca5U7wbLtC" target="_blank" rel="noopener"><svg class="ic" style="width:1.1rem;height:1.1rem;margin-right:.3rem" aria-hidden="true"><use href="#i-google-map"/></svg> View GMB Listing</a>
        <a class="btn alt" href="https://wa.me/917070474808" target="_blank" rel="noopener"><svg class="ic" style="width:1.1rem;height:1.1rem;margin-right:.3rem" aria-hidden="true"><use href="#i-whatsapp"/></svg> WhatsApp Chat</a>
      </div>

      <div style="margin-top:1.5rem;border-top:1px solid var(--line);padding-top:1rem">
        <span style="font-size:.85rem;font-weight:600;color:var(--soft);text-transform:uppercase;letter-spacing:.03em;display:block;margin-bottom:.5rem">Connect Across Social Channels:</span>
        <div class="social-links">
          <a class="social-btn yt" href="https://www.youtube.com/@drsachchidanandsingh" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-youtube"/></svg> YouTube</a>
          <a class="social-btn fb" href="https://www.facebook.com/sachchidanand.singh.5" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-facebook"/></svg> Facebook</a>
          <a class="social-btn insta" href="https://instagram.com/drsachchi" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-instagram"/></svg> Instagram</a>
          <a class="social-btn in" href="https://in.linkedin.com/in/dr-sachchidanand-singh-28724647" target="_blank" rel="noopener"><svg class="ic" aria-hidden="true"><use href="#i-linkedin"/></svg> LinkedIn</a>
        </div>
      </div>
    </div>

    <div>
      <div class="map-responsive">
        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3598.058371190479!2d85.15366567539515!3d25.601852777451996!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39ed589a8de481fd%3A0x779c1baae8ae55d4!2sShanti%20Neuropsychiatry%20Centre%20Dr%20Sachchidanand%20Singh%20%7C%20Psychiatrist%20in%20Patna!5e0!3m2!1sen!2sin!4v1729100000000!5m2!1sen!2sin" width="100%" height="400" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Google My Business Map Location - Shanti Neuropsychiatry Centre Patna"></iframe>
      </div>
      <div class="prose" style="padding-top:1.25rem;padding-bottom:0">
        <h2>Finding the Clinic</h2>
        <p>The clinic is located on <strong>Rajni Path in PC Colony, Kankarbagh</strong>, directly in front of <strong>Savera Cancer Hospital</strong>. Landmark landmarks include PC Colony Play Ground, Doctor\'s Colony, and Old Bypass Road.</p>
        <h2>Booking Your Visit</h2>
        <p>The quickest way to book is to <a href="@/appointment/">submit an appointment request</a> online or message on WhatsApp. Staff will confirm your slot during working hours.</p>
      </div>
    </div>
  </div>
</div>'''.replace('[[IC_PHONE]]', ic('phone')).replace('[[IC_MAIL]]', ic('mail')).replace('[[IC_PIN]]', ic('pin')).replace('[[ADDR]]', ADDR).replace('[[IC_CLOCK]]', ic('clock'))

page('/contact/', 'Contact Shanti Neuropsychiatry Centre | Dr. Sachchidanand Singh, Patna', 'Phone, email, address, clinic hours, and directions for Shanti Neuropsychiatry Centre, G-37 Rajni Path, PC Colony, Kankarbagh, Patna.',
head('Contact & Visit the Clinic', 'Call, WhatsApp, or navigate to our Kankarbagh clinic via Google Maps.') + contact_html, [('Contact', '/contact/')], [CLIN])

# 9. APPOINTMENT PAGE
page('/appointment/', 'Request an Appointment | Dr. Sachchidanand Singh, Psychiatrist Patna', 'Request an in-person or video appointment with Dr. Sachchidanand Singh at Shanti Neuropsychiatry Centre, Patna. Fast confirmation.',
head('Request an Appointment', 'Takes one minute. Staff confirm your consultation time by phone during clinic hours.') + form, [('Appointment', '/appointment/')])

# 10. BLOG ARTICLES
ART = {
    'depression-is-not-just-low-mood': (
        'Depression is Not Just Low Mood',
        'Often people confuse depression with normal sadness. Depression is an enduring, treatable medical condition.',
        '''
<p>Feeling sad or disappointed is a normal part of life. Clinical depression is fundamentally different: it persists for weeks or months, impairs sleep and energy, disrupts concentration and work, and does not lift simply because someone tries to "think positive."</p>

<h2>Recognizing Common Warning Signs</h2>
<ul>
  <li>Persistent low, empty, or irritable mood lasting most of the day for two weeks or longer</li>
  <li>Marked loss of interest or pleasure in activities once enjoyed (anhedonia)</li>
  <li>Noticeable changes in appetite or unintended weight fluctuations</li>
  <li>Chronic insomnia (waking up too early) or excessive sleeping</li>
  <li>Severe physical exhaustion and slowed movement or speech</li>
  <li>Feelings of intense guilt, worthlessness, or helplessness</li>
  <li>Difficulty focusing, remembering details, or making simple decisions</li>
  <li>Recurring thoughts of death or self-harm</li>
</ul>

<h2>Why Does Depression Occur?</h2>
<p>Depression is rarely caused by a single trigger. Neurochemical imbalances involving serotonin, dopamine, and norepinephrine, genetic predisposition, chronic medical illness, severe life bereavement, and prolonged stress all interplay. It is a biological and psychological illness — not a character flaw or sign of weakness.</p>

<h2>Evidence-Based Treatment</h2>
<p>Depression is highly treatable. Modern clinical approaches combine:</p>
<ul>
  <li><strong>Pharmacotherapy:</strong> Antidepressant medications (such as SSRIs or SNRIs) prescribed by a psychiatrist help restore neurotransmitter equilibrium. They require 2 to 4 weeks to take full therapeutic effect and should never be stopped abruptly.</li>
  <li><strong>Psychotherapy & CBT:</strong> Identifying negative cognitive patterns and adopting practical behavioural activation strategies.</li>
  <li><strong>Lifestyle & Sleep Routine:</strong> Establishing circadian rhythm regularity through consistent sleep times, sunlight exposure, and light physical exercise.</li>
</ul>

<h2>If Someone is in Immediate Danger</h2>
<p><strong>If you or a loved one is having thoughts of self-harm, please seek emergency medical care immediately at the nearest hospital emergency room.</strong> Do not wait for an outpatient clinic appointment.</p>
'''
    ),
    'ocd-can-it-be-cured': (
        'Obsessive Compulsive Disorder (OCD): Can It Be Cured?',
        'OCD is a treatable neurological and psychological condition. An honest look at clinical management and recovery.',
        '''
<p>Obsessive Compulsive Disorder (OCD) is a frequently misunderstood condition often trivialized as a desire for neatness. In reality, it is a distressing neuropsychiatric condition characterized by intense unwanted thoughts and repetitive rituals.</p>

<h2>Understanding Obsessions vs Compulsions</h2>
<p><strong>Obsessions</strong> are intrusive, distressing thoughts, images, or urges that enter the mind repeatedly against one\'s will (such as fears of contamination, doubts about leaving doors unlocked, or aggressive thoughts).</p>
<p><strong>Compulsions</strong> are repetitive actions or mental rituals performed in an attempt to neutralize the anxiety caused by the obsession (such as washing hands repeatedly, checking locks, counting, or seeking reassurance).</p>

<h2>Can OCD Be Cured?</h2>
<p>In clinical medicine, psychiatrists describe OCD management in terms of <strong>remission and long-term recovery</strong> rather than a sudden "one-time cure." With evidence-based psychiatric treatment, the vast majority of patients experience significant symptom reduction, reclaiming control over their careers, education, and relationships.</p>

<h2>Proven Treatment Strategies</h2>
<ul>
  <li><strong>Cognitive Behaviour Therapy with ERP:</strong> Exposure and Response Prevention (ERP) is the gold standard psychological therapy. Guided by a trained clinician, the patient faces anxiety-provoking situations without resorting to compulsive rituals.</li>
  <li><strong>Targeted Medications:</strong> High-affinity serotonin reuptake inhibitors (SSRIs) prescribed at therapeutic doses help balance brain circuitry between the orbitofrontal cortex and basal ganglia.</li>
  <li><strong>Combined Approach:</strong> Moderate to severe OCD responds most robustly to combined medication and CBT.</li>
</ul>

<h2>When to Consult a Psychiatrist</h2>
<p>If obsessive thoughts or rituals occupy more than an hour of your day, disrupt your sleep, or impede your daily productivity, consulting a psychiatrist is the first decisive step toward recovery.</p>
'''
    ),
    'anxiety-and-panic-attacks': (
        'Anxiety and Panic Attacks: Symptoms and Recovery',
        'Understanding generalized anxiety, sudden panic attacks, physical symptoms, and practical recovery steps.',
        '''
<p>Anxiety is the body\'s natural fight-or-flight response to perceived threat. However, when anxiety becomes constant, disproportionate, or occurs without an apparent reason, it transforms into an anxiety disorder that drains energy and disrupts life.</p>

<h2>Symptoms of a Panic Attack</h2>
<p>A panic attack is a sudden surge of overwhelming fear that peaks within minutes, often accompanied by alarming physical sensations:</p>
<ul>
  <li>Rapid, pounding heartbeat (palpitations)</li>
  <li>Shortness of breath or feeling smothered</li>
  <li>Chest tightness or pain (often mistaken for a heart attack)</li>
  <li>Trembling, shaking, or profuse sweating</li>
  <li>Dizziness, lightheadedness, or feeling detached from reality (depersonalization)</li>
  <li>Fear of losing control or impending doom</li>
</ul>

<h2>Why Panic Attacks Happen</h2>
<p>During a panic attack, the amygdala (the brain\'s alarm center) misfires, flooding the bloodstream with adrenaline even when no physical danger exists. While intensely frightening, panic attacks are not physically dangerous to the heart and typically subside within 15 to 30 minutes.</p>

<h2>Medical & Psychological Management</h2>
<ul>
  <li><strong>Immediate Coping:</strong> Grounding exercises (the 5-4-3-2-1 technique) and slow diaphragmatic breathing to signal safety to the nervous system.</li>
  <li><strong>Psychiatric Assessment:</strong> Ruling out thyroid disorders, vitamin deficiencies, or caffeine-induced symptoms.</li>
  <li><strong>Pharmacotherapy:</strong> Short-term anxiolytics and longer-term SSRIs to stabilize autonomic reactivity.</li>
  <li><strong>CBT & Interoceptive Exposure:</strong> Helping the mind understand that physical sensations of anxiety are safe and manageable.</li>
</ul>
'''
    ),
    'sleep-and-mental-health': (
        'Sleep and Mental Health: Breaking the Insomnia Cycle',
        'How chronic sleep disturbance and mental health disorders reinforce each other, and practical steps for restful sleep.',
        '''
<p>Sleep and psychiatric wellbeing share an intimate, bidirectional relationship. Poor sleep can trigger or worsen depression, anxiety, and bipolar episodes, while emotional distress frequently manifests as chronic insomnia.</p>

<h2>The Different Types of Sleep Disturbances</h2>
<ul>
  <li><strong>Sleep-Onset Insomnia:</strong> Lying awake for hours with a racing mind, unable to fall asleep.</li>
  <li><strong>Sleep-Maintenance Insomnia:</strong> Waking up multiple times throughout the night and struggling to return to sleep.</li>
  <li><strong>Early Morning Awakening:</strong> Waking at 3 or 4 am with a heavy sense of dread or sadness, a hallmark symptom of clinical depression.</li>
  <li><strong>Hypersomnia:</strong> Sleeping excessively during the day yet still feeling exhausted.</li>
</ul>

<h2>Breaking the Insomnia Cycle: Sleep Hygiene Essentials</h2>
<ol>
  <li><strong>Maintain a Consistent Wake Time:</strong> Wake up at the exact same time every morning, including weekends. This anchors your circadian rhythm.</li>
  <li><strong>Protect the Bed for Sleep Only:</strong> Avoid working, eating, or watching screens in bed. Your brain should associate the mattress exclusively with rest.</li>
  <li><strong>Limit Blue Light Exposure:</strong> Turn off bright screens and mobile phones at least one hour before bedtime.</li>
  <li><strong>Avoid Caffeine after 3 PM:</strong> Caffeine has a half-life of 5 to 7 hours and impairs deep slow-wave sleep.</li>
</ol>

<h2>When to Seek Professional Evaluation</h2>
<p>If sleep problems persist for more than three weeks and impair your concentration, mood, or daytime functioning, consult a neuropsychiatrist. Non-habit-forming sleep regulators and CBT for Insomnia (CBT-I) provide lasting relief without dependency.</p>
'''
    )
}

page('/blogs/', 'Mental Health Articles & Guides | Shanti Neuropsychiatry Centre, Patna', 'Educational psychiatric articles on depression, anxiety, OCD, panic disorder, and sleep by Dr. Sachchidanand Singh.',
head('Mental Health Articles', 'Reliable, evidence-based mental health education by Dr. Sachchidanand Singh.') +
'<div class="wrap"><ul class="plist">' + ''.join('<li><h2><a href="@/blog/%s/">%s</a></h2><p>%s</p></li>' % (s, t, d) for s, (t, d, b) in ART.items()) + '</ul></div>',
[('Articles', '/blogs/')])

for s, (t, d, b) in ART.items():
    rev = 'Clinically reviewed by %s.' % REVIEWED_BY
    page('/blog/%s/' % s, t + ' | Shanti Neuropsychiatry Centre, Patna', d,
         head(t, d) + prose(b + '<p class="rev">%s This article is for informational purposes and does not replace a clinical consultation.</p>' % rev),
         [('Articles', '/blogs/'), (t, '/blog/%s/' % s)],
         [{"@type": "Article", "headline": t, "description": d, "author": {"@type": "Person", "name": "Dr. Sachchidanand Singh"}, "publisher": {"@id": DOM + "/#clinic"}, "mainEntityOfPage": DOM + '/blog/%s/' % s}])
    PAGES[-1] = PAGES[-1]

# 11. LEGAL PAGES
LEG = {
    'privacy': (
        'Privacy Policy',
        'How Shanti Neuropsychiatry Centre protects your personal and medical information.',
        '''
<p>Shanti Neuropsychiatry Centre respects your privacy. This policy outlines how information is collected and handled across our website and clinical channels.</p>
<h2>Online Request Form</h2>
<p>When you complete the appointment request form on this website, your name, telephone number, and preferred date are processed in your browser to generate a direct WhatsApp message and log your slot request in the clinic database. We do not require or ask for sensitive medical history on this form.</p>
<h2>Medical Confidentiality</h2>
<p>All clinical evaluations, diagnosis reports, and treatment notes generated during your consultation with Dr. Sachchidanand Singh are strictly confidential and governed by Indian Medical Council professional conduct guidelines. Records are never disclosed to third parties without your written authorization.</p>
<h2>Cookies & Analytics</h2>
<p>This website operates without intrusive tracking cookies or commercial ad trackers. Standard Google Fonts and map assets are loaded securely over HTTPS.</p>
'''
    ),
    'terms': (
        'Terms of Service',
        'Website terms of use and clinical consultation policies.',
        '''
<p>This website is provided by Shanti Neuropsychiatry Centre, Patna for patient information and appointment scheduling.</p>
<h2>No Doctor–Patient Relationship Prior to Consultation</h2>
<p>Browsing this website, submitting an appointment request, or messaging on WhatsApp does not constitute a formal doctor–patient relationship. That relationship begins solely when an in-person or verified telemedicine clinical assessment takes place.</p>
<h2>Appointment Requests vs Booked Visits</h2>
<p>Online appointment submissions represent scheduling requests. Your consultation time is finalized once our clinic administration speaks with you to confirm availability.</p>
<h2>Emergency Services Disclaimer</h2>
<p>This website, its online forms, and WhatsApp are not emergency response channels. If you are experiencing an acute medical or psychiatric emergency, proceed immediately to the nearest hospital emergency room.</p>
'''
    ),
    'accessibility': (
        'Accessibility Statement',
        'Our commitment to ensuring this website is accessible to all individuals.',
        '''
<p>We are committed to making mental health resources accessible to all patients, including individuals with disabilities or sensory impairments.</p>
<h2>Accessibility Features Implemented</h2>
<ul>
  <li>Full keyboard navigation across all interactive buttons, links, and forms</li>
  <li>High-contrast text compliant with WCAG 2.2 AA visual standards</li>
  <li>Scalable text supporting up to 200% zoom without horizontal scroll clipping</li>
  <li>Screen-reader friendly semantic markup and ARIA live validation regions on forms</li>
  <li>Reduced-motion support respecting user operating system preferences</li>
</ul>
<p>If you experience any accessibility difficulty, please contact us at <a href="mailto:shantineuropsychiatry@gmail.com">shantineuropsychiatry@gmail.com</a>.</p>
'''
    ),
    'medical-disclaimer': (
        'Medical Disclaimer',
        'Important medical disclosure regarding health information on this website.',
        '''
<p>The information on this website is published for general educational and informational awareness only. It does not provide medical diagnosis, individual treatment plans, or personal clinical advice.</p>
<h2>Consult a Qualified Physician</h2>
<p>Never disregard professional medical advice or delay seeking evaluation because of information you have read on this website. Always consult a qualified psychiatrist regarding personal psychiatric symptoms or medication questions.</p>
<h2>Medication Safety</h2>
<p>Never initiate, modify doses of, or discontinue any psychotropic medicine without explicit supervision from the prescribing medical practitioner.</p>
'''
    )
}

for s, (t, d, b) in LEG.items():
    page('/%s/' % s, t + ' | ' + CLINIC, d, head(t, d) + prose(b), [(t, '/%s/' % s)])

# SITEMAP, ROBOTS, AND REDIRECTS
if '/' in PAGES:
    PAGES.remove('/')
    PAGES.insert(0, '/')

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('<url><loc>%s%s</loc></url>\n' % (DOM, p) for p in PAGES) + '</urlset>\n'
open(ROOT + '/sitemap.xml', 'w').write(sm)
open(ROOT + '/robots.txt', 'w').write(('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % DOM) if LAUNCH else 'User-agent: *\nDisallow: /\n')

OLD = 'lorem-ipsum-dolor-sit-amet-consectetur-adipisicing-elittempore'
RD = [
    ('/blog/%s-minus' % OLD, '/blog/depression-is-not-just-low-mood/'),
    ('/blog/%s' % OLD, '/blog/ocd-can-it-be-cured/'),
    ('/service/video-consultation-45', '/service/video-consultation/'),
    ('/gallery', '/'),
    ('/blogs', '/blogs/'),
    ('/about', '/about/'),
    ('/contact', '/contact/')
]
open(ROOT + '/_redirects', 'w').write('# Netlify / Cloudflare Pages\n' + ''.join('%s %s 301\n' % a for a in RD[:4]))
open(ROOT + '/.htaccess', 'w').write('# Apache\nErrorDocument 404 /404.html\nDirectoryIndex index.html\nOptions -Indexes\n<IfModule mod_rewrite.c>\nRewriteEngine On\n' + ''.join('RewriteRule ^%s/?$ %s [R=301,L]\n' % (a.strip('/'), b) for a, b in RD[:4]) + '</IfModule>\n')
open(ROOT + '/vercel.json', 'w').write(json.dumps({"cleanUrls": False, "trailingSlash": True, "redirects": [{"source": a, "destination": b, "permanent": True} for a, b in RD[:4]]}, indent=1))

# 404 PAGE
p404 = open(ROOT + '/blogs/index.html').read()
p404 = re.sub(r'<title>.*?</title>', '<title>Page not found | %s</title>' % CLINIC, p404)
p404 = re.sub(r'<main.*?</main>', '<main id="main" class="nf wrap"><h1>That page is not here</h1><p>The address may have changed. Try one of these:</p><p class="acts"><a class="btn" href="/">Home</a><a class="btn alt" href="/appointment/">Request an appointment</a><a class="btn alt" href="tel:+917070474808">Call +91 70704 74808</a></p></main>', p404, flags=re.S)
p404 = re.sub(r'<link rel="canonical"[^>]*>', '', p404)
p404 = re.sub(r'<script type="application/ld\+json">.*?</script>', '', p404, flags=re.S)
p404 = re.sub(r'<nav class="crumbs.*?</nav>', '', p404, flags=re.S)
p404 = p404.replace('href="../', 'href="/').replace('src="../', 'src="/')
open(ROOT + '/404.html', 'w').write(p404)

print('Built', len(PAGES), 'pages | mode:', 'LAUNCH (Production Ready)' if LAUNCH else 'STAGING (noindex)')
