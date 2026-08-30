# -*- coding: utf-8 -*-
"""
CU Assistant — Chandigarh University AI Campus Chatbot
Flask backend with real-time Server-Sent Events (SSE) streaming.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://localhost:5000

Optional AI upgrade: set GROQ_API_KEY (free tier at groq.com) and
CU_USE_LLM=1 to route answers through a large language model.
"""
import os
import json
import time
import uuid
import threading
from datetime import datetime

from flask import Flask, request, Response, jsonify, render_template

from chatbot.engine import ChatbotEngine, stream_chunks

app = Flask(__name__)

ENGINES = {}
LOCK = threading.Lock()
FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "feedback.json")


def get_engine(session_id: str) -> ChatbotEngine:
    with LOCK:
        if session_id not in ENGINES:
            ENGINES[session_id] = ChatbotEngine()
        return ENGINES[session_id]


def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "cu-assistant", "time": datetime.now().isoformat()})


@app.route("/api/chat", methods=["POST"])
def chat():
    """Real-time streaming chat endpoint (SSE over POST)."""
    data = request.get_json(force=True, silent=True) or {}
    message = (data.get("message") or "").strip()[:1500]
    session_id = data.get("session_id") or str(uuid.uuid4())
    engine = get_engine(session_id)

    def generate():
        yield sse("meta", {"session_id": session_id})
        try:
            answer, chips = engine.smart_answer(message)
        except Exception as e:  # pragma: no cover
            app.logger.exception("engine error")
            answer, chips = ("Sorry, I hit a small glitch processing that 🙏 "
                             "Please try again.", ["Admissions process"])
        for chunk in stream_chunks(answer):
            yield sse("token", {"value": chunk})
            time.sleep(0.018)  # real-time typing pace
        yield sse("quick", {"chips": chips})
        yield sse("done", {"ok": True})

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@app.route("/api/feedback", methods=["POST"])
def feedback():
    """Store thumbs up/down feedback for continuous improvement."""
    data = request.get_json(force=True, silent=True) or {}
    entry = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "rating": data.get("rating"),
        "user_message": (data.get("user_message") or "")[:500],
        "bot_reply": (data.get("bot_reply") or "")[:1000],
    }
    try:
        history = []
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        history.append(entry)
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return jsonify({"ok": True, "thanks": "Thanks for your feedback! 💙"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
