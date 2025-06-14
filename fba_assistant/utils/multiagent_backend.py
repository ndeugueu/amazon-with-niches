import os
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from utils.memory import save_interaction

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm_conf = {
    "model": "gpt-4",
    "api_key": OPENAI_API_KEY
}

product_hunter = AssistantAgent(
    name="ProductHunterAgent",
    llm_config=llm_conf,
    system_message="""Tu es un expert en recherche de produits Amazon FBA. Objectif :
- Prix de vente entre 20€ et 70€
- Moins de 1 kg
- Moins de 1000 avis
- Demande 500+/mois
- Facile à améliorer
- Sans marque dominante

Propose des idées concrètes et analysées."""
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