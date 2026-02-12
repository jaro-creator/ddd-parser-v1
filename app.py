import streamlit as st
import pytacho
import tempfile
import os
import pandas as pd

st.set_page_config(page_title="Tacho Parser Final", layout="wide", page_icon="🚛")

st.title("🚛 Profesionálny DDD Parser (Stable)")
st.info("Aktuálne beží na engine: pytacho | Python 3.11")

uploaded_file = st.file_uploader("Nahrajte súbor .ddd", type=["ddd"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ddd") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        with st.spinner('Analyzujem dáta tachografu...'):
            # Pytacho parsuje súbor priamo do čitateľného objektu
            data = pytacho.parse_file(tmp_path)
            
        st.success(f"Súbor {uploaded_file.name} bol úspešne spracovaný!")

        # --- ZOBRAZENIE DÁT ---
        tab1, tab2 = st.tabs(["📊 Prehľad", "🔍 Surové dáta"])

        with tab1:
            st.subheader("Identifikácia")
            # Skúsime dynamicky zobraziť kľúčové informácie
            st.info("Súbor bol úspešne dekódovaný. Pre technické detaily pozrite druhú záložku.")
            
            # Ak sú v dátach aktivity, pokúsime sa ich zobraziť
            if hasattr(data, 'activities'):
                st.write("**Zistené aktivity:**")
                st.write(data.activities)

        with tab2:
            # Pytacho objekty sa dajú krásne zobraziť ako text alebo slovník
            st.write(data)

    except Exception as e:
        st.error(f"Chyba pri analýze: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

st.sidebar.markdown("---")
st.sidebar.caption("Streamlit 1.54 | Engine: pytacho")
