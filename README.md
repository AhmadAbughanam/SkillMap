# SkillMap-Flask 🚀

**SkillMap-Flask** is a self-improvement tracker that allows users to:

- Create and manage skills
- Track progress with milestones
- Automatically generate AI-powered insights using a local LLM

---

## 🧠 Features

- 🎯 **Skill Management** – Create, edit, delete skills by category and description
- 📈 **Milestone Tracking** – Log progress updates with timestamps and notes
- 🤖 **LLM Insights** – Auto-generate learning insights using a locally hosted LLM
- 📊 **Insight Dashboard** – View AI insights by section, skill, or generation time
- 🧱 Built with:
  - Flask
  - SQLAlchemy
  - Bootstrap
  - llama-cpp-python (Mistral 7B Instruct GGUF)

---

## 📂 Folder Structure

```

SkillMap-Flask/
│
├── app/
│   ├── templates/        # HTML templates
│   ├── static/           # Static files (CSS, JS)
│   ├── routes/           # Flask blueprints (skills, LLM)
│   ├── utils/            # LLM logic (llm\_client.py)
│   ├── models.py         # SQLAlchemy models
│   └── **init**.py       # App factory
│
├── models/
│   └── mistral-7b-instruct-v0.1.Q2\_K.gguf  # Local LLM model
│
├── venv/                 # Virtual environment
├── test.py               # Manual insight generation test
├── config.py             # (Optional) Config settings
├── requirements.txt
└── README.md

```

---

## ⚙️ Setup Instructions

1. **Clone the repo**:
   ```bash
   git clone https://github.com/your-username/SkillMap-Flask.git
   cd SkillMap-Flask
   ```

````

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download and place the LLM model** (e.g., Mistral 7B Instruct GGUF):

   * Place it in `app/models/` and update the `model_path` in `llm_client.py`.

5. **Run the app**:

   ```bash
   flask run
   ```
   another way by:

    python run.py

---

## 🧠 Local LLM Integration

* Uses `llama-cpp-python` to load a local GGUF model.
* Insights are generated when:

  * A new skill is created
  * A milestone is added
* Insight content is stored in the `llm_insights` table and displayed in the dashboard.

---

## 🛠️ Developer Notes

* Make sure `llama_cpp` is installed and your system supports AVX.
* Running on CPU; GPU support requires additional setup.
* Use `test.py` to verify model and generation output manually.

---

## ✅ Example Prompt

```python
from app.utils.llm_client import generate_llm_insight
from app.models import Skill

with app.app_context():
    skill = Skill.query.first()
    insights = generate_llm_insight(skill)
    print(insights)
```

---

## 📃 License

MIT License

````
