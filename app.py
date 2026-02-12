import streamlit as st
import tempfile
import os
import pandas as pd

# 1. DEFZÍVNY IMPORT KNIŽNICE
try:
    import tacho
    from tacho import tacho as tacho_module  # Skúsime vnorený modul
    ST_READY = True
except ImportError:
    ST_READY = False

st.set_page_config(page_title="Tacho Parser v3", layout="wide", page_icon="🚛")

st.title("🚛 Profesionálny DDD Parser")
st.markdown("---")

if not ST_READY:
    st.error("Knižnica 'tacho' nie je správne nainštalovaná v prostredí.")
else:
    uploaded_file = st.file_uploader("Nahrajte súbor karty vodiča (.ddd)", type=["ddd"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ddd") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            with st.spinner('Analyzujem štruktúru súboru...'):
                # SKÚŠAME RÔZNE SPÔSOBY VOLANIA PODĽA VERZIE 0.8.8
                data = None
                
                # Možnosť A: Volanie cez tacho.tacho.Tacho()
                try:
                    from tacho.tacho import Tacho
                    obj = Tacho()
                    obj.load(tmp_path)
                    data = obj.to_dict()
                except:
                    # Možnosť B: Volanie cez tacho.load()
                    try:
                        data = tacho.load(tmp_path).to_dict()
                    except:
                        # Možnosť C: Diagnostika dostupných funkcií
                        st.warning("Hľadám správny procesor pre tento typ .ddd súboru...")
                        # Ak zlyhajú štandardné cesty, vypíšeme, čo knižnica obsahuje
                        available_tools = dir(tacho)
                        st.write(f"Dostupné nástroje v knižnici: {available_tools}")
                        raise Exception("Nepodarilo sa nájsť kompatibilnú metódu parsovania.")

            if data:
                st.success("Súbor bol úspešne dekódovaný!")
                
                tab1, tab2 = st.tabs(["📊 Prehľad", "🔍 Technický JSON"])
                
                with tab1:
                    st.subheader("Identifikácia")
                    # Dynamické zobrazenie kľúčových dát
                    st.info("Dáta sú pripravené nižšie v technickom formáte.")
                    
                with tab2:
                    st.json(data)

        except Exception as e:
            st.error(f"Technická chyba: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

st.sidebar.caption("Lokalizácia: Slovensko | Verzia 3.0")
