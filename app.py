import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Configuration de la page
st.set_page_config(page_title="Vérifications Engins", layout="centered")

st.title("🚒 Gestion des Vérifications")

# Connexion au Google Sheets (utilisant la nouvelle méthode simplifiée)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=0)

    # Affichage des engins
    for index, row in df.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns()
            
            with col1:
                # Vérifie si une URL de photo existe, sinon met une image par défaut
                if row['Photo']:
                    st.image(row['Photo'], use_container_width=True)
                else:
                    st.write("Pas de photo")
            
            with col2:
                st.subheader(row['Engin'])
                verificateur = row['Verificateur'] if row['Verificateur'] else "À désigner"
                st.write(f"Vérificateur : **{verificateur}**")
                
                # Petit formulaire pour changer le nom
                with st.expander("Modifier"):
                    with st.form(key=f"form_{index}"):
                        nouveau_nom = st.text_input("Nom de l'agent", value=row['Verificateur'])
                        if st.form_submit_button("Enregistrer"):
                            df.at[index, 'Verificateur'] = nouveau_nom
                            conn.update(data=df)
                            st.success("Mise à jour réussie !")
                            st.rerun()
except Exception as e:
    st.error("L'application n'est pas encore connectée au Google Sheets.")
    st.info("Allez dans les paramètres Streamlit Cloud pour ajouter l'URL de votre feuille dans les Secrets.")
