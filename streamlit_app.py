import streamlit as st
import pandas as pd
from datetime import datetime

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "FIN", "Produktvariante", "Im Takt?", "Fehlercode", "Bemerkung", "Qualität", "Meldezeit", "Taktzeit"
    ])

st.title("Produktionsdokumentation")
arbeitsbereich = st.sidebar.selectbox("Arbeitsbereich auswählen:", ["Sattelhals", "Lackierung"])
datum = st.sidebar.date_input("Datum auswählen:", value=datetime.now().date())
schicht = st.sidebar.selectbox("Schicht auswählen:", ["Früh", "Spät", "Nacht"])

st.header("Daten hinzufügen")
with st.form("entry_form"):
    fin = st.text_input("FIN")
    produktvariante = st.selectbox("Produktvariante", ["Standard", "RoRo", "Co2"])
    im_takt = st.radio("Im Takt gefertigt?", ["Ja", "Nein"], horizontal=True)
    fehlercode = st.selectbox(
        "Fehlercode auswählen:",
        ["Keine", "Technische Störung", "Zündfehler", "Warten auf Logistik", "Brennerwechsel", "Sonstiges"]
    )
    bemerkung = st.text_area("Bemerkungen")
    qualität = st.radio(
        "Qualität des Produkts:",
        ["i.O. (fehlerfrei)", "e.i.O. (Nacharbeit nötig)", "n.i.O. (Ausschuss)"],
        horizontal=True
    )
    meldezeit = st.time_input("Meldezeit:", value=datetime.now().time())
    taktzeit = st.text_input("Taktzeit (z. B. 00:25:30):", value="00:25:30")
    
    submitted = st.form_submit_button("Eintrag hinzufügen")
    if submitted:
        new_entry = {
            "FIN": fin,
            "Produktvariante": produktvariante,
            "Im Takt?": im_takt,
            "Fehlercode": fehlercode,
            "Bemerkung": bemerkung,
            "Qualität": qualität,
            "Meldezeit": str(meldezeit),
            "Taktzeit": taktzeit
        }
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_entry])], ignore_index=True)
        st.success("Eintrag wurde erfolgreich hinzugefügt!")

st.header("Aktuelle Einträge")
st.dataframe(st.session_state.data)

if st.button("Letzten Eintrag löschen"):
    if not st.session_state.data.empty:
        st.session_state.data = st.session_state.data.iloc[:-1]
        st.success("Der letzte Eintrag wurde gelöscht.")
    else:
        st.warning("Keine Einträge zum Löschen vorhanden.")
