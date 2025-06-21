import streamlit as st
import os
from fba_assistant.utils.multiagent_backend import run_fba_crew
from fba_assistant.utils.memory import get_last_interactions
from fba_assistant.utils.google_sheets import export_to_csv

# 🔐 Lecture sécurisée des secrets Streamlit
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.error("⚠️ Clé OpenAI absente de .streamlit/secrets.toml")
    st.stop()

st.set_page_config(page_title="FBA Assistant - Autogen Crew", layout="wide")

st.title("🤖 FBA Assistant - Multi-agent LLM Crew")
st.markdown("Trouvez automatiquement des niches Amazon FBA rentables grâce à une équipe d’agents intelligents.")

# Saisie utilisateur
user_input = st.text_input("🔍 Quelle niche veux-tu explorer ?", placeholder="ex : Trouve-moi un produit compact entre 20€ et 70€")
launch_button = st.button("🚀 Lancer l’exploration")

# Résultats
if launch_button and user_input:
    with st.spinner("Analyse en cours..."):
        result = run_fba_crew(user_input)
        st.success("✅ Analyse terminée")

        # 🔽 Extraction des lignes par produit (si résultat structuré)
        lines = str(result).split("\n")
        clean_lines = [line.strip("-• ") for line in lines if line.strip()]
        data = {"Propositions": clean_lines}
        df = pd.DataFrame(data)
        st.dataframe(df)

# Historique
st.subheader("🧠 Historique des échanges")
for q, r in get_last_interactions():
    st.markdown(f"**🗨️ Question :** {q}")
    st.markdown(f"**🤖 Réponse :** {r}")
    st.markdown("---")

# Export CSV / Sheets
st.subheader("📤 Export des résultats")
col1, col2 = st.columns(2)
with col1:
    if st.button("📁 Export CSV"):
        data = get_last_interactions()
        df = pd.DataFrame(data, columns=["Question", "Réponse"])
        df.to_csv("export_niches.csv", index=False)
        st.success("✅ Exporté sous export_niches.csv")

with col2:
    if st.button("📤 Export Google Sheets"):
        status = export_to_csv()
        st.info(status)