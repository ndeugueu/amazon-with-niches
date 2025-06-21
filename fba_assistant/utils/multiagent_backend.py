import os
import re
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from .memory import save_interaction


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm_conf = {
    "model": "gpt-4",
    "api_key": OPENAI_API_KEY
}

product_hunter = AssistantAgent(
    name="ProductHunterAgent",
    llm_config=llm_conf,
    system_message="""Vous êtes un expert Amazon FBA.

Votre mission est de trouver des idées de produits rentables à vendre sur Amazon selon les critères suivants :

- Prix entre 20 € et 70 €
- Poids < 1 kg
- Moins de 1000 avis sur les concurrents
- Non électronique
- Améliorable : packaging, accessoire, différenciation

🧾 Répondez uniquement au format tableau, une ligne par produit :

Produit | Prix | Poids | Amélioration possible | Lien produit

Exemple :
Presse-ail ergonomique | 22 € | 300 g | Packaging premium et ajout de brosse de nettoyage | https://www.amazon.fr/dp/B07XYZ
Brosse pour animaux 2-en-1 | 29 € | 450 g | Ajouter recharge + meilleure poignée | https://www.amazon.fr/dp/B08ABC
"""
)

sourcing_agent = AssistantAgent(
    name="SourcingAgent",
    llm_config=llm_conf,
    system_message="Tu es expert sourcing Alibaba. Trouve fournisseurs, MOQ et estimations de coût pour les produits proposés."
)

listing_agent = AssistantAgent(
    name="ListingAgent",
    llm_config=llm_conf,
    system_message="Tu es expert SEO Amazon. Génére des fiches produit optimisées (titre, bullet points, description)."
)

launch_agent = AssistantAgent(
    name="LaunchPlannerAgent",
    llm_config=llm_conf,
    system_message="Tu es expert lancement FBA. Donne stratégie de lancement, avis, promos, campagnes PPC, visuels."
)

user = UserProxyAgent(
    name="Utilisateur",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False}
)

def format_response_as_table(response_text):
    lines = str(response_text).split("\n")
    table_data = []
    for line in lines:
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 5:
                table_data.append(parts[:5])
        else:
            match = re.match(r"(.*?)[,|-]+(\d+ ?€)[,|-]+(\d+ ?g)[,|-]+(.*?)[,|-]+(https?://\S+)", line)
            if match:
                table_data.append([
                    match.group(1),
                    match.group(2),
                    match.group(3),
                    match.group(4),
                    match.group(5),
                ])
    return table_data

def run_fba_crew(user_input):
    groupchat = GroupChat(
        agents=[user, product_hunter, sourcing_agent, listing_agent, launch_agent],
        messages=[],
        max_round=4
    )
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_conf)
    result = user.initiate_chat(manager, message=user_input)
    save_interaction(user_input, str(result))
    return result