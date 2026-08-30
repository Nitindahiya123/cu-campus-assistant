# -*- coding: utf-8 -*-
"""
Chandigarh University knowledge base.
All figures are INDICATIVE and may change — students must verify on
the official website https://www.cuchd.in before taking decisions.
"""

DISCLAIMER = (
    "\n\n> ⚠️ *This is an unofficial student-assistant demo. Fee figures, dates and "
    "stats are indicative and can change — always confirm on the official website "
    "[cuchd.in](https://www.cuchd.in) or call the admission helpline.*"
)

# ---------------------------------------------------------------- quick links
LINKS = {
    "website": "https://www.cuchd.in",
    "admissions": "https://www.cuchd.in/admissions",
    "cucet": "https://www.cuchd.in/cucet",
    "cuims": "https://uims.cuchd.in",
    "fees": "https://www.cuchd.in/admissions/fee-structure",
    "placements": "https://www.cuchd.in/placements",
    "scholarships": "https://www.cuchd.in/scholarships",
    "hostel": "https://www.cuchd.in/campus-life/hostel",
    "international": "https://www.cuchd.in/international",
    "contact": "https://www.cuchd.in/contact-us",
}

# ------------------------------------------------------------------ courses
# fee = indicative annual tuition fee range in INR
COURSES = [
    {
        "id": "btech_cse",
        "name": "B.Tech — Computer Science & Engineering (CSE)",
        "aliases": ["btech cse", "b.tech cse", "b tech cse", "b.tech computer",
                    "btech computer", "computer science engineering", "b tech computer",
                    "b.e. cse", "be cse", "cse btech", "engineering computer",
                    "btech in computer", "b.tech in computer"],
        "duration": "4 years (8 semesters)",
        "eligibility": "10+2 with Physics, Chemistry & Mathematics (PCM), min. 50% aggregate",
        "entrance": "JEE Main / CUCET",
        "fee": "≈ ₹2.4 – 3.0 L per year (varies by specialization)",
        "specializations": ["AI & Machine Learning", "Data Science & Big Data",
                            "Cyber Security", "Cloud Computing", "Full-Stack Development",
                            "Internet of Things (IoT)", "Blockchain", "DevOps & Cloud Computing"],
        "careers": ["Software Engineer", "Data Scientist", "Cloud / DevOps Engineer",
                    "Security Analyst", "Full-Stack Developer"],
    },
    {
        "id": "btech_other",
        "name": "B.Tech — ECE / Mechanical / Civil / Electrical & more",
        "aliases": ["btech ece", "b.tech ece", "electronics communication",
                    "btech mechanical", "mechanical engineering", "btech civil",
                    "civil engineering", "btech electrical", "electrical engineering",
                    "btech aerospace", "aerospace engineering", "btech automobile",
                    "btech mechatronics", "b.tech mechanical", "b tech ece",
                    "engineering branches", "btech branches", "which engineering",
                    "btech it", "information technology engineering"],
        "duration": "4 years (8 semesters)",
        "eligibility": "10+2 with PCM, min. 50% aggregate",
        "entrance": "JEE Main / CUCET",
        "fee": "≈ ₹2.2 – 2.7 L per year",
        "specializations": ["Electronics & Communication", "Mechanical", "Civil",
                            "Electrical", "Aerospace", "Automobile", "Mechatronics",
                            "Chemical", "Information Technology"],
        "careers": ["Core engineer", "Design / R&D engineer", "Project engineer",
                    "PSUs / Govt jobs (GATE)", "Higher studies (M.Tech / MS)"],
    },
    {
        "id": "bca",
        "name": "BCA — Bachelor of Computer Applications",
        "aliases": ["bca", "bachelor of computer application", "computer applications degree"],
        "duration": "3 years (6 semesters)",
        "eligibility": "10+2 (any stream) with min. 50% aggregate",
        "entrance": "CUCET / merit",
        "fee": "≈ ₹1.2 – 1.5 L per year",
        "specializations": ["Cloud Computing & Security", "Data Science",
                            "Full-Stack Development", "Mobile App Development"],
        "careers": ["Software / Web Developer", "App Developer", "Cloud Support Engineer",
                    "System Administrator — or MCA / MBA later"],
    },
    {
        "id": "mca",
        "name": "MCA — Master of Computer Applications",
        "aliases": ["mca", "master of computer application"],
        "duration": "2 years (4 semesters)",
        "eligibility": "Bachelor's degree with Mathematics at 10+2 or graduation level",
        "entrance": "CUCET / merit",
        "fee": "≈ ₹1.2 – 1.6 L per year",
        "specializations": ["AI & ML", "Cloud Computing", "Cyber Security", "Data Analytics"],
        "careers": ["Software Engineer", "Data Analyst", "Cloud Architect", "IT Manager"],
    },
    {
        "id": "mba",
        "name": "MBA — Master of Business Administration (University School of Business)",
        "aliases": ["mba", "m.b.a", "master of business", "business administration masters",
                    "pgdm", "management degree"],
        "duration": "2 years (4 trimesters/semesters)",
        "eligibility": "Bachelor's degree in any stream with min. 50% aggregate",
        "entrance": "CAT / MAT / CMAT / CUCET",
        "fee": "≈ ₹2.5 – 3.0 L per year",
        "specializations": ["Finance", "Marketing", "HR", "Business Analytics",
                            "Digital Marketing", "International Business",
                            "Supply Chain & Logistics", "Entrepreneurship"],
        "careers": ["Consultant", "Business Analyst", "Marketing / Finance Manager",
                    "Product Manager", "Entrepreneur"],
    },
    {
        "id": "bba",
        "name": "BBA — Bachelor of Business Administration",
        "aliases": ["bba", "b.b.a", "bachelor of business", "business administration bach"],
        "duration": "3 years (6 semesters)",
        "eligibility": "10+2 (any stream) with min. 50% aggregate",
        "entrance": "CUCET / merit",
        "fee": "≈ ₹1.3 – 1.6 L per year",
        "specializations": ["Digital Marketing", "Business Analytics", "Finance",
                            "Family Business", "Tourism & Event Management"],
        "careers": ["Management trainee", "Sales / Marketing executive",
                    "Operations analyst — or MBA later"],
    },
    {
        "id": "bcom",
        "name": "B.Com (Hons.) — Bachelor of Commerce",
        "aliases": ["bcom", "b.com", "b com", "commerce honours", "commerce degree",
                    "bachelor of commerce"],
        "duration": "3 years (6 semesters)",
        "eligibility": "10+2 (Commerce preferred) with min. 50% aggregate",
        "entrance": "CUCET / merit",
        "fee": "≈ ₹1.1 – 1.4 L per year",
        "specializations": ["Accounting & Finance", "Banking & Insurance",
                            "Taxation", "Financial Markets"],
        "careers": ["Accountant", "Banking / Insurance roles", "CA / CS / CMA track",
                    "Finance analyst"],
    },
    {
        "id": "law",
        "name": "Law — BA LLB (Hons.) / BBA LLB (Hons.) / LLB",
        "aliases": ["ba llb", "bba llb", "llb", "law course", "law degree",
                    "legal studies", "5 year law", "3 year law", "ba-llb", "bba-llb"],
        "duration": "5 years integrated (BA/BBA LLB) • 3 years (LLB)",
        "eligibility": "10+2 any stream (50%) for integrated LLB; graduation for LLB",
        "entrance": "CUCET / CLAT / merit",
        "fee": "≈ ₹1.3 – 1.7 L per year",
        "specializations": ["Criminal Law", "Corporate / Commercial Law",
                            "Constitutional Law", "Cyber Law"],
        "careers": ["Advocate", "Corporate counsel", "Judicial services",
                    "Legal advisor", "Law firms"],
    },
    {
        "id": "bpharm",
        "name": "B.Pharm / D.Pharm — Pharmacy",
        "aliases": ["bpharm", "b.pharm", "pharmacy", "dpharm", "d.pharm", "pharma degree",
                    "bachelor of pharmacy"],
        "duration": "B.Pharm 4 years • D.Pharm 2 years",
        "eligibility": "10+2 with PCB/PCM, min. 50% aggregate",
        "entrance": "CUCET / state counselling",
        "fee": "≈ ₹1.7 – 2.0 L per year",
        "specializations": ["Pharmaceutics", "Pharmacology", "Pharmacognosy",
                            "Industrial Pharmacy"],
        "careers": ["Pharmacist", "Drug inspector", "Pharmaceutical industry (QA/QC/R&D)",
                    "Clinical research", "Own medical store"],
    },
    {
        "id": "agri",
        "name": "B.Sc (Hons.) Agriculture",
        "aliases": ["bsc agriculture", "b.sc agriculture", "agriculture course",
                    "agri degree", "b.sc agri", "farming course", "bsc agri"],
        "duration": "4 years (8 semesters)",
        "eligibility": "10+2 with Physics, Chemistry & Biology/Maths/Agriculture, min. 50%",
        "entrance": "CUCET / state agriculture counselling",
        "fee": "≈ ₹1.6 – 2.0 L per year",
        "specializations": ["Agronomy", "Horticulture", "Soil Science",
                            "Plant Protection", "Agri-business"],
        "careers": ["Agriculture officer", "Agri-input industry", "Banking (AFO)",
                    "Research / M.Sc", "Agri-entrepreneur"],
    },
    {
        "id": "bdes",
        "name": "B.Des — Bachelor of Design",
        "aliases": ["b.des", "bdes", "design course", "fashion design", "graphic design",
                    "ux design degree", "interior design", "product design degree"],
        "duration": "4 years (8 semesters)",
        "eligibility": "10+2 (any stream) with min. 50% + design aptitude",
        "entrance": "CUCET / portfolio & aptitude",
        "fee": "≈ ₹1.5 – 1.8 L per year",
        "specializations": ["UX/UI Design", "Fashion Design", "Interior Design",
                            "Product & Industrial Design", "Graphics & Animation"],
        "careers": ["UX/UI designer", "Fashion / Interior designer", "Product designer",
                    "Creative studios"],
    },
    {
        "id": "hotel",
        "name": "BHMCT — Hotel & Hospitality Management",
        "aliases": ["hotel management", "bhm", "bhmct", "hospitality course",
                    "bachelor of hotel", "hm course"],
        "duration": "4 years (8 semesters)",
        "eligibility": "10+2 (any stream) with min. 50% aggregate",
        "entrance": "CUCET / merit",
        "fee": "≈ ₹1.2 – 1.5 L per year",
        "specializations": ["Food Production", "F&B Service", "Front Office",
                            "Housekeeping", "Tourism"],
        "careers": ["Hotel chains (Taj, Marriott, Oberoi…)", "Cruise lines",
                    "Aviation hospitality", "Restaurant entrepreneur"],
    },
    {
        "id": "media",
        "name": "BJMC / BA (Journalism & Mass Communication)",
        "aliases": ["bjmc", "journalism", "mass communication", "media course",
                    "mass comm", "b.a journalism"],
        "duration": "3 years (6 semesters)",
        "eligibility": "10+2 (any stream) with min. 50% aggregate",
        "entrance": "CUCET / merit",
        "fee": "≈ ₹1.1 – 1.4 L per year",
        "specializations": ["Digital Media", "TV & Radio", "Public Relations",
                            "Advertising", "Film-making"],
        "careers": ["Journalist / Anchor", "Content writer", "PR & advertising",
                    "Digital media producer", "YouTuber / influencer"],
    },
    {
        "id": "nursing",
        "name": "B.Sc Nursing",
        "aliases": ["bsc nursing", "b.sc nursing", "nursing course", "bsc nurse",
                    "nursing degree"],
        "duration": "4 years (8 semesters)",
        "eligibility": "10+2 with PCB, min. 50% (age 17+ as per INC norms)",
        "entrance": "CUCET / state nursing counselling",
        "fee": "≈ ₹1.4 – 1.7 L per year",
        "specializations": ["Medical-Surgical", "Community Health", "Pediatrics",
                            "Psychiatric nursing"],
        "careers": ["Staff nurse (hospitals India & abroad)", "Community health officer",
                    "Higher studies / teaching"],
    },
]

