# -*- coding: utf-8 -*-
"""
CU Assistant — conversational engine.
Hybrid AI: weighted keyword + fuzzy intent matching over a rich CU knowledge
base, with context-aware follow-ups. If GROQ_API_KEY / OPENAI_API_KEY is set in
the environment it can optionally route through an LLM (OpenAI-compatible API)
and fall back to this engine on any error.
"""
import os
import re
import json
import random
import datetime
import urllib.request
from difflib import SequenceMatcher

from . import knowledge as K

# ------------------------------------------------------------------- helpers
STOP = set("a an the is are was were i me my we you your to of for on in at and "
           "or do does did how what when where who why can could would should i'm "
           "im its it this that about tell give know want need get let please "
           "with from as be been being am there here hi hello hey yes no not".split())

def norm(t: str) -> str:
    t = t.lower().strip()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def tokens(t: str):
    return [w for w in norm(t).split() if w not in STOP]

def has(text_norm, *phrases):
    """True if any phrase appears in normalized text."""
    return any(p in text_norm for p in phrases)

# ------------------------------------------------------------------ LLM hook
SYSTEM_PROMPT = (
    "You are 'CU Assistant', a friendly, accurate campus assistant for Chandigarh "
    "University (CU), Gharuan, Mohali, Punjab — established 2012, NAAC A+, official "
    "website https://www.cuchd.in. Answer ONLY about Chandigarh University: admissions, "
    "CUCET entrance exam, courses/schools, fees, scholarships, placements, hostels, "
    "campus facilities, transport, student portal CUIMS (uims.cuchd.in), contacts "
    "(helpline +91-160-3044444, admissions@cuchd.in). Be concise, use short markdown "
    "bullet points. If unsure about a figure, say it is indicative and tell them to "
    "verify at cuchd.in. Never invent statistics. For unrelated topics, gently say you "
    "specialize in Chandigarh University and suggest topics you can help with."
)

def llm_answer(message: str):
    """Optional OpenAI-compatible LLM (Groq / OpenAI). Returns str or None."""
    api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    if os.environ.get("GROQ_API_KEY"):
        url, model = "https://api.groq.com/openai/v1/chat/completions", "llama-3.3-70b-versatile"
    else:
        url, model = "https://api.openai.com/v1/chat/completions", os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message[:2000]},
        ],
        "temperature": 0.4,
        "max_tokens": 700,
    }).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=25) as r:
        data = json.loads(r.read().decode())
    return data["choices"][0]["message"]["content"]

# ------------------------------------------------------------------ answers
def a_about():
    return (
        "🏛️ **About Chandigarh University**\n\n"
        "- **Established:** 2012 — one of India's fastest-growing young universities\n"
        "- **Location:** NH-95, Gharuan, Mohali (Punjab), on the Chandigarh–Ludhiana highway\n"
        "- **Accreditation:** NAAC **A+** grade\n"
        "- **Campus:** Sprawling 200+ acre green, Wi-Fi-enabled, eco-friendly residential campus\n"
        "- **Community:** 40,000+ students from all Indian states and **40+ countries**\n"
        "- **Ranked** among India's top private universities in NIRF & QS rankings\n\n"
        "CU offers programs in engineering, business, computing, law, pharmacy, agriculture, "
        "design, hotel management, media, health sciences, animation and liberal arts — "
        "with strong placements, research and international tie-ups.",
        ["Admissions process", "Courses & schools", "Placements", "How to reach campus"]
    )

def a_admission():
    return (
        "🎓 **Admission Process at Chandigarh University**\n\n"
        "**Step 1 — Apply:** Register for **CUCET** (Chandigarh University Common Entrance "
        "Test) online at [cuchd.in/cucet](" + K.LINKS["cucet"] + ") or apply via the "
        "[admissions portal](" + K.LINKS["admissions"] + ").\n\n"
        "**Step 2 — Appear for CUCET:** An online MCQ test. Your CUCET score decides both "
        "admission and scholarship (up to 100% tuition waiver). Some programs also accept "
        "JEE / CAT / CLAT / NATA scores.\n\n"
        "**Step 3 — Counselling & merit:** Shortlisted candidates get counselling dates for "
        "branch/program allotment.\n\n"
        "**Step 4 — Confirm seat:** Pay the seat-confirmation/fee online and upload documents.\n\n"
        "**Documents to keep ready:** 10th & 12th marksheets, entrance scorecard, Aadhaar/ID, "
        "passport photos, migration/character certificate, and category/sports certificates if any.\n\n"
        "🟢 Admissions for the 2026–27 batch are open — the earlier you appear in CUCET, the "
        "better the scholarship slabs.",
        ["CUCET exam pattern", "Scholarships", "Fees structure", "Hostel booking"]
    )

