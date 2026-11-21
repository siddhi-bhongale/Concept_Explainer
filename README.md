# Concept Explainer (ELI5)

Complex topics confuse beginners. This app takes any concept and explains it at three levels: kid, student and expert.

## Pipeline
Concept input -> one prompt asking for 3 labelled levels as JSON -> Llama 3 (Ollama) -> each level shown in its own tab or expander

## Run
1. Install Ollama and pull the model: `ollama pull llama3`
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

## Notes
- Use the radio button to switch between tabs and expanders.
- Change `MODEL` in app.py if you use a different Ollama model.
- If the model returns broken JSON, the app tries to recover it, otherwise it asks you to try again.