SCHOOLS = [
    "University Institute of Engineering (UIE) — B.Tech / M.Tech",
    "University School of Business (USB) — BBA / MBA / Commerce",
    "University Institute of Computing",
    "University Institute of Legal Studies (UILS)",
    "Institute of Pharma Sciences",
    "University Institute of Agricultural Sciences",
    "Institute of Media Studies & Film Production",
    "University Institute of Hotel & Tourism Management",
    "University Institute of Design",
    "Institute of Health Sciences & Nursing",
    "University Institute of Sciences (Physics, Chemistry, Maths, Bio)",
    "Institute of Liberal Arts & Humanities",
    "School of Animation, VFX & Gaming",
]

# ---------------------------------------------------------------- placements
PLACEMENT_STATS = [
    "9,000+ placement offers for recent batches, with 900+ recruiting companies visiting campus",
    "National highest packages have crossed **₹50 LPA**; international offers have gone up to crore-plus rupee packages",
    "650+ multi-national recruiters including Fortune-500 companies hire regularly",
]
TOP_RECRUITERS = [
    "Microsoft", "Google", "Amazon", "Adobe", "Cisco", "SAP Labs", "IBM",
    "Deloitte", "EY", "KPMG", "PwC", "TCS", "Infosys", "Wipro", "Accenture",
    "Cognizant", "Capgemini", "HCL", "Tech Mahindra", "Samsung", "HP", "Dell",
    "Flipkart", "Zomato", "Just Dial", "Asian Paints", "ICICI Bank", "HDFC Bank",
]

