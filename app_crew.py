import streamlit as st
import pandas as pd
import os
from utils.multiagent_backend import run_fba_crew
from utils.memory import get_last_interactions
from utils.google_sheets import export_to_csv

st.set_page_config(page_title="FBA Assistant Autogen", layout="wide")
st.title("🤖 FBA Assistant - Autogen Crew")

st.markdown("Lance une recherche de niches FBA automatiquement à l’aide d’agents LLM intelligents.")

# Formulaire pour lancer un nouveau run
with st.form("run_form"):
    user_input = st.text_input("💬 Que veux-tu rechercher ?", value="Trouve-moi une idée de produit Amazon FBA")
    submitted = st.form_submit_button("🚀 Lancer les agents")
    if submitted and user_input:
        with st.spinner("Les agents collaborent..."):
            result = run_fba_crew(user_input)
        st.success("✅ Recherche terminée !")
        st.text_area("Résultat complet :", value=str(result), height=300)

# Dashboard mémoire
st.subheader("📚 Historique des interactions")
mem = get_last_interactions()
if mem:
    df = pd.DataFrame(mem, columns=["Question", "Réponse"])
    st.dataframe(df, use_container_width=True)

    # Export CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger l'historique en CSV",
        data=csv,
        file_name="historique_fba.csv",
        mime="text/csv"
    )
else:
    st.info("Aucune interaction enregistrée pour le moment.")

# Ajout export Sheets (optionnel)
if st.button("📤 Exporter vers Google Sheets"):
    result = export_to_csv()
    st.success(result if result else "✅ Export vers Google Sheets terminé.")