import streamlit as st
from tacho import Tacho  # Správny import pre verziu 0.8.8
import tempfile
import os
import pandas as pd

st.set_page_config(page_title="Tacho Explorer", layout="wide", page_icon="🚛")

st.title("🚛 Profesionálny DDD Parser")
st.markdown("---")

uploaded_file = st.file_uploader("Nahrajte súbor karty vodiča (.ddd)", type=["ddd"])

if uploaded_file:
    # Vytvorenie dočasného súboru
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ddd") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        with st.spinner('Dekódujem dáta...'):
            # SPRÁVNE VOLANIE PRE VERZIU 0.8.8
            tacho_obj = Tacho.from_file(tmp_path)
            data = tacho_obj.to_dict()
            
        st.success(f"Súbor {uploaded_file.name} bol úspešne spracovaný!")

        # --- ZOBRAZENIE DÁT ---
        tab1, tab2 = st.tabs(["📊 Prehľad", "🔍 Technický JSON"])

        with tab1:
            st.subheader("Základné informácie")
            # Skúsime vytiahnuť meno, ak je v štruktúre prítomné
            # Štruktúra v tacho býva hlboko vnorená
            st.info("Súbor bol úspešne načítaný do objektového modelu.")
            st.write("Dáta sú pripravené na analýzu v technickom výpise.")

        with tab2:
            st.json(data)

    except Exception as e:
        st.error(f"Chyba pri spracovaní: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

st.sidebar.markdown("---")
st.sidebar.caption("Použitá knižnica: tacho v0.8.8")