# --------------------------------------------------------------- scholarships
SCHOLARSHIPS = [
    ("CUCET merit scholarship",
     "Performance in **CUCET** is the biggest scholarship route — top scorers can get "
     "up to **100% tuition-fee waiver**, with slabs decreasing by score band. "
     "Appearing in the early CUCET phases generally gives the best scholarship benefit."),
    ("National entrance-exam merit",
     "Scholarships based on **JEE Main / CAT / MAT / CMAT / CLAT / NATA** percentiles."),
    ("Board merit",
     "Toppers / high scorers of Class 12 boards get fee concessions."),
    ("Sports quota",
     "Scholarships for state / national / international level sportspersons."),
    ("Defence & paramilitary wards",
     "Concession for wards of defence/paramilitary personnel and war widows."),
    ("Special categories",
     "Concessions for single girl child, orphans, and certain social categories "
     "(as per university policy)."),
]

# ----------------------------------------------------------------- facilities
FACILITIES = [
    ("📚 Libraries", "Central & departmental libraries with 100,000+ books, e-journals, "
     "digital library and reading halls open late, especially during exams."),
    ("💻 Smart campus", "Wi-Fi enabled campus, smart classrooms, modern computer & "
     "research labs (Apple, IBM, AWS, Microsoft-partnered labs)."),
    ("🏟️ Sports", "Sports complex with gymnasiums, basketball/tennis/badminton courts, "
     "cricket & football grounds, athletics track and indoor arenas."),
    ("🏥 Medical centre", "On-campus medical centre with doctors & ambulance, plus "
     "tie-ups with hospitals in Mohali/Chandigarh."),
    ("🍽️ Food courts", "Multiple cafeterias, food courts and mess facilities serving "
     "vegetarian multi-cuisine meals."),
    ("🚌 Transport", "Fleet of buses covering Chandigarh, Mohali, Kharar, Panchkula, "
     "Ludhiana, Ambala and nearby towns."),
    ("🏦 Banking & ATMs", "Bank branch and ATMs inside campus; postal and courier "
     "facilities available."),
    ("🛍️ Daily needs", "Stationery shops, general store, saloon, laundry and printing "
     "facilities inside the campus."),
]