def a_cucet():
    return (
        "📝 **All about CUCET**\n\n"
        "- **What it is:** Chandigarh University Common Entrance Test — the gateway for admission "
        "**and** scholarships across most UG & PG programs.\n"
        "- **Mode:** Online computer-based test (you can appear from home with remote proctoring "
        "or at a test centre).\n"
        "- **Format:** ~100 multiple-choice questions in around 120 minutes — sections typically "
        "include English, general awareness, quantitative aptitude/reasoning and a domain subject "
        "related to your program.\n"
        "- **Marking:** +1 per correct answer; **no negative marking** (so attempt everything!).\n"
        "- **Phases:** CUCET runs in phases through the year; early phases generally offer the "
        "best scholarship slabs.\n"
        "- **Result & scholarship:** Score-based merit slabs give fee waivers from modest "
        "percentages up to **100% tuition** for top scorers.\n\n"
        "Register & take a free mock at [cuchd.in/cucet](" + K.LINKS["cucet"] + ").",
        ["Scholarships", "Admissions process", "Eligibility for B.Tech", "Apply now"]
    )

def a_courses():
    schools = "\n".join(f"- {s}" for s in K.SCHOOLS)
    return (
        "📚 **Programs & Schools at CU**\n\n"
        f"{schools}\n\n"
        "Popular choices include **B.Tech (CSE & specializations like AI/ML, Data Science, Cyber "
        "Security)**, **BCA/MCA**, **BBA/MBA**, **B.Com (Hons)**, **BA LLB / BBA LLB**, "
        "**B.Pharm**, **B.Sc Agriculture**, **B.Des**, **Hotel Management**, **BJMC** and "
        "**B.Sc Nursing**.\n\n"
        "💬 Ask me about any specific course, e.g. *\"Tell me about B.Tech CSE\"* or *\"MBA details\"* — "
        "I'll give duration, eligibility, entrance, fees and careers.",
        ["B.Tech CSE details", "MBA details", "BCA details", "Fees structure"]
    )

def a_fees(course=None):
    if course:
        return (
            f"💰 **Fees — {course['name']}**\n\n"
            f"- **Tuition:** {course['fee']} (indicative annual)\n"
            "- Plus a refundable caution deposit (~₹2,000 one-time) and exam/incidental charges\n"
            "- **Scholarships via CUCET can cut the tuition substantially — even up to 100%**\n"
            "- Hostel + mess, if opted, is roughly ₹95,000 – ₹1,50,000 per year\n\n"
            "Get the exact official fee slip on the [fee structure page](" + K.LINKS["fees"] + ").",
            ["Scholarships", "Hostel fees", "Admissions process"]
        )
    rows = "\n".join(f"- **{c['name'].split('—')[0].strip()}**: {c['fee']}" for c in K.COURSES)
    body = (
        "💰 **Indicative Tuition Fees (per year)**\n\n"
        f"{rows}\n\n"
        "- A refundable caution money (~₹2,000) and exam charges are extra.\n"
        "- Fees are revised slightly every year — **CUCET scholarships can reduce tuition by "
        "a big margin, up to 100% for top scorers.**\n"
        "- Pay fees online through the student portal once admitted.\n\n"
        "Exact official figures: [cuchd.in fee structure](" + K.LINKS["fees"] + ")."
    )
    return body + K.DISCLAIMER, ["Scholarships", "Hostel fees", "CUCET exam pattern"]

def a_scholarship():
    items = "\n".join(f"- **{name}:** {desc}" for name, desc in K.SCHOLARSHIPS)
    return (
        "🎖️ **Scholarships at Chandigarh University**\n\n"
        f"{items}\n\n"
        "💡 **Pro tip:** The CUCET score is the single biggest scholarship lever — prepare well "
        "and appear in the earliest phase. Details & apply: [cuchd.in/scholarships]("
        + K.LINKS["scholarships"] + ").",
        ["CUCET exam pattern", "Fees structure", "Admissions process"]
    )

