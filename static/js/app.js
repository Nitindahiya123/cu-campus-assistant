/* ============================================================
   CU Assistant — frontend logic
   ============================================================ */
const $ = (s) => document.querySelector(s);
const chat = $("#chat");
const input = $("#input");
const sendBtn = $("#sendBtn");
const chipsRow = $("#chipsRow");
const toast = $("#toast");

let sessionId = localStorage.getItem("cu_session") || crypto.randomUUID();
localStorage.setItem("cu_session", sessionId);
let streaming = false;
let queue = [];
let ttsEnabled = localStorage.getItem("cu_tts") === "1";
let currentBotEl = null;
let lastBotText = "";

/* ---------------- data ---------------- */
const EXPLORE = [
  { icon: "🎓", title: "Admissions & CUCET", text: "Process, exam pattern, documents", q: "How do I take admission at CU? Tell me about CUCET." },
  { icon: "📚", title: "Courses & Schools", text: "B.Tech, MBA, Law, Pharma…", q: "What courses and schools does CU offer?" },
  { icon: "💰", title: "Fees", text: "Tuition fee for all programs", q: "What is the fee structure?" },
  { icon: "🎖️", title: "Scholarships", text: "CUCET merit & more", q: "Tell me about scholarships" },
  { icon: "💼", title: "Placements", text: "Packages & recruiters", q: "How are the placements at CU?" },
  { icon: "🏨", title: "Hostel Life", text: "Rooms, mess, fees", q: "Tell me about hostel facilities" },
  { icon: "🏫", title: "Campus & Transport", text: "Facilities, buses, clubs", q: "What campus facilities are there?" },
  { icon: "🖥️", title: "CUIMS Portal", text: "Attendance, results, login", q: "What is CUIMS student portal?" },
  { icon: "📞", title: "Contact & Reach", text: "Helpline, address, directions", q: "How do I contact or reach the campus?" },
];
const SUGGEST = [
  { icon: "🎓", title: "Admissions 2026", text: "CUCET process & documents", q: "How do I take admission at Chandigarh University?" },
  { icon: "💻", title: "B.Tech CSE", text: "Eligibility, fees, scope", q: "Tell me about B.Tech CSE" },
  { icon: "💰", title: "Fees & Scholarships", text: "Up to 100% waiver via CUCET", q: "Fee structure and scholarships" },
  { icon: "💼", title: "Placements", text: "9000+ offers, top recruiters", q: "Placement details at CU" },
  { icon: "🏨", title: "Hostel & Mess", text: "AC rooms, fees, amenities", q: "Hostel details please" },
  { icon: "📞", title: "Contact CU", text: "Helpline & how to reach", q: "Contact details and address" },
];
const TICKER = [
  "📢 CUCET applications open for 2026–27 batch — apply at cuchd.in/cucet",
  "💼 9,000+ placement offers with 900+ recruiters in recent drives",
  "🎖️ CUCET top scorers can win up to 100% tuition scholarship",
  "🏨 Hostel seats fill fast — request one during counselling",
  "📞 Admission helpline: +91-160-3044444",
  "🌍 Students from 40+ countries study at CU",
];

/* ---------------- render static content ---------------- */
function initStatic() {
  $("#tickerTrack").innerHTML =
    [...TICKER, ...TICKER].map(t => `<span>${t}</span>`).join("");

  $("#exploreGrid").innerHTML = EXPLORE.map(e => `
    <button class="explore-card" data-q="${e.q.replace(/"/g, "&quot;")}">
      <span class="ec-icon">${e.icon}</span>
      <span class="ec-text"><strong>${e.title}</strong><span>${e.text}</span></span>
    </button>`).join("");

  $("#suggestGrid").innerHTML = SUGGEST.map(s => `
    <button class="suggest-card" data-q="${s.q.replace(/"/g, "&quot;")}">
      <span class="sc-icon">${s.icon}</span>
      <strong>${s.title}</strong><span>${s.text}</span>
    </button>`).join("");

  document.querySelectorAll("[data-q]").forEach(b =>
    (b.onclick = () => sendUser(b.dataset.q)));

  $("#ttsToggle").classList.toggle("active", ttsEnabled);
}

/* ---------------- theme ---------------- */
function initTheme() {
  const saved = localStorage.getItem("cu_theme");
  if (saved) document.documentElement.dataset.theme = saved;
  $("#themeToggle").addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    localStorage.setItem("cu_theme", next);
  });
}