# ------------------------------------------------------------------- hostels
HOSTEL_INFO = {
    "overview": "Separate, secure in-campus hostels for boys and girls with warden supervision, "
                "24×7 security and CCTV coverage.",
    "rooms": "Options of 1-seater, 2-seater, 3-seater and 4-seater rooms — both AC and non-AC. "
             "Rooms come with bed, table, chair, almirah and Wi-Fi.",
    "mess": "Hygienic multi-cuisine vegetarian mess (and on-campus food courts) with "
            "rotating menu; separate mess for boys' and girls' hostels.",
    "fee": "Hostel + mess fees are roughly **₹95,000 – ₹1,50,000 per year** depending on room "
           "occupancy and AC choice (indicative).",
    "amenities": "Gym, common rooms with TV, indoor games, laundry, hot water, reading rooms, "
                 "24×7 power backup and medical assistance.",
    "booking": "Hostel seats are limited and allotted at the time of admission on first-come, "
               "first-served basis — mention hostel requirement during counselling/admission.",
}

# -------------------------------------------------------------------- contact
CONTACT = {
    "address": "Chandigarh University, NH-95, Chandigarh–Ludhiana Highway, "
               "Gharuan, Mohali, Punjab – 140413",
    "phone": "+91-160-3044444 (admission helpline)",
    "email_admissions": "admissions@cuchd.in",
    "email_info": "info@cuchd.in",
    "website": "www.cuchd.in",
    "reach": [
        "✈️ Chandigarh International Airport (IXC) — approx. 35 km",
        "🚆 Chandigarh Railway Station — approx. 30 km",
        "🚌 Kharar bus stand — approx. 8 km; university buses ply from Chandigarh, "
        "Mohali, Panchkula & nearby towns",
    ],
}

JOKES = [
    "Why do CU students make great friends? Because they've survived 8:30 AM lectures "
    "with 75% attendance pressure — nothing scares them. 😄",
    "A student asked the librarian: 'Can I borrow a book on paranoia?' The librarian whispered: "
    "'They're right behind you!' 📚",
    "My CSE code never works on the first try… that's why they call it 'try-and-try-again' — "
    "or, as we call it, a loop. 🔁",
    "Placement season is like CUCET — the earlier you prepare, the better the result. "
    "See what I did there? 😏",
]

MOTIVATION = [
    "“Success is the sum of small efforts, repeated day in and day out.” — Robert Collier. "
    "Your 75% attendance today is your placement offer tomorrow. 💪",
    "“The expert in anything was once a beginner.” — Helen Hayes. Keep shipping, keep learning. 🚀",
    "“Don't watch the clock; do what it does. Keep going.” — Sam Levenson. One more DSA problem. One more revision. ⏱️",
]

# quick-reply chip presets
WELCOME_CHIPS = ["Admissions process", "Courses & schools", "Fees & scholarships", "Placements"]
