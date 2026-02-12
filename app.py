import streamlit as st
import os
import tempfile

# Úplne základný import - bez try/except, aby sme videli reálnu chybu v logu ak neprejde
import tacho

st.set_page_config(page_title="Tacho Parser Fix", layout="wide", page_icon="🚛")

st.title("🚛 Profesionálny DDD Parser")
st.markdown("---")

# Kontrola čo všetko tacho obsahuje (uvidíš to v bočnom paneli pre diagnostiku)
st.sidebar.subheader("Diagnostika balíka")
st.sidebar.write(f"Verzia tacho: {getattr(tacho, '__version__', 'neznáma')}")
st.sidebar.write("Dostupné funkcie:", dir(tacho))

uploaded_file = st.file_uploader("Nahrajte súbor karty vodiča (.ddd)", type=["ddd"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ddd") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        with st.spinner('Čítam dáta...'):
            # Skúsime najbežnejšiu cestu pre verziu 0.8.8
            # tacho.Tacho() je trieda, ktorú musíme inicializovať
            from tacho import Tacho
            tc = Tacho()
            tc.load(tmp_path)
            data = tc.to_dict()

        st.success("Súbor bol úspešne prečítaný!")
        
        tab1, tab2 = st.tabs(["📊 Výsledky", "🔍 Surový výpis"])
        with tab1:
            st.info("Dáta sú pripravené v JSON formáte v susednej záložke.")
            # Tu neskôr pridáme pekné tabuľky
        with tab2:
            st.json(data)

    except Exception as e:
        st.error(f"Chyba pri spracovaní: {e}")
        st.write("Skúšam alternatívny spôsob...")
        
        # Alternatívny pokus ak by zlyhala trieda Tacho
        try:
            with open(tmp_path, 'rb') as f:
                data = tacho.parse(f.read()).to_dict()
            st.json(data)
        except Exception as e2:
            st.warning(f"Zlyhal aj druhý pokus: {e2}")

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
