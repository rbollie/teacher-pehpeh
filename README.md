# 🎓 Teacher AI Assistant

## What This Is
A web application that helps teachers in underresourced communities by combining the intelligence of **three AI models** (ChatGPT, Claude, and Gemini) into one tool. Teachers select their classroom context, ask a question, and get a synthesized best-possible answer.

---

## 🚀 SETUP INSTRUCTIONS (Step by Step)

### Step 1: Install Python
1. Go to **https://www.python.org/downloads/**
2. Click the big yellow **"Download Python"** button
3. Run the installer
4. ⚠️ **IMPORTANT:** Check the box that says **"Add Python to PATH"** before clicking Install
5. Click **"Install Now"**

**To verify it worked:** Open your Terminal (Mac) or Command Prompt (Windows) and type:
```
python --version
```
You should see something like `Python 3.12.x`

---

### Step 2: Download This Project
Save the entire `teacher_ai_assistant` folder to your computer. Inside it you should have:
```
teacher_ai_assistant/
├── app.py              ← The main application
├── requirements.txt    ← List of packages needed
└── README.md           ← This file
```

---

### Step 3: Install Required Packages
Open Terminal (Mac) or Command Prompt (Windows), then navigate to the project folder:

**On Mac:**
```bash
cd ~/Desktop/teacher_ai_assistant
```

**On Windows:**
```bash
cd C:\Users\YourName\Desktop\teacher_ai_assistant
```

Then install everything with one command:
```bash
pip install -r requirements.txt
```

Wait for it to finish (may take 1-2 minutes).

---

### Step 4: Get Your API Keys (The "VIP Passes")

You need to create accounts and get a key from each AI company. Each takes about 2 minutes.

#### 🟢 OpenAI (for ChatGPT)
1. Go to **https://platform.openai.com**
2. Sign up or log in
3. Click your profile icon → **"API Keys"**
4. Click **"Create new secret key"**
5. Copy the key (starts with `sk-...`)
6. Add $5 credit at **https://platform.openai.com/settings/organization/billing**

#### 🟣 Anthropic (for Claude)
1. Go to **https://console.anthropic.com**
2. Sign up or log in
3. Go to **Settings → API Keys**
4. Click **"Create Key"**
5. Copy the key (starts with `sk-ant-...`)
6. Add $5 credit in the Billing section

#### 🔵 Google (for Gemini)
1. Go to **https://aistudio.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key
5. Google gives you free credits to start!

---

### Step 5: Add Your Keys to the App

1. Open the file **`app.py`** in any text editor (Notepad, TextEdit, or VS Code)
2. Find these lines near the top (around line 20):

```python
OPENAI_API_KEY = ""       # Paste your OpenAI key here
ANTHROPIC_API_KEY = ""    # Paste your Anthropic key here
GOOGLE_API_KEY = ""       # Paste your Google AI key here
```

3. Paste your keys between the quotes. It should look like this:

```python
OPENAI_API_KEY = "sk-abc123..."
ANTHROPIC_API_KEY = "sk-ant-abc123..."
GOOGLE_API_KEY = "AIzaSy..."
```

4. **Save the file**

---

### Step 6: Run the App! 🎉

In your Terminal/Command Prompt (still in the project folder), type:

```bash
streamlit run app.py
```

Your browser will automatically open to **http://localhost:8501** and you'll see the app!

---

## 📱 HOW TO USE THE APP

### Left Sidebar (Set Once)
Set your classroom context — these settings apply to every question:
| Setting | What It Means |
|---|---|
| **Country** | Your country (affects cultural context in responses) |
| **School Setting** | Urban, Rural, etc. (affects resource assumptions) |
| **Grade Level** | Grade 7–12 |
| **Subject** | The subject you teach |
| **Class Size** | How many students |
| **Resources** | What you have available |
| **Language** | Language context for your classroom |
| **Student Ability** | General ability level of your class |

### Main Area (Use Each Time)
1. **Select what you need** (Lesson Plan, Quiz, WASSCE Questions, etc.)
2. **Set the time available** for the lesson
3. **Type the topic** (e.g., "Photosynthesis")
4. **Write your question** with as much detail as possible
5. Click **"Generate Response"**

### Viewing Results
- **Best Combined Answer** — The app sends your question to all 3 AIs, then combines the best ideas into one response (recommended!)
- **Side-by-Side** — See each AI's response separately in tabs

---

## 💰 COST INFORMATION

The app uses the most affordable models by default:

| Model | Approximate Cost |
|---|---|
| GPT-4o-mini | ~$0.001 per question |
| Claude Haiku | ~$0.001 per question |
| Gemini Flash | ~$0.0005 per question |
| Synthesis step | ~$0.005 per question |

**Total: About $0.008 (less than 1 cent) per question**

$5 on each platform will give you **thousands** of questions.

---

## 🌐 DEPLOYING ONLINE (So Teachers Can Access It)

Once you've tested it locally, you can put it online for free:

### Option A: Streamlit Community Cloud (Easiest)
1. Create a free account at **https://github.com** 
2. Upload your project folder to a new repository
3. Go to **https://share.streamlit.io**
4. Connect your GitHub account
5. Select your repository
6. Add your API keys as **"Secrets"** (so they're not visible in code):
   - In Streamlit Cloud, go to App Settings → Secrets
   - Add them in this format:
   ```
   OPENAI_API_KEY = "sk-..."
   ANTHROPIC_API_KEY = "sk-ant-..."
   GOOGLE_API_KEY = "AIzaSy..."
   ```
7. Click **Deploy!**

Your app will be live at a URL like: `https://your-app-name.streamlit.app`

### Option B: For WhatsApp Access (Advanced)
If teachers need to access via WhatsApp:
1. Sign up at **https://www.twilio.com** (has free tier)
2. Use Twilio's WhatsApp sandbox for testing
3. This requires additional code — let me know and I can build this extension

---

## 🔧 TROUBLESHOOTING

| Problem | Solution |
|---|---|
| `python: command not found` | Reinstall Python and make sure "Add to PATH" is checked |
| `pip: command not found` | Try `python -m pip install -r requirements.txt` instead |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| API key error | Double-check you pasted the key between the quotes correctly |
| "Rate limit exceeded" | Wait a minute and try again, or add more credit to your account |
| App won't load | Make sure you're in the right folder when running `streamlit run app.py` |

---

## 📝 WHAT'S NEXT?

Ideas for improving this tool:
- [ ] Add a question history / saved responses feature
- [ ] Add WhatsApp integration via Twilio
- [ ] Add offline caching for common topics
- [ ] Create a teacher feedback system
- [ ] Add support for more exam systems (NECO, GCE, KCSE, etc.)
- [ ] Multi-language interface (not just English)

---

## ❤️ CREDITS

Built to support teachers in underresourced communities across Sub-Saharan Africa.
Powered by OpenAI, Anthropic, and Google AI.
