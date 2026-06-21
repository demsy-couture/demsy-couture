import streamlit as st
import json
import os
import base64

# Configuration de la page
st.set_page_config(
    page_title="DEMSY COUTURE AU MASCULIN",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

FICHIER_DONNEES = "donnees_atelier.json"
MOT_DE_PASSE_ADMIN = "16129489f"

def charger_donnees():
    if os.path.exists(FICHIER_DONNEES):
        with open(FICHIER_DONNEES, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                pass
    return {"configuration": {}, "modeles": [], "clients": {}, "commandes": {}}

def sauvegarder_donnees(donnees):
    with open(FICHIER_DONNEES, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)

donnees = charger_donnees()
config = donnees.get("configuration", {})

# --- INITIALISATION DES SESSIONS ---
if "page_actuelle" not in st.session_state:
    st.session_state.page_actuelle = "ACCUEIL"
if "client_connecte" not in st.session_state:
    st.session_state.client_connecte = None
if "panier" not in st.session_state:
    st.session_state.panier = []

# --- NAVIGATION SIDEBAR ---
st.sidebar.markdown('<div style="color: #d4af37; font-size: 22px; font-weight: bold; text-align: center; margin-bottom: 5px; letter-spacing: 1px; font-family: \'Playfair Display\', serif;">DEMSY<br><span style="font-size:12px; color:#aaa;">COUTURE AU MASCULIN</span></div>', unsafe_allow_html=True)
st.sidebar.write("---")

st.sidebar.write("### 🔑 Espace Client")
if st.session_state.client_connecte is None:
    nom_saisi = st.sidebar.text_input("Votre Nom Complet :", key="connexion_nom").strip().upper()
    tel_saisi = st.sidebar.text_input("Votre Téléphone :", key="connexion_tel").strip()
    if st.sidebar.button("Se connecter / S'inscrire"):
        if nom_saisi:
            st.session_state.client_connecte = nom_saisi
            if nom_saisi not in donnees["clients"]:
                donnees["clients"][nom_saisi] = {"telephone": tel_saisi, "mesures_haut": {}, "mesures_bas": {}}
                sauvegarder_donnees(donnees)
            st.rerun()
else:
    st.sidebar.success(f"Connecté : {st.session_state.client_connecte}")
    if st.sidebar.button("❌ Se déconnecter"):
        st.session_state.client_connecte = None
        st.session_state.panier = []
        st.rerun()

st.sidebar.write("---")
theme_choisi = st.sidebar.selectbox("🎨 Style visuel :", ["Sombre & Or", "Clair & Prestige"])
st.sidebar.write("---")

def changer_page(nom_page):
    st.session_state.page_actuelle = nom_page

liste_pages = ["ACCUEIL", "COLLECTIONS (GALERIE)", "MON PROFIL & PANIER", "📦 SUIVI DES COMMANDES", "⚙️ PARAMÈTRES"]
index_page = liste_pages.index(st.session_state.page_actuelle) if st.session_state.page_actuelle in liste_pages else 0

menu = st.sidebar.radio(
    "Navigation :", 
    liste_pages, 
    index=index_page, 
    key="navigation_radio",
    on_change=lambda: changer_page(st.session_state.navigation_radio)
)

if theme_choisi == "Sombre & Or":
    bg_app, text_main, bg_sidebar = "#0d0d0d", "#ffffff", "#1a1a1a"
    card_bg, card_border, card_text_desc = "linear-gradient(135deg, #1a1a1a 0%, #111111 100%)", "#333333", "#aaaaaa"
    hero_overlay, tab_text_color = "rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.8)", "#ffffff"
else:
    bg_app, text_main, bg_sidebar = "#fcfaf2", "#1a1a1a", "#f4ebd0"
    card_bg, card_border, card_text_desc = "#ffffff", "#e2d1b3", "#4a4a4a"
    hero_overlay, tab_text_color = "rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.4)", "#1a1a1a"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_app}; color: {text_main}; }}
    [data-testid="stSidebar"] {{ background-color: {bg_sidebar}; border-right: 1px solid #d4af37; }}
    h1, h2, h3, h4, .stMarkdown p {{ font-family: 'Playfair Display', serif; }}
    button[data-baseweb="tab"] p {{ color: {tab_text_color} !important; font-weight: bold !important; }}
    .hero-container {{
        background: linear-gradient({hero_overlay}), url('https://images.unsplash.com/photo-1593032465175-481ac7f401a0?q=80&w=1200&auto=format&fit=crop');
        background-size: cover; background-position: center; padding: 80px 50px; border-radius: 10px; text-align: center; border: 1px solid #d4af37; margin-bottom: 40px;
    }}
    .hero-title {{ color: #d4af37; font-size: 40px; font-weight: 900; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 10px; }}
    .card-capsule {{ background: {card_bg}; border: 1px solid {card_border}; border-radius: 8px; padding: 20px; text-align: center; margin-bottom: 15px; }}
    div.stButton > button {{ background: linear-gradient(90deg, #d4af37, #aa7c11) !important; color: #000000 !important; font-weight: bold !important; border: none !important; }}
    </style>
""", unsafe_allow_html=True)

# 1. ACCUEIL
if st.session_state.page_actuelle == "ACCUEIL":
    titre_dynamique = config.get("titre_principal", "L'ÉLÉGANCE MASCULINE, REDÉFINIE.")
    st.markdown(f'<div class="hero-container"><div class="hero-title">{titre_dynamique}</div><div class="hero-subtitle">DEMSY COUTURE AU MASCULIN</div></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card-capsule">👤<h4>Mon Profil & Panier</h4><p>Gérez vos mensurations et vos sélections.</p></div>', unsafe_allow_html=True)
        if st.button("Ouvrir mon espace", key="go_profil", use_container_width=True):
            changer_page("MON PROFIL & PANIER")
            st.rerun()
    with col2:
        st.markdown('<div class="card-capsule">📦<h4>Suivi Commandes</h4><p>Suivez vos confections en temps réel.</p></div>', unsafe_allow_html=True)
        if st.button("Suivre mes commandes", key="go_commandes", use_container_width=True):
            changer_page("📦 SUIVI DES COMMANDES")
            st.rerun()
    with col3:
        st.markdown('<div class="card-capsule">🧥<h4>Galerie Modèles</h4><p>Découvrez nos collections exclusives.</p></div>', unsafe_allow_html=True)
        if st.button("Voir la collection", key="go_galerie", use_container_width=True):
            changer_page("COLLECTIONS (GALERIE)")
            st.rerun()

# 2. GALERIE
elif st.session_state.page_actuelle == "COLLECTIONS (GALERIE)":
    st.markdown("<h1 style='text-align: center; color: #d4af37;'>MODÈLES & CRÉATIONS</h1>", unsafe_allow_html=True)
    modeles = donnees.get("modeles", [])
    if modeles:
        cols = st.columns(3)
        for idx, mod in enumerate(modeles):
            with cols[idx % 3]:
                st.markdown("<div class='card-capsule'>", unsafe_allow_html=True)
                if mod["image"].startswith("data:image") or mod["image"].startswith("http"):
                    st.image(mod["image"], use_container_width=True)
                st.markdown(f"<h3 style='color:#d4af37;'>{mod['nom']}</h3>", unsafe_allow_html=True)
                st.write(mod["description"])
                st.markdown(f"<p style='color:#d4af37; font-weight:bold; font-size:18px;'>{int(mod['prix'])} FCFA</p>", unsafe_allow_html=True)
                
                if mod in st.session_state.panier:
                    if st.button(f"🗑️ Retirer", key=f"rm_{mod['id']}", use_container_width=True):
                        st.session_state.panier.remove(mod)
                        st.rerun()
                else:
                    if st.button(f"🛒 Ajouter au panier", key=f"add_{mod['id']}", use_container_width=True):
                        if st.session_state.client_connecte is None:
                            st.warning("Connectez-vous à gauche d'abord !")
                        else:
                            st.session_state.panier.append(mod)
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Aucun modèle dans la vitrine.")

# 3. PROFIL & PANIER
elif st.session_state.page_actuelle == "MON PROFIL & PANIER":
    st.write("Espace Profil et Panier")

# 4. SUIVI COMMANDES
elif st.session_state.page_actuelle == "📦 SUIVI DES COMMANDES":
    st.write("Suivi des commandes")

# 5. PARAMÈTRES (ADMIN)
elif st.session_state.page_actuelle == "⚙️ PARAMÈTRES":
    st.markdown("<h1 style='color: #d4af37;'>WORKSHOP INTERFACE (PRO)</h1>", unsafe_allow_html=True)
    mdp = st.text_input("Code secret de l'atelier :", type="password")
    
    if mdp == MOT_DE_PASSE_ADMIN:
        tab1, tab2, tab3 = st.tabs(["🧥 Ajouter un modèle", "🗑️ Gérer / Supprimer", "👥 Clients & Commandes"])
        
        with tab1:
            with st.form("form_pub_modele"):
                m_nom = st.text_input("Nom de la création :")
                m_desc = st.text_area("Description :")
                m_prix = st.number_input("Prix (FCFA) :", min_value=0, step=5000)
                m_file = st.file_uploader("Charger la photo depuis votre ordinateur :", type=["png", "jpg", "jpeg"])
                
                if st.form_submit_button("Mettre en vitrine"):
                    if m_nom and m_file:
                        bytes_data = m_file.getvalue()
                        b64_img = base64.b64encode(bytes_data).decode("utf-8")
                        ext = m_file.name.split(".")[-1]
                        final_img = f"data:image/{ext};base64,{b64_img}"
                        
                        donnees["modeles"].append({
                            "id": f"mod_{len(donnees['modeles'])+1}",
                            "nom": m_nom, "description": m_desc, "prix": int(m_prix), "image": final_img
                        })
                        sauvegarder_donnees(donnees)
                        st.success("Publié !")
                        st.rerun()

        with tab2:
            st.write("### 🗑️ Supprimer des modèles de la vitrine")
            modeles = donnees.get("modeles", [])
            if modeles:
                for idx, mod in enumerate(modeles):
                    col_m1, col_m2 = st.columns([4, 1])
                    with col_m1:
                        st.write(f"👔 **{mod['nom']}** — {mod['prix']} FCFA")
                    with col_m2:
                        if st.button("❌ Supprimer", key=f"del_admin_{mod['id']}"):
                            donnees["modeles"].pop(idx)
                            sauvegarder_donnees(donnees)
                            st.success(f"{mod['nom']} supprimé !")
                            st.rerun()
            else:
                st.info("Aucun modèle enregistré dans le fichier JSON.")
