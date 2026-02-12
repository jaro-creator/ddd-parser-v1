import streamlit as st
import tacho
import tempfile
import os
import pandas as pd

# Nastavenie stránky
st.set_page_config(page_title="Tacho Explorer", layout="wide")

st.title("🚛 Python Tacho Parser")
st.write("Nahrajte `.ddd` súbor a okamžite uvidíte výsledky.")

uploaded_file = st.file_uploader("Vyberte súbor (karta vodiča)", type=["ddd"])

if uploaded_file:
    # 1. Uloženie do dočasného súboru
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ddd") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        with st.spinner('Analyzujem...'):
            # 2. Parsovanie pomocou knižnice tacho
            obj = tacho.parse(tmp_path)
            
            # Pre účely zobrazenia to prevedieme na slovník (JSON)
            data = obj.to_dict()

        st.success(f"Súbor {uploaded_file.name} bol úspešne spracovaný.")

        # 3. Rozhranie s kartami
        tab1, tab2 = st.tabs(["📊 Prehľad", "🔍 Surové JSON dáta"])

        with tab1:
            st.subheader("Základné informácie")
            # Skúsime nájsť meno vodiča v štruktúre
            # Poznámka: Štruktúra sa líši podľa typu súboru (vodič vs vozidlo)
            st.write("Dáta boli úspešne načítané do pamäte.")
            st.info("Knižnica 'tacho' rozpoznala štruktúru súboru.")

        with tab2:
            st.json(data)

    except Exception as e:
        st.error(f"Chyba pri čítaní: {e}")
    finally:
        # 4. Upratanie dočasného súboru
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

st.sidebar.markdown("---")
st.sidebar.write("Použitá knižnica: `tacho` (Python native)")
