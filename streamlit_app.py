import streamlit as st
import pandas as pd
from datetime import datetime

# Mock data for the dashboard
data = {
    "FIN": [],
    "Produktvariante": [],
    "Im Takt?": [],
    "Fehlercode": [],
    "Bemerkung": [],
    "Qualität": [],
    "Meldezeit": [],
    "Taktzeit": []
}

df = pd.DataFrame(data)

# Set page configuration
st.set_page_config(page_title="Produktionsdokumentation Dashboard", layout="wide")

# Title and Logo
st.sidebar.image("logo.png", use_column_width=True)
st.sidebar.title("Produktionsdokumentation")

# Form to Input Data
with st.form("data_entry_form"):
    st.subheader("Auftragsdaten SATTELHALS eingeben")
    arbeitsplatz = st.text_input("Ausgewählter Arbeitsplatz", "Sattelhals", disabled=True)
    fin = st.text_input("FIN")
    variante = st.selectbox("Variante", ["Standard", "RoRo", "Co2"])
    datum_schichtbeginn = st.date_input("Datum Schichtbeginn", datetime.today())
    schicht = st.selectbox("Schicht", ["Früh", "Spät", "Nacht"])
    meldezeit = st.time_input("Meldezeit", datetime.now().time())
    zeit_letzte_meldung = st.time_input("Zeit letzte Meldung", datetime.now().time())
    zeit_seit_letzter_meldung = st.number_input("Zeit seit letzter Meldung (Minuten)", min_value=0, value=0)
    vorgegebene_taktzeit = st.text_input("Vorgegebene Taktzeit", "00:25:30", disabled=True)
    in_taktzeit_gefertigt = st.radio("In Taktzeit gefertigt?", ["Ja", "Nein"])
    fehlercode = st.selectbox("Fehlercode", [
        "Störung auswählen", "Technische Störung", "Zündfehler", "Warten auf Logistik",
        "Brennerwechsel", "Fehler ohne Alarm", "Rüsten", "Drachtwechsel", "Anlage nicht besetzt", "Sonstiges"
    ])
    bemerkungen = st.text_area("Bemerkungen")
    qualitaet = st.radio("Qualität des gefertigten Produktes?", [
        "i.O. fehlerfrei / Direktläufer", "e.i.O. Nacharbeit nötig", "n.i.O. Ausschuss"
    ])
    submit_button = st.form_submit_button(label="Eingabe")

# Handling form submission
if submit_button:
    new_data = {
        "FIN": fin,
        "Produktvariante": variante,
        "Im Takt?": in_taktzeit_gefertigt,
        "Fehlercode": fehlercode if fehlercode != "Störung auswählen" else "",
        "Bemerkung": bemerkungen,
        "Qualität": qualitaet,
        "Meldezeit": meldezeit.strftime("%H:%M"),
        "Taktzeit": vorgegebene_taktzeit
    }
    df = df.append(new_data, ignore_index=True)
    st.success(f"Sattelhals Daten hinzugefügt: FIN {fin}")

# Display Table with Data Entries
st.subheader("Schichtübersicht")
st.table(df)

# Button to delete the last entry
if st.button("Letzten Eintrag löschen"):
    if not df.empty:
        df = df[:-1]
        st.warning("Der letzte Eintrag wurde gelöscht.")
    else:
        st.warning("Es gibt keine Einträge zum Löschen.")

# Save the data to a CSV file
if st.button("Daten speichern"):
    df.to_csv("produktionsdaten.csv", index=False)
    st.success("Daten wurden erfolgreich gespeichert.")
