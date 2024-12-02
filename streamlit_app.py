import streamlit as st

# HTML-Datei laden
html_file = "index(1).html"  # Pfad zur Datei

# HTML-Inhalt lesen
with open(html_file, "r", encoding="utf-8") as file:
    html_content = file.read()

# HTML-Inhalt in Streamlit anzeigen
st.markdown(html_content, unsafe_allow_html=True)
