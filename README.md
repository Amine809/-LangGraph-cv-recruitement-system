## CV Recruitment System (LangGraph + Streamlit)

An AI-powered multi-agent system that parses a candidate's CV, analyzes skills and experience, assesses cultural fit, calculates an aggregate score, and produces a hiring recommendation — all through a Streamlit UI.

### Features
- Multi-agent workflow using LangGraph
- CV parsing for structured data
- Skills, Experience, and Cultural Fit assessments
- Aggregate scoring and final recommendation
- JSON report download and local persistence

### Tech Stack
- Python 3.11+
- Streamlit UI
- LangGraph / LangChain
- OpenAI (via `langchain_openai`)

### Project Structure
- `app.py`: Streamlit app entry
- `agents/`: Agent implementations and workflow
- `prompts/`: Agent prompts
- `tools/cv_parser.py`: PDF/DOCX text extraction
- `utils/serialization.py`: JSON-safe serializer
- `utils/memory.py`: Save/load assessments
- `utils/state.py`: Typed state definitions

### Prerequisites
- Python 3.11 installed
- An OpenAI API key

### Setup (Windows CMD)
```cmd
cd C:\Users\hp\Desktop\cv-recruitment-system

:: Create venv
python -m venv venv

:: Activate venv
venv\Scripts\activate

:: Upgrade pip
python -m pip install --upgrade pip

:: Install dependencies
pip install -r requirements.txt

:: Configure environment
copy NUL .env
:: Open .env and add your key, e.g.:
:: OPENAI_API_KEY=sk-...
```

### Run the App (Windows CMD)
```cmd
cd C:\Users\hp\Desktop\cv-recruitment-system
venv\Scripts\activate
streamlit run app.py
```

Then open the URL shown (typically `http://localhost:8501`).

### How to Use
1. Upload a CV (PDF/DOCX) or paste CV text.
2. Enter job requirements and company culture.
3. Click "Start Analysis".
4. Explore tabs: Overview, Detailed Analysis, Skills Deep Dive, Experience Review, Final Recommendation.
5. In Final Recommendation, use "Download JSON Report" to export results.

### Notes
- JSON export is safe for complex objects (e.g., LangChain messages) using `utils/serialization.to_json_safe`.
- Saved assessments are written to `data/assessments`.

### Testing
```cmd
venv\Scripts\activate
python -m pytest -q
```

### Troubleshooting
- If the app cannot access the OpenAI API, confirm `OPENAI_API_KEY` in `.env`.
- If CV parsing seems empty, ensure the uploaded file text is extracted (see `tools/cv_parser.py`).
- To reset UI state, use the sidebar "Reset Analysis" button.

### License
MIT


