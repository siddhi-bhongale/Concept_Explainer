import json
import re

import requests
import streamlit as st

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

LEVELS = [
    ("kid", "Kid (ELI5)", "a 7-year-old: very simple words, a fun everyday example, no jargon"),
    ("student", "Student", "a college student: clear explanation with key terms defined and a small example"),
    ("expert", "Expert", "a professional in the field: precise, technical, mention internals and trade-offs"),
]


def build_prompt(concept):
    level_lines = "\n".join(f'- "{key}": explain for {desc}' for key, _, desc in LEVELS)
    return f"""Explain the concept "{concept}" at three levels.
{level_lines}

Each explanation should be 3-6 sentences.
Reply ONLY with JSON in this format:
{{"kid": "...", "student": "...", "expert": "..."}}
"""


def get_explanations(concept):
    resp = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": build_prompt(concept), "stream": False, "format": "json"},
        timeout=300,
    )
    resp.raise_for_status()
    raw = resp.json()["response"]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return None


st.set_page_config(page_title="Concept Explainer", layout="centered")
st.title("Concept Explainer (ELI5)")
st.write("Type any concept and get it explained at three levels: kid, student and expert.")

concept = st.text_input("Concept", placeholder="e.g. Recursion, Blockchain, Photosynthesis")
view = st.radio("Show levels as", ["Tabs", "Expanders"], horizontal=True)

if st.button("Explain") and concept.strip():
    with st.spinner("Thinking..."):
        try:
            st.session_state["result"] = (concept.strip(), get_explanations(concept.strip()))
        except requests.RequestException as e:
            st.error(f"Could not reach Ollama. Is it running? ({e})")
            st.stop()

saved = st.session_state.get("result")
if saved:
    name, data = saved
    if not data:
        st.warning("The model did not return a proper answer. Try again.")
    else:
        st.subheader(name)
        if view == "Tabs":
            for tab, (key, title, _) in zip(st.tabs([t for _, t, _ in LEVELS]), LEVELS):
                with tab:
                    st.write(data.get(key, "Not available."))
        else:
            for key, title, _ in LEVELS:
                with st.expander(title, expanded=(key == "kid")):
                    st.write(data.get(key, "Not available."))
