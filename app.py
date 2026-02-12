import streamlit as st
import tacho
import tempfile
import os
import pandas as pd

# Nastavenie vzhľadu
st.set_page_config(page_title="Tacho Parser", layout="wide", page_icon="🚛")

st.title("🚛 Profesionálny DDD Parser (Python)")
st.info("Nahrajte súbor .ddd a systém ho automaticky spracuje.")

uploaded_file = st.file_uploader("Vyberte .ddd súbor", type=["ddd"])

if uploaded_file:
    # Vytvorenie dočasného súboru
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ddd") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        with st.spinner('Analyzujem súbor...'):
            # OPRAVA: Knižnica tacho používa parse_file
            # Ak by nefungovalo, vyskúšame alternatívny prístup nižšie
            try:
                data_obj = tacho.parse_file(tmp_path)
                data = data_obj.to_dict()
            except AttributeError:
                # Niektoré verzie tacho vyžadujú otvorenie súboru
                with open(tmp_path, 'rb') as f:
                    data = tacho.parse(f.read()).to_dict()

        st.success("Dáta boli úspešne načítané!")

        # Zobrazenie výsledkov
        tab1, tab2 = st.tabs(["📊 Prehľad", "🔍 Surové dáta (JSON)"])

        with tab1:
            st.subheader("Identifikácia")
            # Skúsime dynamicky vypísať kľúčové polia
            if 'card_number' in data:
                st.write(f"**Číslo karty:** {data['card_number']}")
            
            st.warning("Pre detailný rozpis aktivít rozbalte kartu Surové dáta.")

        with tab2:
            st.json(data)

    except Exception as e:
        st.error(f"Chyba pri spracovaní: {e}")
        st.info("Skontrolujte, či je súbor platný .ddd súbor.")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

st.sidebar.caption("Verzia 2.0 | Engine: Python Tacho")