def a_placement():
    stats = "\n".join(f"- {s}" for s in K.PLACEMENT_STATS)
    rec = ", ".join(K.TOP_RECRUITERS[:24])
    body = (
        "💼 **Placements at CU**\n\n"
        f"{stats}\n\n"
        f"**Top recruiters include:** {rec}, and many more.\n\n"
        "The university's **Department of Career Development** runs aptitude training, mock "
        "interviews, coding practice (HackerRank/CodeChef chapters), resume workshops and "
        "industry internships from the second year onwards.\n\n"
        "See placement records: [cuchd.in/placements](" + K.LINKS["placements"] + ")."
    )
    return body + K.DISCLAIMER, ["B.Tech CSE details", "MBA details", "Scholarships"]

def a_hostel():
    h = K.HOSTEL_INFO
    return (
        "🏨 **Hostel & Residential Life**\n\n"
        f"- **Stay:** {h['overview']}\n"
        f"- **Rooms:** {h['rooms']}\n"
        f"- **Mess:** {h['mess']}\n"
        f"- **Fees:** {h['fee']}\n"
        f"- **Amenities:** {h['amenities']}\n"
        f"- **Booking:** {h['booking']}\n\n"
        "Day scholars can use university bus transport instead. Details: "
        "[hostel page](" + K.LINKS["hostel"] + ").",
        ["Transport facilities", "Campus facilities", "Fees structure"]
    )

def a_facilities():
    items = "\n".join(f"- {name}: {desc}" for name, desc in K.FACILITIES)
    return (
        "🏫 **Campus Facilities**\n\n"
        f"{items}\n\n"
        "The campus also has open-air theatres, seminar halls, incubation/entrepreneurship "
        "cells, maker spaces and dozens of student clubs (coding, robotics, music, dance, "
        "photography, NCC/NSS…).",
        ["Hostel life", "Transport facilities", "Events & fests"]
    )

def a_transport():
    return (
        "🚌 **Transport Facility**\n\n"
        "- CU runs a large fleet of buses covering **Chandigarh (Tricity), Mohali, Kharar, "
        "Panchkula, Zirakpur, Ludhiana, Ambala, Ropar** and surrounding towns.\n"
        "- Buses run fixed morning/evening schedules as per the academic timetable.\n"
        "- Transport is charged annually/semester-wise — opt in at the time of admission.\n"
        "- Route & fee details are shared by the transport office after enrolment; students "
        "can also use local CTU buses and auto/cab services to Kharar/Gharuan.\n\n"
        "Many students also choose in-campus **hostel** stay to skip the commute.",
        ["Hostel life", "How to reach campus", "Admissions process"]
    )

def a_cuims():
    return (
        "🖥️ **Student Portal — CUIMS & Student Email**\n\n"
        "- **CUIMS** (Chandigarh University Information Management System) is the student "
        "portal: [uims.cuchd.in](" + K.LINKS["cuims"] + ")\n"
        "- On CUIMS you can view **attendance, timetable, results/marks, fee receipts, "
        "assignments, library account** and download certificates.\n"
        "- Every student gets an official **@cumail.in** email ID used for all university "
        "communication and free access to tools like Microsoft 365.\n"
        "- Login credentials are shared at enrolment; use the 'Forgot Password' option on the "
        "portal if locked out, or contact your department office.\n\n"
        "Attendance rule to remember: **75% is mandatory** in every course to appear in "
        "end-semester exams.",
        ["Attendance rules", "Results & exams", "Contact & helpline"]
    )

def a_contact():
    c = K.CONTACT
    reach = "\n".join(f"- {r}" for r in c["reach"])
    return (
        "📞 **Contact Chandigarh University**\n\n"
        f"- **Address:** {c['address']}\n"
        f"- **Admission helpline:** {c['phone']}\n"
        f"- **Email:** {c['email_admissions']} • {c['email_info']}\n"
        f"- **Website:** [{c['website']}]({K.LINKS['website']})\n\n"
        "**Reaching the campus:**\n"
        f"{reach}\n\n"
        "For grievances, you can also use the grievance cell / anti-ragging helpline shared "
        "with students at orientation.",
        ["Admissions process", "How to reach campus", "Hostel life"]
    )

