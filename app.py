import streamlit as st
import tempfile
import os
from py_ddd_parser import DDD

st.set_page_config(page_title="Tacho Parser Final", layout="wide")

st.title("🚛 Finálny DDD Parser")
st.write("Tento systém používa stabilný motor py-ddd-parser.")

uploaded_file = st.file_uploader("Nahrajte súbor .ddd", type=["ddd"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ddd") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        with st.spinner('Spracúvam...'):
            # Načítanie a parsovanie
            parsed_data = DDD.parse(tmp_path)
            
            # Získanie textového výstupu
            output = str(parsed_data)

        st.success("Analýza úspešne dokončená!")
        
        st.subheader("Výsledky zo súboru")
        st.text_area("Detailný výpis:", output, height=600)

    except Exception as e:
        st.error(f"Chyba pri čítaní: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
