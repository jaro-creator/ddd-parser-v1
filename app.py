import streamlit as st
import os
import tempfile
import pandas as pd

# --- INTELIGENTNÝ IMPORT ---
PARSER_ENGINE = None

# Skúsime Tacho (Možnosť 1)
try:
    from tacho.tacho import Tacho
    PARSER_ENGINE = "tacho"
except ImportError:
    # Skúsime py-ddd-parser (Možnosť 2 - stabilnejšia)
    try:
        from py_ddd_parser import DDD
        PARSER_ENGINE = "py-ddd-parser"
    except ImportError:
        PARSER_ENGINE = None

st.set_page_config(page_title="Tacho Parser Pro", layout="wide")
st.title("🚛 Profesionálny DDD Parser")

if not PARSER_ENGINE:
    st.error("Chyba: Žiadna knižnica na parsovanie nie je dostupná. Skontrolujte requirements.txt.")
else:
    st.sidebar.success(f"Aktívny motor: {PARSER_ENGINE}")
    uploaded_file = st.file_uploader("Nahrajte .ddd súbor", type=["ddd"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ddd") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            with st.spinner('Spracúvam súbor...'):
                if PARSER_ENGINE == "tacho":
                    from tacho.tacho import Tacho
                    tc = Tacho()
                    tc.load(tmp_path)
                    data = tc.to_dict()
                else:
                    # Spracovanie cez py-ddd-parser
                    from py_ddd_parser import DDD
                    parsed_ddd = DDD.parse(tmp_path)
                    # Prevod na slovník pre zobrazenie
                    data = str(parsed_ddd) 

            st.success("Analýza dokončená!")
            
            # Zobrazenie výsledkov
            tab1, tab2 = st.tabs(["📊 Prehľad", "🔍 Technické dáta"])
            
            with tab1:
                st.subheader("Informácie zo súboru")
                st.info(f"Súbor: {uploaded_file.name}")
                if PARSER_ENGINE == "py-ddd-parser":
                    st.text_area("Výpis dát:", data, height=400)
                else:
                    st.json(data)

            with tab2:
                if PARSER_ENGINE == "tacho":
                    st.json(data)
                else:
                    st.write("Dáta sú zobrazené v Prehľade.")

        except Exception as e:
            st.error(f"Chyba pri analýze: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