def a_attendance():
    return (
        "📅 **Attendance & Academic Rules**\n\n"
        "- **75% attendance is compulsory** in every course (UGC pattern) to be eligible for "
        "end-semester examinations — detainment for shortage is enforced strictly.\n"
        "- Leave applications (medical or otherwise) must be submitted through CUIMS / HOD "
        "approval; medical leave needs a valid certificate.\n"
        "- Academics run in a **semester pattern** (two semesters per year) with mid-semester "
        "tests (MSTs), quizzes/assignments for internal marks, and end-semester exams.\n"
        "- Results are published on **CUIMS**; re-evaluation/supplementary exams are available "
        "as per the academic calendar.\n\n"
        "Tip: track attendance weekly on CUIMS — don't wait for the warning notice!",
        ["CUIMS student portal", "Results & exams", "Hostel life"]
    )

def a_results():
    return (
        "📄 **Results, Exams & Certificates**\n\n"
        "- Mid-semester and end-semester results are published on **CUIMS** "
        "([uims.cuchd.in](" + K.LINKS["cuims"] + ")) under the Exams/Results section.\n"
        "- Date sheets and admit cards are also released on CUIMS before each exam phase.\n"
        "- Provisional degree/character certificates and migration are applied for through the "
        "examination branch after final results.\n"
        "- Transcripts/verification for higher studies or jobs are issued by the examination "
        "branch (apply via CUIMS or the exam office).\n\n"
        "Forgot your CUIMS password? Use 'Forgot Password' on the portal or contact your "
        "department coordinator.",
        ["CUIMS student portal", "Attendance rules", "Contact & helpline"]
    )

def a_international():
    return (
        "🌍 **International Students & Global Exposure**\n\n"
        "- CU hosts students from **40+ countries**, with a dedicated **International Student "
        "Desk** for visa letters, FRRO support, arrival pickup and onboarding.\n"
        "- **Semester exchange / summer school / credit transfer** programs with partner "
        "universities in the USA, UK, Canada, Australia, Europe and South-East Asia.\n"
        "- English-taught programs, international faculty visits and global internship pathways "
        "are available.\n\n"
        "Aspirants abroad can apply via [cuchd.in/international](" + K.LINKS["international"] + ") "
        "or write to the international office linked there.",
        ["Admissions process", "Hostel life", "Contact & helpline"]
    )

def a_events():
    return (
        "🎉 **Campus Life, Fests & Clubs**\n\n"
        "- CU hosts a grand **annual cultural & tech fest** with celebrity performances, plus "
        "department-level tech fests, hackathons and robotics competitions through the year.\n"
        "- **100+ student clubs**: coding & robotics, AI/ML, music, dance, drama, photography, "
        "literary, entrepreneurship (E-Cell), NCC, NSS and more.\n"
        "- Inter-university **sports meets**, basketball/football leagues, and state/national "
        "level tournaments on campus.\n"
        "- Regular industry expert talks, TEDx-style events and startup demo days.\n\n"
        "Club recruitment happens in the first month of the academic year — watch the notice "
        "boards and CUIMS announcements!",
        ["Campus facilities", "Placements", "Hostel life"]
    )

def a_ragging():
    return (
        "🛡️ **Anti-Ragging & Student Safety**\n\n"
        "- Chandigarh University has a **zero-tolerance anti-ragging policy** as per UGC "
        "regulations; ragging of any kind is strictly prohibited.\n"
        "- An anti-ragging committee and squads operate across hostels and academic blocks, "
        "especially during the first weeks of the session.\n"
        "- Every student and parent submits an anti-ragging affidavit at admission.\n"
        "- **Report instantly:** tell your warden/HOD, or use the helpline numbers shared at "
        "orientation; complaints are treated confidentially.\n\n"
        "Campus security and CCTV coverage run 24×7, including hostel areas.",
        ["Hostel life", "Contact & helpline", "Campus facilities"]
    )

def a_apply():
    return (
        "✅ **How to Apply Right Now**\n\n"
        "1. Open [cuchd.in/cucet](" + K.LINKS["cucet"] + ") and click **Register / Apply Now**.\n"
        "2. Fill your basic details and choose your program.\n"
        "3. Pay the registration fee (if applicable) and book your CUCET slot.\n"
        "4. Take the test online, then watch your dashboard for the result & scholarship slab.\n"
        "5. Complete counselling, pay the admission fee and upload documents.\n\n"
        "Need human help? Call **+91-160-3044444** or email "
        "[admissions@cuchd.in](mailto:admissions@cuchd.in).",
        ["CUCET exam pattern", "Scholarships", "Documents needed?"]
    )

