import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Caserne", layout="centered")
st.title("🚒 Vérifications Engins")

conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Chargement de la liste des agents depuis l'onglet 'Agents'
try:
    df_agents = conn.read(worksheet="Agents")
    liste_agents = [""] + df_agents.iloc[:, 0].tolist()
except:
    liste_agents = ["", "mouche", "rosset", "pierto"] # Liste de secours

# 2. Chargement des engins
df = conn.read(ttl=0)

for index, row in df.iterrows():
    with st.container(border=True):
        st.subheader(f"Engin : {row['Engin']}")
        agent_actuel = row['Verificateur'] if pd.notnull(row['Verificateur']) else "À désigner"
        st.write(f"👤 Actuel : **{agent_actuel}**")
        
        with st.expander("Modifier l'agent"):
            with st.form(key=f"form_{index}"):
                # La liste déroulante avec recherche
                nouveau = st.selectbox(
                    "Choisir un nom", 
                    options=liste_agents,
                    key=f"search_{index}"
                )
                
                if st.form_submit_button("Valider"):
                    if nouveau != "":
                        df.at[index, 'Verificateur'] = nouveau
                        # Mise à jour du Sheets
                        conn.update(data=df)
                        st.success("Mise à jour réussie !")
                        st.rerun()
