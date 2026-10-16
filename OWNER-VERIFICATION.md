# Owner verification: facts that conflict or are unconfirmed

Sources checked: the HTTrack clone (109 files, nothing executed), your project plan and master prompt, and on 15 Oct 2026 the Practo profile, plus search snippets from Lybrate, ThreeBestRated and DocIndia.
**Not accessible:** LinkedIn and the Google share link both refused automated access. The live site was not re-crawled; only the clone was read. Google Business Profile owner data was not seen.

## A. Decide before launch (these change what the public sees)

| # | Conflict | What the site shows now | Decision needed |
|---|---|---|---|
| 1 | Header call icon on the old site dials `+91 62003 05580`, shown nowhere as a clinic number. The same number is the WhatsApp link beside "Developed by Pushpaje". | Not used anywhere. | Whose number is it? |
| 2 | Old WhatsApp link was `wa.me/7070474808` (no country code, likely broken). | `917070474808` | Is 7070474808 on WhatsApp? Which number should patients message? |
| 3 | Two numbers: 7070474808 and 9905400460. | Both listed as phone. | Confirm both are public. |
| 4 | **Experience:** old site meta and Practo bio say 11 years; Practo header says 15 years overall (9 as specialist); Lybrate says 20; ThreeBestRated says 15+. | No experience figure shown. | One verified figure, or none. |
| 5 | **Hours:** old site Mon to Sat 9-12 and 3-7. Practo: Mon to Sat 10-12 and 3-6, plus Sunday 12-3. Lybrate: 9:30-12 and 3-6. | Old site's hours (clinic's own). Sunday treated as closed in the form. | Confirm real hours, including Sunday. This also drives the open/closed indicator and the form's Sunday check. |
| 6 | **Fee:** Practo shows 800 rupees, Lybrate 700. | No fee shown. | Publish a fee or leave it out. |
| 7 | **Address:** old site G-37 Rajni Path, in front of Savera Cancer Hospital; DocIndia lists "CC/82, P C Colony". Practo's map pin differs from the old site's map. | G-37 Rajni Path. Maps link searches by name. | Confirm address and the exact Google Maps pin. |
| 8 | **Title:** old site and ThreeBestRated say Assistant Professor of Psychiatry at Patna Medical College (current). Practo lists only Senior Resident posts, 2013-2015 CIP and 2015-2018 PMCH. | Not claimed. | Confirm current post. |
| 9 | **MBBS year:** 2006 (Practo list, DocIndia) vs 2007 (Practo bio). | Year omitted. | Confirm. |
| 10 | Bihar Medical Council registration 37058 (2007) and memberships (Indian Psychiatric Society, IMA) appear on Practo. | Not published. | Approve publishing, if correct. |
| 11 | Titles on Practo: Neuropsychiatrist, Psychiatrist, Addiction Psychiatrist, Sexologist. | "Consultant psychiatrist". | Choose the titles you want used. |
| 12 | "More than 12,000 satisfied patients", "24/7 Support", "world class" wording. | Removed. | Evidence or drop. |
| 13 | Three old testimonials (all avatar "SP"; two nearly identical). Practo shows 64 patient stories (97%) and a 5.0 rating. | None shown. | Consent and permission before any are reproduced. |
| 14 | "Ved Medicare" pharmacy association. | Removed. | Confirm relationship and disclosure. |
| 15 | Old FAQ had five questions with no answers. | No FAQ page. | Doctor writes answers. |
| 16 | Old `/contact` form had Name, Username, Phone, Subject, Message; no destination found in the clone. | Replaced by the appointment form. | Where did those messages go? |
| 17 | Old `/gallery` was empty. Old `/service/video-consultation-45` duplicated video consultation. | `/gallery` and `-45` 301-redirect. | Approve the redirects. |

## B. Content that needs the doctor's sign-off
- Both articles (depression, OCD) are rewritten from the old pages: no statistics, no cure promises, no medicine advice. They carry the visible line "Clinician review pending". Dr. Singh must read and approve them, then set `REVIEWED_BY` in `tools/build.py`.
- The About page, service wording and the "what happens next" steps (staff follow up by phone) are drafted from the old site and Practo. Please confirm they match how the clinic works.
- Conditions list on About includes "alcohol and drug use problems", taken from the Practo profile. Confirm.
- Counselling: who provides it and how long sessions run is not stated anywhere I could find.

## C. Images
No real photographs of the doctor or clinic were obtainable here. The old site's images were Hygraph-hosted (not in the clone), cartoon clip-art and two stock photos; none was reused. Practo clinic photos are hosted by Practo. **Supply your own photos with permission**, and I will place them. Current visuals: your logo, emblem, favicons and an SVG icon set.

## D. What this build does not include
- Appointment requests are not saved anywhere. The form prepares a WhatsApp message that the patient must press Send on. There is no Google Sheet, Apps Script, server, or automatic notification to the doctor. The privacy notice says exactly this.
- No Hindi version, no gallery, no testimonials, no FAQ page, no Google Business Profile changes.
- Fonts load from Google Fonts. Self-hosting them is recommended for privacy and speed.