def a_capabilities():
    return (
        "🤖 **What I can help you with**\n\n"
        "- 🎓 Admissions & the **CUCET** entrance exam (process, pattern, dates, documents)\n"
        "- 📚 Courses, schools, eligibility, duration & career options\n"
        "- 💰 Fee structure & 🎖️ scholarships\n"
        "- 💼 Placements, recruiters & training\n"
        "- 🏨 Hostels, 🚌 transport & 🏫 campus facilities\n"
        "- 🖥️ CUIMS student portal, attendance rules, results & exams\n"
        "- 📞 Contacts, directions to campus, international students, fests, safety\n\n"
        "I also do small talk — ask me for a joke or a motivational quote! "
        "Use the 🎤 mic button to talk to me and the 🔊 button to hear my answers.",
        ["Admissions process", "Fees structure", "Placements"]
    )

# ----------------------------------------------------------------- intents
# Each: id, phrases (substring on normalized text), answer fn
INTENTS = [
    ("greeting",
     ["hi", "hello", "hey", "good morning", "good evening", "good afternoon",
      "namaste", "yo", "hiya"],
     None),
    ("goodbye", ["bye", "goodbye", "good night", "see you", "later", "exit", "quit"], None),
    ("thanks", ["thank", "thanks", "thankyou", "shukriya", "dhanyavad", "appreciate"], None),
    ("about", ["about cu", "about chandigarh", "about university", "about the university",
               "chandigarh university kya", "university history", "naac", "ranking",
               "nirf", "established", "founded", "which university", "cu kya hai"], a_about),
    ("admission", ["admission", "apply", "enrol", "enroll", "registration", "register",
                   "kaise le", "how to get admission", "eligib", "counselling", "counseling",
                   "documents", "seat", "intake", "eligibility criteria"], a_admission),
    ("cucet", ["cucet", "entrance exam", "entrance test", "exam pattern", "mock test",
               "entrance test pattern", "syllabus for entrance"], a_cucet),
    ("courses", ["course", "program", "degree", "branch", "school", "department",
                 "konse course", "which courses", "streams", "study options", "subjects offered",
                 "ug programs", "pg programs"], a_courses),
    ("fees", ["fee", "fees", "tuition", "cost", "price", "kitna", "charge", "payment",
              "pay fees", "fee structure", "kitni fee", "expense"], None),  # context-aware
    ("scholarship", ["scholarship", "scholarships", "concession", "fee waiver", "discount on fee",
                     "financial aid", "free seat", "merit scholarship"], a_scholarship),
    ("placement", ["placement", "job", "package", "recruiter", "company", "salary",
                   "internship", "career", "highest package", "employ", "hire", "hiring"], a_placement),
    ("hostel", ["hostel", "room", "mess", "rahat", "stay on campus", "living campus",
                "accommodation", "hostel fee", "dorm"], a_hostel),
    ("facilities", ["facility", "facilities", "gym", "library", "wifi", "wi fi", "lab",
                    "cafeteria", "food court", "sports", "campus life", "medical", "atm",
                    "bank", "infrastructure"], a_facilities),
    ("transport", ["transport", "bus", "commute", "travel from", "pickup", "cab"], a_transport),
    ("cuims", ["cuims", "student portal", "student login", "uims", "cumail", "student email",
               "login portal"], a_cuims),
    ("attendance", ["attendance", "75", "leave application", "short attendance", "bunk"],
     a_attendance),
    ("results", ["result", "results", "marksheet", "transcript", "certificate", "degree milega",
                 "exam date", "datesheet", "admit card", "re evaluation"], a_results),
    ("international", ["international student", "foreign student", "exchange program",
                       "study abroad", "credit transfer", "abroad", "nri", "visa"], a_international),
    ("events", ["fest", "event", "club", "celebration", "party", "cultural", "hackathon",
                "competition", "tedx"], a_events),
    ("safety", ["ragging", "raging", "safety", "security", "harass", "bullying"], a_ragging),
    ("apply", ["apply now", "how do i apply", "where to apply", "application form", "register now"],
     a_apply),
    ("contact", ["contact", "helpline", "phone", "number", "email", "address", "call",
                 "office location", "toll free", "reach campus", "how to reach", "direction",
                 "where is cu", "gharuan", "airport", "railway station"], a_contact),
    ("capabilities", ["what can you do", "help me", "help", "features", "options",
                      "who are you", "what are you", "your name", "tum kaun", "kya kar sakte"],
     a_capabilities),
    ("joke", ["joke", "funny", "jokes", "hasa", "laugh"], None),
    ("motivate", ["motivat", "inspire", "inspiration", "quote", "sad", "depressed",
                  "tension", "stress"], None),
    ("time", ["time now", "current time", "what time", "aaj date", "today date",
              "what day", "date today", "current date"], None),
    ("creator", ["who made you", "who created", "who built", "your creator", "developer",
                 "banaya kisne"], None),
]