/* ---------------- markdown (lightweight, safe) ---------------- */
function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
function md(mdText) {
  let src = escapeHtml(mdText);
  // links
  src = src.replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g,
    (m, t, u) => `<a href="${u}" target="_blank" rel="noopener">${t}</a>`);
  src = src.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  src = src.replace(/\*([^*\n]+)\*/g, "<em>$1</em>");

  const lines = src.split("\n");
  let html = "", list = null;
  const closeList = () => { if (list) { html += `</${list}>`; list = null; } };
  for (let line of lines) {
    const l = line.trim();
    if (l.startsWith("&gt; ")) {
      closeList();
      html += `<blockquote>${l.slice(5)}</blockquote>`;
    } else if (/^[-•]\s+/.test(l)) {
      if (list !== "ul") { closeList(); html += "<ul>"; list = "ul"; }
      html += `<li>${l.replace(/^[-•]\s+/, "")}</li>`;
    } else if (/^\d+\.\s+/.test(l)) {
      if (list !== "ol") { closeList(); html += "<ol>"; list = "ol"; }
      html += `<li>${l.replace(/^\d+\.\s+/, "")}</li>`;
    } else if (l === "") {
      closeList();
    } else {
      closeList();
      html += `<p>${l}</p>`;
    }
  }
  closeList();
  return html;
}
function stripMd(t) {
  return t.replace(/\[([^\]]+)\]\([^)]+\)/g, "$1").replace(/[*>#`]/g, "").replace(/\n{2,}/g, "\n");
}

/* ---------------- messages ---------------- */
function ensureThread() {
  let thread = $(".chat-inner");
  if (!thread) {
    $("#welcome")?.remove();
    thread = document.createElement("div");
    thread.className = "chat-inner";
    chat.appendChild(thread);
  }
  return thread;
}
const BOT_SVG = `<svg viewBox="0 0 100 100"><path d="M50 14 10 32l40 18 31-13.9V62h7V32z" fill="currentColor"/><path d="M28 54v13c0 8 10 15 22 15s22-7 22-15V54l-22 10z" fill="#ffb020"/></svg>`;

function addUserMsg(text) {
  const thread = ensureThread();
  const el = document.createElement("div");
  el.className = "msg user";
  el.innerHTML = `
    <div class="msg-avatar">🧑‍🎓</div>
    <div class="msg-body">
      <div class="bubble"></div>
      <div class="msg-time">${timeNow()}</div>
    </div>`;
  el.querySelector(".bubble").textContent = text;
  thread.appendChild(el);
  scrollDown();
}

function addBotMsg() {
  const thread = ensureThread();
  const el = document.createElement("div");
  el.className = "msg bot";
  el.innerHTML = `
    <div class="msg-avatar">${BOT_SVG}</div>
    <div class="msg-body">
      <div class="bubble"><div class="typing"><span></span><span></span><span></span></div></div>
      <div class="msg-actions" style="display:none">
        <button class="msg-action" data-act="up" title="Good answer">👍</button>
        <button class="msg-action" data-act="down" title="Bad answer">👎</button>
        <button class="msg-action" data-act="copy" title="Copy">⧉</button>
        <button class="msg-action" data-act="speak" title="Read aloud">🔊</button>
      </div>
    </div>`;
  thread.appendChild(el);
  currentBotEl = el;
  scrollDown();
  return el;
}

function finalizeBot(el, fullText, userText) {
  const actions = el.querySelector(".msg-actions");
  actions.style.display = "flex";
  actions.querySelectorAll(".msg-action").forEach(btn => {
    btn.addEventListener("click", () => handleAction(btn, btn.dataset.act, fullText, userText));
  });
  lastBotText = fullText;
  if (ttsEnabled) speak(stripMd(fullText));
  saveHistory();
}

function handleAction(btn, act, text, userText) {
  if (act === "copy") {
    navigator.clipboard.writeText(stripMd(text));
    showToast("Copied to clipboard 📋");
  } else if (act === "speak") {
    speak(stripMd(text));
    showToast("Reading aloud 🔊");
  } else if (act === "up" || act === "down") {
    btn.classList.add("picked");
    fetch("/api/feedback", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rating: act, user_message: userText, bot_reply: text })
    });
    showToast(act === "up" ? "Glad it helped! 💙" : "Thanks — we'll improve 🙏");
  }
}

/* ---------------- streaming chat ---------------- */
async function sendUser(text) {
  text = (text || "").trim();
  if (!text) return;
  if (streaming) { queue.push(text); return; }
  addUserMsg(text);
  input.value = "";
  autoGrow();
  chipsRow.innerHTML = "";

  streaming = true;
  sendBtn.disabled = true;
  const botEl = addBotMsg();
  const bubble = botEl.querySelector(".bubble");
  let answer = "";

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, session_id: sessionId }),
    });
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "", metaSet = false;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const blocks = buffer.split("\n\n");
      buffer = blocks.pop();
      for (const block of blocks) {
        const dataLine = block.split("\n").find(l => l.startsWith("data:"));
        if (!dataLine) continue;
        const evt = JSON.parse(dataLine.slice(5).trim());
        const type = block.includes("event: meta") ? "meta"
                   : block.includes("event: quick") ? "quick"
                   : block.includes("event: done") ? "done" : "token";
        if (type === "meta") {
          sessionId = evt.session_id;
          localStorage.setItem("cu_session", sessionId);
          metaSet = true;
        } else if (type === "token") {
          answer += evt.value;
          bubble.innerHTML = md(answer);
          scrollDown();
        } else if (type === "quick") {
          renderChips(evt.chips || []);
        }
      }
    }
  } catch (e) {
    answer = "⚠️ Connection hiccup — please check the server and try again.";
    bubble.innerHTML = md(answer);
  }
  finalizeBot(botEl, answer, text);
  streaming = false;
  sendBtn.disabled = false;
  if (queue.length) sendUser(queue.shift());
}

