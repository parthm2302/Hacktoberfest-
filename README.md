# 💡 Hintly

Snap a photo of a problem and get **hints, not answers**. Hintly helps students learn by revealing only as much as they ask for.

Built for Hacktoberfest 2026 Hack Day (Android Club VITC) with **Gemma 4**, Google's open-weights multimodal model, via the Gemini API.

🚀 **Live demo:** https://hintly.streamlit.app

## Features
- Upload a photo or use your camera (textbook, notes, diagrams, whiteboards)
- 3 hint levels: Nudge, Method, Worked steps
- Replies in English, Tamil or Hindi
- Follow-up questions in a chat

## Run it
```bash
git clone https://github.com/parthm2302/Hacktoberfest-.git
cd Hacktoberfest-
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then paste your free key from aistudio.google.com/apikey
streamlit run app.py
```

## How it works
The app sends your photo plus a tutor system prompt to `gemma-4-26b-a4b-it`. The chosen hint level is injected into the prompt so the model never reveals more than allowed.

## Roadmap
- Run Gemma 4 locally (Ollama / llama.cpp) for fully offline use
- Export problems and hints as flashcards
- More languages

## Contributing
PRs welcome! Good first issues: add a language, improve the prompts, add tests.

## License
MIT