GREETINGS = [
    "Hey there! 👋 I'm **CU Assistant**, your 24×7 campus guide for Chandigarh University. "
    "Ask me about **admissions, courses, fees, scholarships, placements, hostels** or anything "
    "campus-related!",
    "Hello! 😊 Welcome to **CU Assistant**. How can I help you today — admissions, courses, fees, "
    "placements or campus life?",
    "Hi! 👋 Great to see you! I can help with **CUCET, admissions, courses, fees, scholarships, "
    "placements, hostels and CUIMS**. What would you like to know?",
]

FALLBACKS = [
    "I'm not fully sure I caught that 🤔. I'm best at **Chandigarh University** topics — try "
    "asking about admissions, CUCET, courses, fees, scholarships, placements, hostels, campus "
    "facilities or the CUIMS portal.",
    "Hmm, I didn't quite get that. I specialize in everything **Chandigarh University** — "
    "admissions, courses, fees, placements, hostel life and more. Ask me one of those! 🎓",
]

# ---------------------------------------------------------------- course detect
def detect_course(text: str):
    t = norm(text)
    best, best_len = None, 0
    for c in K.COURSES:
        for alias in c["aliases"]:
            a = norm(alias)
            if a in t and len(a) > best_len:
                best, best_len = c, len(a)
    return best

def course_card(c):
    specs = ", ".join(c["specializations"][:8])
    careers = ", ".join(c["careers"])
    chips = ["Fees for this course", "Admissions process", "Placements"]
    return (
        f"🎓 **{c['name']}**\n\n"
        f"- **Duration:** {c['duration']}\n"
        f"- **Eligibility:** {c['eligibility']}\n"
        f"- **Entrance:** {c['entrance']}\n"
        f"- **Indicative fee:** {c['fee']}\n"
        f"- **Specializations / areas:** {specs}\n"
        f"- **Career paths:** {careers}\n\n"
        "Exact fee & current seats: check [cuchd.in admissions]("
        + K.LINKS["admissions"] + ") or ask me for the **fees** or **scholarship** details.",
        chips
    )

