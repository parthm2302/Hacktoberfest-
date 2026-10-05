"""Hintly - snap a problem, get hints (not answers).

Built with Gemma 4 (open-weights model) via the Gemini API + Streamlit.
"""
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # reads GEMINI_API_KEY from a local .env file

MODEL = "gemma-4-26b-a4b-it"  # alternative: "gemma-4-31b-it"

HINT_LEVELS = {
    "1 - Nudge": "Give ONE short nudge that points to the key idea. Do not show any steps or the answer.",
    "2 - Method": "Name the concept/formula needed and outline the approach in 2-4 bullets. Do NOT compute or reveal the final answer.",
    "3 - Worked steps": "Walk through the full solution step by step and end with the final answer.",
}

SYSTEM_PROMPT = """You are Hintly, a patient tutor for school and college students.
The student shares a photo of a problem (textbook, notes, diagram, circuit, whiteboard).
First, briefly restate what the problem is asking so the student can confirm you read it correctly.
Then follow the hint level you are given EXACTLY. Never reveal more than the level allows.
Keep answers short, friendly and clear. Reply in the language requested."""


@st.cache_resource
def get_client():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        st.error("GEMINI_API_KEY is missing. Copy .env.example to .env and add your key.")
        st.stop()
    return genai.Client(api_key=key)


def ask(history, image_bytes, mime, level, subject, language):
    """Send the whole conversation (plus the image) to Gemma and return its reply."""
    contents = []
    for i, msg in enumerate(history):
        parts = []
        if i == 0 and msg["role"] == "user":  # attach the photo to the first message only
            parts.append(types.Part.from_bytes(data=image_bytes, mime_type=mime))
        parts.append(types.Part.from_text(text=msg["text"]))
        contents.append(types.Content(role=msg["role"], parts=parts))

    config = types.GenerateContentConfig(
        system_instruction=f"{SYSTEM_PROMPT}\nSubject: {subject}\nLanguage: {language}\n"
        f"Hint level: {HINT_LEVELS[level]}"
    )
    response = get_client().models.generate_content(model=MODEL, contents=contents, config=config)
    return response.text


# ---------------- UI ----------------
st.set_page_config(page_title="Hintly", page_icon="💡")
st.title("💡 Hintly")
st.caption("Snap a problem. Get a hint, not the answer. Powered by Gemma 4 (open weights).")

with st.sidebar:
    st.header("Settings")
    level = st.radio("Hint level", list(HINT_LEVELS))
    subject = st.selectbox("Subject", ["Maths", "Physics", "Chemistry", "Electronics", "Programming", "Other"])
    language = st.selectbox("Reply language", ["English", "Tamil", "Hindi"])
    if st.button("Start over"):
        st.session_state.clear()
        st.rerun()

source = st.radio("Photo source", ["Upload", "Camera"], horizontal=True)
photo = st.file_uploader("Upload a photo", type=["png", "jpg", "jpeg"]) if source == "Upload" else st.camera_input("Take a photo")

if photo:
    st.image(photo, width=350)
    image_bytes, mime = photo.getvalue(), photo.type or "image/jpeg"

    if "history" not in st.session_state:
        st.session_state.history = []

    if st.button("Get hint 💡", type="primary") and not st.session_state.history:
        st.session_state.history.append({"role": "user", "text": "Please help me with this problem."})
        with st.spinner("Thinking..."):
            reply = ask(st.session_state.history, image_bytes, mime, level, subject, language)
        st.session_state.history.append({"role": "model", "text": reply})

    # show conversation
    for msg in st.session_state.history[1:]:
        with st.chat_message("assistant" if msg["role"] == "model" else "user"):
            st.write(msg["text"])

    # follow-ups
    if st.session_state.history:
        followup = st.chat_input("Ask a follow-up, or pick a deeper hint level in the sidebar and ask again")
        if followup:
            st.session_state.history.append({"role": "user", "text": followup})
            with st.spinner("Thinking..."):
                reply = ask(st.session_state.history, image_bytes, mime, level, subject, language)
            st.session_state.history.append({"role": "model", "text": reply})
            st.rerun()
