import streamlit as st
import os
import tempfile
import pandas as pd
import importlib

st.set_page_config(page_title="Tacho Parser Final", layout="wide", page_icon="🚛")

st.title("🚛 Profesionálny DDD Parser")
st.markdown("---")

# --- DIAGNOSTIKA A IMPORT ---
try:
    import tacho
    # Skúsime nájsť cestu, kde je tacho nainštalované
    tacho_path = os.path.dirname(tacho.__file__)
    st.sidebar.success(f"Knižnica nájdená v: {tacho_path}")
except Exception as e:
    st.error(f"Knižnica tacho sa nenačítala: {e}")
    tacho = None

uploaded_file = st.file_uploader("Nahrajte .ddd súbor", type=["ddd"])

if uploaded_file and tacho:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ddd") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        with st.spinner('Spracúvam...'):
            # Skúšame volanie cez dynamický import podmodulu
            # Verzia 0.8.8 má hlavnú logiku v tacho.tacho alebo tacho.reader
            try:
                from tacho.tacho import Tacho
                parser = Tacho()
                parser.load(tmp_path)
                data = parser.to_dict()
            except:
                # Ak zlyhá Tacho, skúsime priamo čítačku
                from tacho.reader import Reader
                with open(tmp_path, 'rb') as f:
                    data = Reader(f.read()).to_dict()

        st.success("Analýza úspešná!")
        st.json(data)

    except Exception as e:
        st.error(f"Chyba pri parsovaní: {e}")
        st.info("Tip: Skúste v Settings Streamlitu zmeniť Python späť na 3.11, ak je to možné.")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