# ------------------------------------------------------------------ engine
class ChatbotEngine:
    def __init__(self):
        self.ctx = {"last_intent": None, "last_course": None}

    def answer(self, message: str):
        """Return (markdown_text, chips_list)."""
        raw = message.strip()
        t = norm(raw)
        if not t:
            return "Please ask me something about Chandigarh University! 😊", K.WELCOME_CHIPS

        # --- 0. hostel/mess queries always route to residential info
        if re.search(r"\b(hostel|mess|dorm|rahat|accommodation)\b", t):
            self.ctx["last_intent"] = "hostel"
            return a_hostel()

        # --- 1. course-specific lookup wins when a course is clearly mentioned
        course = detect_course(raw)
        asks_fee = has(t, "fee", "fees", "cost", "kitna", "price", "tuition")
        asks_place = has(t, "placement", "job", "package", "salary", "career", "scope")
        asks_elig = has(t, "eligib", "kya chahiye", "required", "criteria")
        if course:
            self.ctx["last_course"] = course["id"]
            if asks_fee:
                return a_fees(course)
            if asks_place:
                return (
                    f"💼 **Careers after {course['name']}**\n\n"
                    f"- Common roles: {', '.join(course['careers'])}\n"
                    "- CU's recent placement drives saw 9,000+ offers with 900+ recruiters "
                    "(Microsoft, Google, Amazon, Adobe, Deloitte, TCS, Infosys, Wipro, "
                    "Accenture and many more).\n"
                    "- Specializations like AI/ML, Data Science and Cyber Security get strong "
                    "product-company offers.\n\n"
                    "More: [cuchd.in/placements](" + K.LINKS["placements"] + ").",
                    ["Placement overview", "Fees for this course", "Admissions process"]
                )
            return course_card(course)

        # --- 2. follow-ups using context
        if self.ctx["last_course"] and (asks_fee or t in ("fees", "fee", "kitni fee")):
            cid = self.ctx["last_course"]
            c = next((x for x in K.COURSES if x["id"] == cid), None)
            if c:
                return a_fees(c)

        # --- 3. intent scoring
        scored = []
        words = t.split()
        # token set tolerant of plural forms (placement/placements, fee/fees…)
        tset = set(words)
        for w in words:
            if len(w) > 4 and w.endswith("s"):
                tset.add(w[:-1])
            if len(w) > 3:
                tset.add(w + "s")
        for iid, phrases, fn in INTENTS:
            score = 0
            for p in phrases:
                pn = norm(p)
                if " " in pn:
                    if pn in t:
                        score += 3 + len(pn.split())
                else:
                    if pn in tset:
                        score += 2
                    elif len(pn) >= 6 and pn in t:
                        score += 1
            # fuzzy bonus against user words for single-word triggers
            if score == 0:
                for w in tset:
                    for p in phrases:
                        pn = norm(p)
                        if " " not in pn and len(w) > 4 and len(pn) > 4:
                            r = SequenceMatcher(None, w, pn).ratio()
                            if r > 0.86:
                                score += 1.5
            if score:
                scored.append((score, iid, fn))

        scored.sort(key=lambda x: -x[0])
        best = scored[0] if scored and scored[0][0] >= 2 else None

        if best:
            iid, fn = best[1], best[2]
            self.ctx["last_intent"] = iid
            return self._serve(iid, fn, raw, t)

        # --- 4. fallback
        return random.choice(FALLBACKS), ["Admissions process", "Courses & schools",
                                          "Fees structure", "Placements"]

    def _serve(self, iid, fn, raw, t):
        if iid == "greeting":
            return random.choice(GREETINGS), K.WELCOME_CHIPS
        if iid == "goodbye":
            return ("Goodbye! 👋 All the best with your CU journey — I'm here 24×7 whenever "
                    "you need campus info. #CUCampusLife 🎓",
                    ["Contact & helpline", "Admissions process"])
        if iid == "thanks":
            return random.choice([
                "You're welcome! 😊 Anything else about CU — admissions, courses, fees, "
                "hostels or placements?",
                "Happy to help! 🌟 Feel free to ask anything else about Chandigarh University.",
                "Anytime! 🙌 Want to know about scholarships, CUCET or campus life next?",
            ]), ["Scholarships", "Campus facilities", "Admissions process"]
        if iid == "fees":
            return a_fees()
        if iid == "joke":
            return "😄 " + random.choice(K.JOKES), ["One more joke", "Motivate me", "Admissions process"]
        if iid == "motivate":
            return "🌟 " + random.choice(K.MOTIVATION), ["Placements", "Scholarships", "One more quote"]
        if iid == "time":
            now = datetime.datetime.now()
            return (f"🕒 It's **{now.strftime('%I:%M %p')}** on **{now.strftime('%A, %d %B %Y')}** "
                    f"right now.\n\nFun fact: the campus is buzzing most between 9 AM and 5 PM — "
                    f"that's when you'll want to be in class anyway (75% attendance! 😉)."), \
                   ["Attendance rules", "Admissions process"]
        if iid == "creator":
            return ("I'm **CU Assistant** — an AI chatbot demo built with Python (Flask), a "
                    "custom NLP intent engine, and a streaming web chat UI. Think of me as a "
                    "friendly digital guide for Chandigarh University. 🤖🎓",
                    ["What can you do?", "About CU", "Admissions process"])
        if fn is not None:
            return fn()
        return random.choice(FALLBACKS), K.WELCOME_CHIPS

    # ---------------------------------------------------------------- LLM route
    def smart_answer(self, message: str):
        """Try LLM if configured, else local engine. Never fails hard."""
        if os.environ.get("CU_USE_LLM", "0") == "1":
            try:
                out = llm_answer(message)
                if out:
                    return out.strip(), []
            except Exception:
                pass
        return self.answer(message)


def stream_chunks(text: str):
    """Split markdown into small streaming chunks (word groups)."""
    words = text.split(" ")
    buf = []
    for i, w in enumerate(words):
        buf.append(w)
        if len(buf) >= 3 or i == len(words) - 1:
            yield " ".join(buf) + (" " if i < len(words) - 1 else "")
            buf = []
