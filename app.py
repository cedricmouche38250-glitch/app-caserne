import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Caserne", layout="centered")

st.title("🚒 Vérifications Engins")

try:
    # Connexion
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Lecture forcée
    df = conn.read(ttl=0)
    
    if df.empty:
        st.warning("Le tableau est vide.")
    else:
        for index, row in df.iterrows():
            with st.container(border=True):
                # Affichage simple sans image pour tester
                st.subheader(f"Engin : {row['Engin']}")
                agent = row['Verificateur'] if pd.notnull(row['Verificateur']) else "À désigner"
                st.write(f"👤 Actuel : **{agent}**")
                
               with st.expander("Modifier"):
    with st.form(key=f"f_{index}"):
        # Remplacement du text_input par un selectbox avec recherche
        nouveau = st.selectbox(
            "Sélectionner l'agent", 
            options=liste_agents,
            index=0,
            key=f"sel_{index}",
            help="Tapez les premières lettres du nom pour filtrer"
        )
        
        if st.form_submit_button("Valider la garde"):
            if nouveau == "":
                st.error("Veuillez choisir un nom.")
            else:
                df.at[index, 'Verificateur'] = nouveau
                conn.update(data=df)
                st.success(f"Garde validée pour {nouveau} !")
                st.rerun()
except Exception as e:
    st.error(f"Erreur de lecture : {e}")
    st.info("Vérifiez que l'URL dans les Secrets est la bonne et que le Sheets est partagé en 'Éditeur'.")