function renderChips(chips) {
  chipsRow.innerHTML = "";
  chips.forEach(c => {
    const b = document.createElement("button");
    b.className = "chip";
    b.textContent = c;
    b.addEventListener("click", () => sendUser(c));
    chipsRow.appendChild(b);
  });
}

/* ---------------- voice input (Web Speech API) ---------------- */
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
let recog = null;
if (SR) {
  recog = new SR();
  recog.lang = "en-US";
  recog.interimResults = false;
  recog.onresult = (e) => {
    const said = e.results[0][0].transcript;
    input.value = said;
    sendUser(said);
  };
  recog.onend = () => $("#micBtn").classList.remove("listening");
  recog.onerror = () => $("#micBtn").classList.remove("listening");
}
$("#micBtn").addEventListener("click", () => {
  if (!recog) { showToast("Voice input isn't supported in this browser 🎤❌"); return; }
  if ($("#micBtn").classList.contains("listening")) { recog.stop(); return; }
  try {
    recog.start();
    $("#micBtn").classList.add("listening");
    showToast("Listening… speak now 🎤");
  } catch { /* already started */ }
});

/* ---------------- text to speech ---------------- */
function speak(text) {
  if (!("speechSynthesis" in window)) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text.slice(0, 1200));
  u.rate = 1.02; u.pitch = 1;
  speechSynthesis.speak(u);
}
$("#ttsToggle").addEventListener("click", () => {
  ttsEnabled = !ttsEnabled;
  localStorage.setItem("cu_tts", ttsEnabled ? "1" : "0");
  $("#ttsToggle").classList.toggle("active", ttsEnabled);
  if (!ttsEnabled) speechSynthesis.cancel();
  showToast(ttsEnabled ? "Read-aloud ON 🔊" : "Read-aloud OFF");
});

/* ---------------- composer ---------------- */
function autoGrow() {
  input.style.height = "auto";
  input.style.height = Math.min(input.scrollHeight, 130) + "px";
}
input.addEventListener("input", autoGrow);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendUser(input.value);
  }
});
sendBtn.addEventListener("click", () => sendUser(input.value));

/* ---------------- new chat / sidebar / misc ---------------- */
$("#newChat").addEventListener("click", () => {
  speechSynthesis?.cancel();
  sessionId = crypto.randomUUID();
  localStorage.setItem("cu_session", sessionId);
  chat.innerHTML = `
    <div class="welcome" id="welcome">
      <div class="welcome-logo">${BOT_SVG}</div>
      <h2>Fresh chat — ask me anything! 🎓</h2>
      <p>Admissions, CUCET, courses, fees, scholarships, placements, hostels, CUIMS… I'm ready.</p>
      <div class="suggest-grid" id="suggestGrid"></div>
    </div>`;
  chipsRow.innerHTML = "";
  initStatic();
  closeSidebar();
});
$("#hamburger").addEventListener("click", () => {
  $("#sidebar").classList.toggle("open");
  $("#sidebarOverlay").classList.toggle("show");
});
function closeSidebar() {
  $("#sidebar").classList.remove("open");
  $("#sidebarOverlay").classList.remove("show");
}
$("#sidebarOverlay").addEventListener("click", closeSidebar);

function timeNow() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}
let toastTimer;
function showToast(msg) {
  toast.textContent = msg;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2400);
}
function scrollDown() {
  chat.scrollTop = chat.scrollHeight;
}

/* ---------------- history persistence (best effort) ---------------- */
function saveHistory() {
  try {
    const msgs = [...document.querySelectorAll(".msg")].slice(-30).map(m => ({
      role: m.classList.contains("user") ? "user" : "bot",
      text: m.classList.contains("user")
        ? m.querySelector(".bubble").textContent
        : lastBotTextIf(m),
    }));
    localStorage.setItem("cu_history", JSON.stringify(msgs));
  } catch { /* ignore */ }
}
function lastBotTextIf(m) {
  const b = m.querySelector(".bubble");
  return b ? b.textContent : "";
}

/* ---------------- boot ---------------- */
initStatic();
initTheme();
input.focus();
