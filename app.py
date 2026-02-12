import streamlit as st
import ddd_py
import tempfile
import os
import pandas as pd

st.set_page_config(page_title="Tacho Parser v4", layout="wide", page_icon="🚛")

st.title("🚛 Moderný DDD Parser")
st.info("Beží na engine ddd-py (Python 3.12+)")

uploaded_file = st.file_uploader("Nahrajte súbor .ddd", type=["ddd"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ddd") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        with st.spinner('Dekódujem dáta tachografu...'):
            # ddd-py načítanie
            parsed = ddd_py.DDD.parse(tmp_path)
            
            # Prevedieme základné info do slovníka pre zobrazenie
            # ddd-py má výbornú podporu pre rôzne bloky dát
            data_summary = str(parsed) 

        st.success("Súbor bol úspešne spracovaný!")

        tab1, tab2 = st.tabs(["📊 Prehľad dát", "📜 Surový výpis"])

        with tab1:
            st.subheader("Detailný výpis zo súboru")
            # ddd-py generuje veľmi podrobný textový výpis
            st.text_area("Výsledky analýzy:", data_summary, height=500)

        with tab2:
            st.write("V tejto záložke môžete vidieť dáta v neformátovanom tvare.")
            st.code(data_summary)

    except Exception as e:
        st.error(f"Chyba pri analýze: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

st.sidebar.markdown("---")
st.sidebar.caption("Lokalizácia: Slovensko | Engine: ddd-py")
