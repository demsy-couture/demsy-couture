import streamlit as st
import json
import os

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
            return json.load(f)
    return {"configuration": {}, "modeles": [], "clients": {}, "commandes": {}}

def sauvegarder_donnees(donnees):
    with open(FICHIER_DONNEES, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)

donnees = charger_donnees()
config = donnees.get("configuration", {})

# --- INITIALISATION DES PAGES DANS LA SESSION ---
if "page_actuelle" not in st.session_state:
    st.session_state.page_actuelle = "ACCUEIL"

# --- NAVIGATION SIDEBAR ---
st.sidebar.markdown('<div style="color: #d4af37; font-size: 22px; font-weight: bold; text-align: center; margin-bottom: 5px; letter-spacing: 1px; font-family: \'Playfair Display\', serif;">DEMSY<br><span style="font-size:12px; color:#aaa;">COUTURE AU MASCULIN</span></div>', unsafe_allow_html=True)
st.sidebar.write("---")

theme_choisi = st.sidebar.selectbox("🎨 Style visuel :", ["Sombre & Or", "Clair & Prestige"])
st.sidebar.write("---")

def changer_page(nom_page):
    st.session_state.page_actuelle = nom_page

liste_pages = ["ACCUEIL", "COLLECTIONS (GALERIE)", "MON PROFIL & MESURES", "📦 SUIVI DES COMMANDES", "⚙️ PARAMÈTRES"]
index_page = liste_pages.index(st.session_state.page_actuelle) if st.session_state.page_actuelle in liste_pages else 0

menu = st.sidebar.radio(
    "Navigation :", 
    liste_pages, 
    index=index_page, 
    key="navigation_radio",
    on_change=lambda: changer_page(st.session_state.navigation_radio)
)

# --- INJECTION DU CSS DYNAMIQUE SELON LE THÈME ---
if theme_choisi == "Sombre & Or":
    bg_app = "#0d0d0d"
    text_main = "#ffffff"
    bg_sidebar = "#1a1a1a"
    card_bg = "linear-gradient(135deg, #1a1a1a 0%, #111111 100%)"
    card_border = "#333333"
    card_text_desc = "#aaaaaa"
    hero_overlay = "rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.8)"
    tab_text_color = "#ffffff"  # Texte blanc sur fond sombre
