import streamlit as st
import os
import tempfile

# Pokus o import knižnice s kontrolou
try:
    from tachoparser import Tachoparser
    LIB_READY = True
except ImportError:
    LIB_READY = False

st.set_page_config(page_title="Tachoparser UI", layout="wide")

st.title("🚛 DDD Parser (Tachoparser)")

if not LIB_READY:
    st.error("❌ Knižnica 'tachoparser' nie je nainštalovaná. Skontrolujte requirements.txt a Logs.")
    st.info("V requirements.txt by malo byť: git+https://github.com/traconiq/tachoparser.git")
else:
    st.success("✅ Systém je pripravený na analýzu súborov.")
    
    uploaded_file = st.file_uploader("Nahrajte .ddd súbor (karta vodiča alebo vozidlo)", type=["ddd"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ddd") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            with st.spinner('Analyzujem dáta...'):
                parser = Tachoparser(tmp_path)
                data = parser.parse()
            
            st.divider()
            st.subheader("Výsledok analýzy (JSON)")
            st.json(data)
            
        except Exception as e:
            st.error(f"Chyba pri spracovaní súboru: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

st.sidebar.info("Tento nástroj používa knižnicu traconiq/tachoparser na dekódovanie digitálnych tachografov.")
