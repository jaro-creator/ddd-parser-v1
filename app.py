import streamlit as st
import os
import subprocess
import sys
import tempfile

# --- AUTOMATICKÉ STIAHNUTIE KNIŽNICE ---
def prepare_library():
    if not os.path.exists("tachoparser"):
        st.info("Pripravujem prostredie (sťahujem parser)...")
        # Stiahneme len priečinok tachoparser z GitHubu
        subprocess.run(["git", "clone", "https://github.com/traconiq/tachoparser.git", "temp_repo"])
        # Presunieme dôležitý priečinok do hlavného adresára
        os.rename("temp_repo/tachoparser", "./tachoparser")
        # Upraceme
        subprocess.run(["rm", "-rf", "temp_repo"])
        st.rerun()

prepare_library()

from tachoparser import Tachoparser

# --- INTERFACE APLIKÁCIE ---
st.set_page_config(page_title="TachoParser Online", layout="centered")

st.title("🚛 Digitálny Tachograf Parser")
st.write("Nahrajte súbor `.ddd` pre rýchlu analýzu dát.")

uploaded_file = st.file_uploader("Vyberte súbor", type=["ddd"])

if uploaded_file:
    # Vytvorenie dočasného súboru
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ddd") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        with st.spinner('Spracúvam...'):
            # Inicializácia parsera
            tc = Tachoparser(tmp_path)
            data = tc.parse()

            st.success("Analýza dokončená!")
            
            # Zobrazenie výsledkov v prehľadných kartách
            col1, col2 = st.columns(2)
            
            # Skúsime vytiahnuť základné info (štruktúra závisí od obsahu .ddd)
            with col1:
                st.subheader("Identifikácia")
                st.write(f"Súbor: `{uploaded_file.name}`")
            
            st.divider()
            with st.expander("Zobraziť kompletné JSON dáta"):
                st.json(data)

    except Exception as e:
        st.error(f"Chyba pri analýze: {e}")
        st.info("Tip: Uistite sa, že ide o platný .ddd súbor z karty vodiča alebo tachografu.")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

st.sidebar.markdown("---")
st.sidebar.caption("Beží na Streamlit Cloud | Engine: traconiq/tachoparser")
