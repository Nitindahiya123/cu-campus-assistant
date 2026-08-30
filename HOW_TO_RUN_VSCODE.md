# 🚀 How to Run CU Assistant in VS Code — Step by Step

Follow these steps in order. Even if you've never used Python before, this will work.

---

## Step 1 — Install Python (one time only)

1. Go to **https://www.python.org/downloads/**
2. Click the big yellow button to download Python for Windows (or Mac).
3. Run the installer.
4. ⚠️ **VERY IMPORTANT:** On the first installer screen, tick the box
   **“Add Python to PATH”** at the bottom, then click **Install Now**.
5. Verify it worked: open Command Prompt (Windows: press `Win + R`, type `cmd`, Enter)
   and run:
   ```
   python --version
   ```
   You should see something like `Python 3.12.x`. (Mac/Linux users use `python3`.)

## Step 2 — Install Visual Studio Code (one time only)

1. Download from **https://code.visualstudio.com/** and install with default options.
2. Open VS Code.
3. Click the **Extensions** icon on the left sidebar (or press `Ctrl + Shift + X`).
4. Search for **“Python”** (by Microsoft) and click **Install**.

## Step 3 — Get the project folder

Make sure you have the whole **`cu-campus-assistant`** folder on your computer.
Its contents should look like this:

```
cu-campus-assistant/
├── app.py                  ← the main file we run
├── requirements.txt
├── chatbot/
│   ├── __init__.py
│   ├── knowledge.py
│   └── engine.py
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## Step 4 — Open the project in VS Code

1. In VS Code: **File → Open Folder…**
2. Select the **`cu-campus-assistant`** folder (the one that contains `app.py`) and click
   **Select Folder**.
3. You should see `app.py`, `chatbot/`, `templates/`, `static/` in the left Explorer panel.

## Step 5 — Open the VS Code terminal

- Press **`Ctrl + ` `** (the backtick key, under Esc) — or menu **Terminal → New Terminal**.
- A terminal opens at the bottom. Make sure its path ends with `cu-campus-assistant`, e.g.:
  ```
  C:\Users\YourName\cu-campus-assistant>
  ```

## Step 6 — (Recommended) Create a virtual environment

This keeps the project's packages separate. In the terminal run:

**Windows:**
```
python -m venv venv
venv\Scripts\activate
```
**Mac / Linux:**
```
python3 -m venv venv
source venv/bin/activate
```
You'll see `(venv)` appear at the start of the terminal line — that means it's active.
(If you skip this step, the project still runs fine.)

## Step 7 — Install the project's packages

In the same terminal, run:
```
pip install -r requirements.txt
```
This installs Flask (the only dependency). Wait until it finishes.

## Step 8 — Select the Python interpreter (VS Code)

1. Press **`Ctrl + Shift + P`** to open the Command Palette.
2. Type **“Python: Select Interpreter”** and press Enter.
3. Choose the interpreter from your folder — it looks like
   `./venv/Scripts/python.exe ('venv')` if you made a venv, otherwise any Python 3.10+.

## Step 9 — Run the server 🎉

**Option A — from the terminal (recommended):**
```
python app.py
```
(Mac/Linux: `python3 app.py`)

You should see:
```
* Running on http://127.0.0.1:5000
* Running on http://0.0.0.0:5000
```

**Option B — using the Play button:**
Open `app.py` in the editor and click the ▶️ **Run Python File** button at the top-right.

## Step 10 — Open the chatbot in your browser

1. Open **Chrome** or **Edge** (best for the voice features).
2. Go to:  **http://localhost:5000**
3. Start chatting! 🎓 Try: *“How do I get admission?”*, *“B.Tech CSE fees”*, *“Placements”*.

## Step 11 — To stop the server

Click in the terminal and press **`Ctrl + C`**. To start again, just run
`python app.py` again.

---

## ⚙️ (Optional) Make answers AI-generated with a free LLM

1. Get a **free** API key at **https://console.groq.com** (sign up → API Keys → Create).
2. In the VS Code terminal, set these environment variables, then run:

**Windows (Command Prompt):**
```
set GROQ_API_KEY=gsk_your_key_here
set CU_USE_LLM=1
python app.py
```
**Windows (PowerShell):**
```
$env:GROQ_API_KEY="gsk_your_key_here"
$env:CU_USE_LLM="1"
python app.py
```
**Mac / Linux:**
```
export GROQ_API_KEY=gsk_your_key_here
export CU_USE_LLM=1
python3 app.py
```
Without a key, the built-in knowledge-base engine answers everything offline — no internet needed.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `'python' is not recognized` | Re-run the Python installer and **tick “Add Python to PATH”**. Or use `py app.py` / `python3 app.py`. |
| `'pip' is not recognized` | Same PATH fix; or try `python -m pip install -r requirements.txt`. |
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install -r requirements.txt` (make sure the terminal is in the `cu-campus-assistant` folder). |
| `Address already in use` / port 5000 busy | Stop the other server with `Ctrl + C`, or run on another port: `set PORT=5050 && python app.py` (Windows) / `PORT=5050 python3 app.py` (Mac/Linux), then open http://localhost:5050. |
| I edited a file but nothing changed | Stop the server (`Ctrl + C`) and start it again with `python app.py`. |
| 🎤 Mic doesn't work | Use **Chrome or Edge**, open via **http://localhost:5000** (not `file://`), and click **Allow** when it asks for microphone permission. |
| 404 on CSS/JS or page looks plain | Make sure you opened the **folder** containing `app.py` (not a parent folder), and run `app.py` — don't double-click the HTML file. |
| Emojis look weird in terminal | Harmless — the web page displays them fine. |

## ✅ Quick recap (every time you want to run it)

```
1. Open VS Code → File → Open Folder → cu-campus-assistant
2. Terminal (Ctrl + `)
3. pip install -r requirements.txt      (only needed the first time)
4. python app.py
5. Open http://localhost:5000 in Chrome
6. Ctrl + C to stop
```
