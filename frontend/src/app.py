import streamlit as st
import requests
import json
import time

# URL de votre API Docker (ajustez si votre port hôte est différent)
API_URL = "http://backend:8000/api/articles"

# --- Configuration de la page Streamlit ---
st.set_page_config(
    page_title="Articles TechCrunch AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)

# Initialisation de l'état de la session
if "current_view" not in st.session_state:
    st.session_state.current_view = "list" # 'list' pour la vue des titres, 'article' pour la vue d'un article
    st.session_state.selected_article = None

st.title("🤖 Articles récents TechCrunch AI")
st.markdown("---")

# --- Fonction pour récupérer les articles de l'API ---
@st.cache_data(ttl=600)
def get_articles_from_api():
    try:
        # logging de la requête
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        articles = response.json()
        return articles
    except requests.exceptions.ConnectionError:
        st.error("Impossible de se connecter à l'API. Assurez-vous que le conteneur Docker de l'API est en cours d'exécution sur le port 8000.")
        return []
    except requests.exceptions.Timeout:
        st.error("La requête API a dépassé le délai imparti. Veuillez réessayer.")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Une erreur s'est produite lors de la récupération des articles: {e}")
        return []

# --- Fonction pour afficher la liste des titres ---
def display_article_list():
    if st.button("Actualiser les articles"):
        st.cache_data.clear()
        st.rerun()

    articles = get_articles_from_api()

    if articles:
        st.subheader(f"Derniers articles ({len(articles)} trouvés)")
        for article in articles:
            # Création d'un bouton pour chaque titre
            if st.button(article.get('title', 'Titre inconnu'), use_container_width=True, key=article.get('url')):
                st.session_state.current_view = "article"
                st.session_state.selected_article = article
                st.rerun()
    else:
        st.info("Aucun article n'a été trouvé ou l'API n'a pas renvoyé de données.")

# --- Fonction pour afficher le contenu de l'article sélectionné ---
def display_selected_article():
    # Bouton de retour à la liste
    if st.button("Retour à la liste des articles"):
        st.session_state.current_view = "list"
        st.session_state.selected_article = None
        st.rerun()
        
    article = st.session_state.selected_article
    if article:
        st.title(article.get('title', 'Titre inconnu'))
        st.markdown("---")
        st.write(article.get('content', 'Contenu non disponible'))
    else:
        st.error("Article non trouvé. Retour à la liste.")
        st.session_state.current_view = "list"
        st.session_state.selected_article = None

# --- Logique de routage ---
if st.session_state.current_view == "list":
    display_article_list()
elif st.session_state.current_view == "article":
    display_selected_article()

st.sidebar.markdown("### À propos")
st.sidebar.info(
    "Cette application affiche les titres des articles de la catégorie 'Artificial Intelligence' de TechCrunch, "
    "récupérés via une API Docker."
)