else:
    bg_app = "#fcfaf2"
    text_main = "#1a1a1a"
    bg_sidebar = "#f4ebd0"
    card_bg = "#ffffff"
    card_border = "#e2d1b3"
    card_text_desc = "#4a4a4a"
    hero_overlay = "rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.4)"
    tab_text_color = "#1a1a1a"  # Texte noir sur fond clair

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_app}; color: {text_main}; }}
    [data-testid="stSidebar"] {{ background-color: {bg_sidebar}; border-right: 1px solid #d4af37; }}
    h1, h2, h3, h4, .stMarkdown p {{ font-family: 'Playfair Display', serif; }}
    
    /* Correction de la visibilité du texte dans les Onglets (Tabs) */
    button[data-baseweb="tab"] p {{
        color: {tab_text_color} !important;
        font-weight: bold !important;
    }}
    
    .hero-container {{
        background: linear-gradient({hero_overlay}), 
                    url('https://images.unsplash.com/photo-1593032465175-481ac7f401a0?q=80&w=1200&auto=format&fit=crop');
        background-size: cover; background-position: center; padding: 100px 50px; border-radius: 10px; text-align: center; border: 1px solid #d4af37; margin-bottom: 40px;
    }}
    .hero-title {{ color: #d4af37; font-size: 45px; font-weight: 900; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }}
    .hero-subtitle {{ color: {text_main}; font-size: 18px; letter-spacing: 2px; margin-bottom: 30px; text-shadow: 1px 1px 3px rgba(0,0,0,0.3); }}
    
    .card-capsule {{ background: {card_bg}; border: 1px solid {card_border}; border-radius: 8px; padding: 25px; text-align: center; transition: 0.3s; height: 100%; margin-bottom: 15px; }}
    .card-capsule:hover {{ border-color: #d4af37; transform: translateY(-5px); box-shadow: 0px 4px 20px rgba(212, 175, 55, 0.2); }}
    .card-icon {{ font-size: 35px; margin-bottom: 10px; }}
    .card-title {{ color: {text_main}; font-size: 18px; font-weight: bold; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 1px; }}
    .card-desc {{ color: {card_text_desc}; font-size: 13px; line-height: 1.6; margin-bottom: 15px; min-height: 60px; }}
    
    .measure-box {{ border: 1px solid #d4af37; padding: 15px; border-radius: 8px; background-color: {card_bg}; margin-bottom: 15px; }}
    .measure-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; border-bottom: 1px dashed {card_border}; padding-bottom: 4px; color: {text_main}; }}
    .measure-val {{ background: linear-gradient(90deg, #d4af37, #aa7c11); color: #000000; padding: 2px 10px; border-radius: 15px; font-weight: bold; font-size: 14px; }}
    
    div.stButton > button {{ background: linear-gradient(90deg, #d4af37, #aa7c11) !important; color: #000000 !important; font-weight: bold !important; border: none !important; }}
    div.stButton > button:hover {{ background: #000000 !important; color: #ffffff !important; box-shadow: 0px 0px 10px rgba(212,175,55,0.5); }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. ACCUEIL
# ==========================================
if st.session_state.page_actuelle == "ACCUEIL":
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">L'ÉLÉGANCE MASCULINE, REDÉFINIE.</div>
            <div class="hero-subtitle">DEMSY COUTURE AU MASCULIN</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card-capsule"><div class="card-icon">👤</div><div class="card-title">Mon Profil</div><div class="card-desc">Accédez à vos fiches de mesures exclusives et gérez vos mensurations pour vos commandes.</div></div>', unsafe_allow_html=True)
        if st.button("Ouvrir mon profil", key="go_profil", use_container_width=True):
            changer_page("MON PROFIL & MESURES")
            st.rerun()
            
    with col2:
        st.markdown('<div class="card-capsule"><div class="card-icon">📦</div><div class="card-title">Suivi Commandes</div><div class="card-desc">Suivez l\'avancement en temps réel de la confection de vos vêtements de luxe en atelier.</div></div>', unsafe_allow_html=True)
        if st.button("Suivre mes commandes", key="go_commandes", use_container_width=True):
            changer_page("📦 SUIVI DES COMMANDES")
            st.rerun()
            
    with col3:
        st.markdown('<div class="card-capsule"><div class="card-icon">🧥</div><div class="card-title">Galerie Modèles</div><div class="card-desc">Explorez notre sélection de costumes, boubous prestigieux et coupes haut de gamme.</div></div>', unsafe_allow_html=True)
        if st.button("Voir la collection", key="go_galerie", use_container_width=True):
            changer_page("COLLECTIONS (GALERIE)")
            st.rerun()

# ==========================================
# 2. GALERIE MODÈLES
# ==========================================
elif st.session_state.page_actuelle == "COLLECTIONS (GALERIE)":
    if st.button("⬅️ Retour à l'accueil", key="back_galerie"):
        changer_page("ACCUEIL")
        st.rerun()
        
    st.markdown("<h1 style='text-align: center; color: #d4af37;'>MODÈLES & CRÉATIONS</h1>", unsafe_allow_html=True)
    
    modeles = donnees.get("modeles", [])
    if modeles:
        cols = st.columns(3)
        for idx, mod in enumerate(modeles):
            with cols[idx % 3]:
                st.markdown("<div class='card-capsule'>", unsafe_allow_html=True)
                if os.path.exists(mod["image"]):
                    st.image(mod["image"], use_container_width=True)
                else:
                    st.markdown("<div style='height:200px; background-color:#222; display:flex; align-items:center; justify-content:center; border-radius:5px; color:#fff;'>📸 Image bientôt disponible</div>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='color:#d4af37; margin-top:10px;'>{mod['nom']}</h4>", unsafe_allow_html=True)
                st.write(mod["description"])
                st.markdown(f"<p style='color:#d4af37; font-weight:bold;'>{int(mod['prix']):,} FCFA</p>".replace(",", " "), unsafe_allow_html=True)
                if st.button(f"Commander {mod['nom']}", key=f"btn_{mod['id']}", use_container_width=True):
                    st.success(f"Modèle sélectionné ! Contactez l'atelier de Cocody.")
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Aucun modèle enregistré pour le moment.")

# ==========================================
# 3. PROFIL & MESURES
# ==========================================
elif st.session_state.page_actuelle == "MON PROFIL & MESURES":
    if st.button("⬅️ Retour à l'accueil", key="back_profil"):
        changer_page("ACCUEIL")
        st.rerun()
        
    st.markdown("<h1 style='text-align: center; color: #d4af37;'>COMPTE CLIENT & MESURES</h1>", unsafe_allow_html=True)
    nom_recherche = st.text_input("Entrez votre Nom Complet :").strip().upper()
    
    if nom_recherche in donnees["clients"]:
        client = donnees["clients"][nom_recherche]
        st.markdown(f"<h2 style='text-align:center; color:#d4af37;'>{nom_recherche}</h2>", unsafe_allow_html=True)
        
        col_haut, col_bas = st.columns(2)
        with col_haut:
            st.markdown("<div class='measure-box'><h4 style='color:#d4af37; text-align:center;'>VOS MESURES - HAUT</h4>", unsafe_allow_html=True)
            for m, val in client.get("mesures_haut", {}).items():
                st.markdown(f"<div class='measure-row'><span>📏 {m}</span><span class='measure-val'>{val} cm</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_bas:
            st.markdown("<div class='measure-box'><h4 style='color:#d4af37; text-align:center;'>VOS MESURES - BAS</h4>", unsafe_allow_html=True)
            for m, val in client.get("mesures_bas", {}).items():
                st.markdown(f"<div class='measure-row'><span>📐 {m}</span><span class='measure-val'>{val} cm</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    elif nom_recherche:
        st.error("Client introuvable.")

# ==========================================
# 4. SUIVI DES COMMANDES DYNAMIQUE
# ==========================================
elif st.session_state.page_actuelle == "📦 SUIVI DES COMMANDES":
    if st.button("⬅️ Retour à l'accueil", key="back_suivi"):
        changer_page("ACCUEIL")
        st.rerun()
        
    st.markdown("<h1 style='text-align: center; color: #d4af37;'>📦 SUIVI DE VOS COMMANDES</h1>", unsafe_allow_html=True)
    st.write("Saisissez votre nom pour voir l'évolution de vos confections dans notre atelier de Cocody.")
    
    nom_client = st.text_input("Entrez votre Nom Complet (ex: SISSOKO) :").strip().upper()
    
    if nom_client:
        commandes_existantes = donnees.get("commandes", {})
        commandes_client = {k: v for k, v in commandes_existantes.items() if v.get("client", "").upper() == nom_client}
        
        if commandes_client:
            for id_cmd, cmd in commandes_client.items():
                statut = cmd.get("statut", "En attente")
                
                couleur_statut = "#d4af37"
                if statut == "Prêt": couleur_statut = "#28a745"
                elif statut in ["Coupe", "Couture"]: couleur_statut = "#007bff"
                
                st.markdown(f"""
                <div style="border: 1px solid #d4af37; padding: 20px; border-radius: 8px; margin-bottom: 20px; background-color: rgba(212,175,55,0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="color: {text_main};">Commande N° {id_cmd}</h3>
                        <span style="background-color: {couleur_statut}; color: black; padding: 5px 15px; font-weight: bold; border-radius: 20px;">
                            📌 Statut : {statut}
                        </span>
                    </div>
                    <hr style="border-color: #333;">
                    <p style="color: {text_main};"><b>Modèle :</b> {cmd.get('modele', 'Non spécifié')}</p>
                    <p style="color: {text_main};"><b>Prix Total :</b> {int(cmd.get('prix', 0)):,} FCFA</p>
                    <p style="color: {text_main};"><b>Avance versée :</b> {int(cmd.get('avance', 0)):,} FCFA</p>
                    <p style="color: {text_main};"><b>Reste à payer :</b> <span style="color: #ff4b4b; font-weight:bold;">{int(cmd.get('prix', 0)) - int(cmd.get('avance', 0)):,} FCFA</span></p>
                    <p style="font-size: 13px; color: #888;">⏱️ Date limite de livraison : {cmd.get('date_livraison', 'Non définie')}</p>
                </div>
                """.replace(",", " "), unsafe_allow_html=True)
        else:
            st.warning(f"Aucune commande en cours trouvée au nom de '{nom_client}'.")

# ==========================================
# 5. ZONE PARAMÈTRES (ADMIN) - ENTIÈREMENT RESTAURÉE
# ==========================================
elif st.session_state.page_actuelle == "⚙️ PARAMÈTRES":
    if st.button("⬅️ Retour à l'accueil", key="back_parametres"):
        changer_page("ACCUEIL")
        st.rerun()
        
    st.markdown("<h1 style='color: #d4af37;'>PANNEAU DE CONFIGURATION</h1>", unsafe_allow_html=True)
    mdp = st.text_input("Entrez le code de sécurité :", type="password")
    
    if mdp == MOT_DE_PASSE_ADMIN:
        st.success("Accès autorisé.")
        
        # RESTAURATION DE TOUTES LES FONCTIONNALITÉS COMPLÈTES DES ONGLETS
        tab1, tab2, tab3, tab4 = st.tabs(["📢 Général", "🧥 Ajouter un Modèle", "👥 Fiches Mesures", "📦 Gérer Commandes"])
        
        # ONGLET 1 : TEXTE GÉNÉRAL
        with tab1:
            st.write("### 📢 Modifier le titre principal")
            nv_titre = st.text_input("Grand titre d'accueil :", value=config.get("titre_principal", "L'ÉLÉGANCE MASCULINE, REDÉFINIE."))
            if st.button("Mettre à jour l'accueil"):
                donnees["configuration"]["titre_principal"] = nv_titre
                sauvegarder_donnees(donnees)
                st.success("Textes modifiés !")
                st.rerun()
                
        # ONGLET 2 : AJOUT DE MODÈLES À LA GALERIE
        with tab2:
            st.write("### 🧥 Ajouter un vêtement dans la collection")
            with st.form("ajout_modele"):
                m_nom = st.text_input("Nom du vêtement :")
                m_desc = st.text_area("Description :")
                m_prix = st.text_input("Prix (ex: 150000) :")
                m_img = st.text_input("Lien de l'image :", value="images/")
                if st.form_submit_button("Publier le modèle"):
                    if m_nom and m_prix:
                        donnees["modeles"].append({
                            "id": f"mod_{len(donnees['modeles'])+1}", 
                            "nom": m_nom, "description": m_desc, 
                            "prix": m_prix, "image": m_img
                        })
                        sauvegarder_donnees(donnees)
                        st.success("Modèle ajouté sur la galerie !")
                        st.rerun()
                        
        # ONGLET 3 : GESTION DES FICHES CLIENTS ET MESURES
        with tab3:
            st.write("### 👥 Toutes les fiches Mesures de l'atelier")
            for c_nom, c_data in list(donnees.get("clients", {}).items()):
                with st.expander(f"👤 {c_nom}"):
                    donnees["clients"][c_nom]["telephone"] = st.text_input(f"Tel - {c_nom}", value=c_data.get("telephone", ""), key=f"t_{c_nom}")
                    for cat in ["mesures_haut", "mesures_bas"]:
                        st.write(f"**{cat.upper()}**")
                        for m, val in c_data.get(cat, {}).items():
                            donnees["clients"][c_nom][cat][m] = st.number_input(f"{c_nom} - {m}", value=int(val), key=f"{c_nom}_{m}_adm")
                    if st.button(f"Sauvegarder {c_nom}", key=f"s_{c_nom}"):
                        sauvegarder_donnees(donnees)
                        st.success(f"Fiche de {c_nom} enregistrée !")
                        st.rerun()
                        
        # ONGLET 4 : SUIVI DES COMMANDES
        with tab4:
            st.write("### 🛠️ Enregistrer ou Modifier une commande client")
            with st.form("ajout_commande"):
                c_id = st.text_input("Numéro unique de commande (ex: CMD-101) :")
                c_nom = st.text_input("Nom du client :").strip().upper()
                c_mod = st.text_input("Modèle commandé :")
                c_prix = st.number_input("Prix Total (FCFA) :", min_value=0, step=5000)
                c_avance = st.number_input("Avance payée (FCFA) :", min_value=0, step=5000)
                c_statut = st.selectbox("Statut de la confection :", ["En attente", "Coupe", "Couture", "Finitions", "Prêt"])
                c_date = st.text_input("Date prévue de livraison :")
                
                if st.form_submit_button("Sauvegarder la commande"):
                    if c_id and c_nom:
                        if "commandes" not in donnees: donnees["commandes"] = {}
                        donnees["commandes"][c_id] = {
                            "client": c_nom, "modele": c_mod, "prix": c_prix,
                            "avance": c_avance, "statut": c_statut, "date_livraison": c_date
                        }
                        sauvegarder_donnees(donnees)
                        st.success("Commande mise à jour !")
                        st.rerun()
            
            st.write("### Liste actuelle des commandes")
            st.json(donnees.get("commandes", {}))
    elif mdp:
        st.error("Mot de passe incorrect.")