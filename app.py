import streamlit as st
from tachoparser import Tachoparser
import tempfile
import os

st.title("Tachoparser Web App 🚛")
st.write("Nahrajte .ddd súbor a získajte dáta v čitateľnom formáte.")

uploaded_file = st.file_uploader("Vyberte .ddd súbor", type=["ddd"])

if uploaded_file is not None:
    # Uloženie do dočasného súboru, pretože tachoparser potrebuje cestu k súboru
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ddd") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        # Inicializácia a parsovanie
        parser = Tachoparser(tmp_path)
        data = parser.parse()

        st.success("Súbor úspešne spracovaný!")
        st.json(data) # Zobrazí surové JSON dáta
        
    except Exception as e:
        st.error(f"Chyba pri spracovaní: {e}")
    finally:
        os.remove(tmp_path)