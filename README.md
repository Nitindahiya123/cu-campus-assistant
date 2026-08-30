# 🎓 CU Assistant — Chandigarh University AI Campus Chatbot

A complete, production-style **AI campus assistant for Chandigarh University** — Python
streaming backend + a premium, fully responsive chat UI. It answers in real time about
admissions, CUCET, courses, fees, scholarships, placements, hostels, campus facilities,
transport, CUIMS, contacts and more — with voice input, read-aloud, dark mode, quick
replies and feedback.

> ⚠️ This is an unofficial student-assistant demo. Figures (fees, stats, dates) are
> indicative — always verify on the official website [cuchd.in](https://www.cuchd.in).

---

## ✨ Features

**Backend (Python / Flask)**
- Real-time **Server-Sent Events (SSE) streaming** — answers appear word-by-word like ChatGPT
- Custom NLP engine: weighted keyword + fuzzy (`difflib`) intent matching, 30+ intents
- **Context-aware follow-ups** (ask “B.Tech CSE details” → then just “fees” → it remembers)
- Rich CU knowledge base: 14+ courses with duration/eligibility/entrance/fees/careers,
  scholarships, placements, hostels, facilities, contacts, CUCET, CUIMS, attendance rules…
- Hinglish-friendly (understands *“fees kya hai”*, *“placements kaisi hai”*, *“kaise le”*)
- Feedback API (thumbs up/down persisted to `feedback.json`)
- **Optional real-LLM mode**: set `GROQ_API_KEY` (free tier) + `CU_USE_LLM=1` to power
  answers with Llama-3.3-70B — automatic fallback to the local engine on any error

**Frontend (vanilla HTML/CSS/JS — no build step)**
- Modern chat UI with CU-branded blue/amber theme, gradients & smooth animations
- 💡 Welcome dashboard with topic cards; sidebar “Explore Campus” quick links
- ⌨️ Quick-reply chips after every answer
- 🎤 **Voice input** (Web Speech API) and 🔊 **text-to-speech** read-aloud
- 🌙 **Dark / light theme** (persisted), 📋 copy, 👍👎 feedback per message
- 📰 Live admission notice ticker
- Fully responsive (mobile drawer sidebar), session persistence, markdown rendering

---

## 🚀 Run it

```bash
cd cu-campus-assistant
pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000** (in the Arena preview, the server appears as a live preview).

### Optional — power it with a real LLM (Groq, free)

```bash
export GROQ_API_KEY="gsk_your_key_here"   # get one free at console.groq.com
export CU_USE_LLM=1
python app.py
```

Or use OpenAI: `OPENAI_API_KEY=...` (optionally `OPENAI_MODEL=gpt-4o-mini`).
Without a key, the built-in knowledge engine handles everything offline.

---

## 📡 API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Chat web app |
| `GET` | `/api/health` | Health check |
| `POST` | `/api/chat` | Stream an answer — body `{"message": "...", "session_id": "..."}`; responds with SSE events `meta → token* → quick → done` |
| `POST` | `/api/feedback` | Store `{"rating":"up|down","user_message":"...","bot_reply":"..."}` |

Quick test:

```bash
curl -N -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Tell me about B.Tech CSE fees"}'
```

---

## 🗂️ Project structure

```
cu-campus-assistant/
├── app.py                  # Flask app — SSE streaming, feedback, sessions
├── requirements.txt
├── chatbot/
│   ├── knowledge.py        # CU data: courses, fees, placements, contacts…
│   └── engine.py           # NLP intents, fuzzy matching, context, LLM hook
├── templates/
│   └── index.html          # Chat UI markup
└── static/
    ├── css/style.css       # Design system (themes, animations, responsive)
    └── js/app.js           # Streaming client, voice, TTS, markdown, state
```

## ➕ Extending it

- **Add a topic:** add an answer function + an intent row in `chatbot/engine.py`.
- **Add a course:** append to `COURSES` in `chatbot/knowledge.py` (aliases drive matching).
- **Tune design:** edit the CSS variables at the top of `static/css/style.css`.
