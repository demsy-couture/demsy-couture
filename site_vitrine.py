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

# Espace Connexion Client dans la Sidebar
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

# --- THÉMATISATION CSS ---
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
    .measure-box {{ border: 1px solid #d4af37; padding: 15px; border-radius: 8px; background-color: {card_bg}; margin-bottom: 15px; }}
    .measure-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; border-bottom: 1px dashed {card_border}; color: {text_main}; }}
    .measure-val {{ background: linear-gradient(90deg, #d4af37, #aa7c11); color: #000000; padding: 2px 10px; border-radius: 15px; font-weight: bold; }}
    div.stButton > button {{ background: linear-gradient(90deg, #d4af37, #aa7c11) !important; color: #000000 !important; font-weight: bold !important; border: none !important; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. ACCUEIL
# ==========================================
if st.session_state.page_actuelle == "ACCUEIL":
    titre_dynamique = config.get("titre_principal", "L'ÉLÉGANCE MASCULINE, REDÉFINIE.")
    st.markdown(f'<div class="hero-container"><div class="hero-title">{titre_dynamique}</div><div class="hero-subtitle">DEMSY COUTURE AU MASCULIN</div></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card-capsule">👤<h4>Mon Profil & Panier</h4><p>Gérez vos mensurations et vos sélections de vêtements de luxe.</p></div>', unsafe_allow_html=True)
        if st.button("Ouvrir mon espace", key="go_profil", use_container_width=True):
            changer_page("MON PROFIL & PANIER"); st.rerun()
    with col2:
        st.markdown('<div class="card-capsule">📦<h4>Suivi Commandes</h4><p>Suivez l\'avancement de vos confections en temps réel dans l\'atelier.</p></div>', unsafe_allow_html=True)
        if st.button("Suivre mes commandes", key="go_commandes", use_container_width=True):
            changer_page("📦 SUIVI DES COMMANDES"); st.rerun()
    with col3:
        st.markdown('<div class="card-capsule">🧥<h4>Galerie Modèles</h4><p>Découvrez nos collections exclusives de boubous et costumes.</p></div>', unsafe_allow_html=True)
        if st.button("Voir la collection", key="go_galerie", use_container_width=True):
            changer_page("COLLECTIONS (GALERIE)"); st.rerun()

# ==========================================
# 2. GALERIE MODÈLES
# ==========================================
elif st.session_state.page_actuelle == "COLLECTIONS (GALERIE)":
    st.markdown("<h1 style='text-align: center; color: #d4af37;'>MODÈLES & CRÉATIONS</h1>", unsafe_allow_html=True)
    
    modeles = donnees.get("modeles", [])
    if modeles:
        cols = st.columns(3)
        for idx, mod in enumerate(modeles):
            with cols[idx % 3]:
                st.markdown("<div class='card-capsule'>", unsafe_allow_html=True)
                if mod["image"].startswith("http"):
                    st.image(mod["image"], use_container_width=True)
                else:
                    st.markdown("<div style='height:180px; background-color:#222; display:flex; align-items:center; justify-content:center; color:#fff; border-radius:5px;'>✨ Modèle d'Élite</div>", unsafe_allow_html=True)
                
                st.markdown(f"<h3 style='color:#d4af37;'>{mod['nom']}</h3>", unsafe_allow_html=True)
                st.write(mod["description"])
                st.markdown(f"<p style='color:#d4af37; font-weight:bold; font-size:18px;'>{int(mod['prix']):,} FCFA</p>".replace(",", " "), unsafe_allow_html=True)
                
                # Système d'ajout ou retrait du panier
                if mod in st.session_state.panier:
                    if st.button(f"🗑️ Retirer du panier", key=f"rm_{mod['id']}", use_container_width=True):
                        st.session_state.panier.remove(mod)
                        st.rerun()
                else:
                    if st.button(f"🛒 Ajouter au panier", key=f"add_{mod['id']}", use_container_width=True):
                        if st.session_state.client_connecte is None:
                            st.warning("Veuillez d'abord entrer votre nom dans l'espace client (à gauche) !")
                        else:
                            st.session_state.panier.append(mod)
                            st.success("Ajouté !")
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Aucun modèle disponible pour le moment.")

# ==========================================
# 3. PROFIL & PANIER CLIENT
# ==========================================
elif st.session_state.page_actuelle == "MON PROFIL & PANIER":
    if st.session_state.client_connecte is None:
        st.warning("Veuillez vous connecter dans l'Espace Client sur la barre latérale gauche pour voir votre profil et votre panier.")
    else:
        nom_c = st.session_state.client_connecte
        st.markdown(f"<h1 style='text-align: center; color: #d4af37;'>ESPACE DE {nom_c}</h1>", unsafe_allow_html=True)
        
        tab_profil, tab_panier = st.tabs(["👤 Mes Informations & Mesures", "🛒 Mon Panier d'Achat"])
        
        with tab_profil:
            client_data = donnees["clients"].get(nom_c, {"telephone": "", "mesures_haut": {}, "mesures_bas": {}})
            st.write(f"**Téléphone enregistré :** {client_data.get('telephone', 'Non renseigné')}")
            
            # Formulaire permettant au client de modifier lui-même son profil
            st.write("### ✏️ Modifier mes mensurations")
            with st.form("modif_mesures_client"):
                nv_tel = st.text_input("Mettre à jour mon téléphone :", value=client_data.get("telephone", ""))
                
                colh, colb = st.columns(2)
                mesures_haut_maj = {}
                mesures_bas_maj = {}
                
                # Listes de mesures de base par défaut si vides
                champs_haut = ["Cou", "Poitrine", "Épaule", "Longueur Manche", "Tour de Bras"]
                champs_bas = ["Taille", "Hanche", "Cuisse", "Longueur Pantalon", "Entrejambe"]
                
                with colh:
                    st.markdown("##### 📏 Haut du corps (en cm)")
                    for m in champs_haut:
                        val_m = client_data.get("mesures_haut", {}).get(m, 0.0)
                        mesures_haut_maj[m] = st.number_input(f"{m} :", value=float(val_m), step=0.5, key=f"cl_h_{m}")
                with colb:
                    st.markdown("##### 📐 Bas du corps (en cm)")
                    for m in champs_bas:
                        val_m = client_data.get("mesures_bas", {}).get(m, 0.0)
                        mesures_bas_maj[m] = st.number_input(f"{m} :", value=float(val_m), step=0.5, key=f"cl_b_{m}")
                
                if st.form_submit_button("Enregistrer mes modifications"):
                    donnees["clients"][nom_c] = {
                        "telephone": nv_tel,
                        "mesures_haut": "%s" % mesures_haut_maj, # Sauvegarde propre
                        "mesures_haut": mesures_haut_maj,
                        "mesures_bas":  mesures_bas_maj
                    }
                    sauvegarder_donnees(donnees)
                    st.success("Profil mis à jour avec succès !")
                    st.rerun()
            
        with tab_panier:
            st.write("### 🛒 Votre panier actuel")
            if st.session_state.panier:
                total_panier = 0
                for idx, item in enumerate(st.session_state.panier):
                    col_p1, col_p2, col_p3 = st.columns([3, 2, 1])
                    with col_p1:
                        st.write(f"**{item['nom']}**")
                    with col_p2:
                        st.write(f"{int(item['prix']):,} FCFA".replace(",", " "))
                        total_panier += int(item['prix'])
                    with col_p3:
                        if st.button("Retirer", key=f"del_pan_{idx}"):
                            st.session_state.panier.remove(item)
                            st.rerun()
                
                st.markdown("---")
                st.markdown(f"### 💰 TOTAL À PAYER : <span style='color:#d4af37;'>{total_panier:,} FCFA</span>".replace(",", " "), unsafe_allow_html=True)
                
                if st.button("🚀 VALIDER LA COMMANDE ET ENVOYER À L'ATELIER", use_container_width=True):
                    # Génération automatique des commandes reçues
                    if "commandes" not in donnees:
                        donnees["commandes"] = {}
                    
                    for item in st.session_state.panier:
                        new_id = f"CMD-{len(donnees['commandes']) + 101}"
                        donnees["commandes"][new_id] = {
                            "client": nom_c,
                            "modele": item["nom"],
                            "prix": int(item["prix"]),
                            "avance": 0,
                            "statut": "En attente",
                            "date_livraison": "À définir avec l'atelier"
                        }
                    
                    sauvegarder_donnees(donnees)
                    st.session_state.panier = [] # Vider le panier
                    st.success("🎉 Commande envoyée avec succès ! Le tailleur vient de la recevoir dans son panneau.")
                    st.rerun()
            else:
                st.info("Votre panier est vide. Visitez l'onglet 'COLLECTIONS' pour ajouter des articles.")

# ==========================================
# 4. SUIVI DE COMMANDES
# ==========================================
elif st.session_state.page_actuelle == "📦 SUIVI DES COMMANDES":
    st.markdown("<h1 style='text-align: center; color: #d4af37;'>📦 SUIVI DE VOS CONFECTIONS</h1>", unsafe_allow_html=True)
    
    # Recherche automatique si connecté, sinon manuelle
    nom_rech = st.session_state.client_connecte if st.session_state.client_connecte else st.text_input("Entrez votre Nom Complet pour le suivi :").strip().upper()
    
    if nom_rech:
        cmds = donnees.get("commandes", {})
        cmds_client = {k: v for k, v in cmds.items() if v.get("client", "").upper() == nom_rech}
        
        if cmds_client:
            for id_cmd, cmd in cmds_client.items():
                statut = cmd.get("statut", "En attente")
                c_statut = "#d4af37" if statut == "En attente" else ("#28a745" if statut == "Prêt" else "#007bff")
                
                st.markdown(f"""
                <div style="border: 1px solid #d4af37; padding: 20px; border-radius: 8px; margin-bottom: 15px; background: rgba(212,175,55,0.02);">
                    <div style="display: flex; justify-content: space-between;">
                        <h4>Commande {id_cmd} - <b>{cmd['modele']}</b></h4>
                        <span style="background:{c_statut}; color:black; padding:3px 15px; font-weight:bold; border-radius:15px;">📌 {statut}</span>
                    </div>
                    <p><b>Prix :</b> {int(cmd['prix']):,} FCFA | <b>Avance :</b> {int(cmd['avance']):,} FCFA</p>
                    <p style="color:#ff4b4b;"><b>Reste à payer :</b> {int(cmd['prix'])-int(cmd['avance']):,} FCFA</p>
                    <small>⏱️ Livraison : {cmd.get('date_livraison', 'Non définie')}</small>
                </div>
                """.replace(",", " "), unsafe_allow_html=True)
        else:
            st.info("Aucune commande enregistrée pour ce nom.")

# ==========================================
# 5. PARAMÈTRES / INTERFACE PRIVÉE DU TAILLEUR (TOTAL CONTROLE)
# ==========================================
elif st.session_state.page_actuelle == "⚙️ PARAMÈTRES":
    st.markdown("<h1 style='color: #d4af37;'>WORKSHOP INTERFACE (PRO)</h1>", unsafe_allow_html=True)
    mdp = st.text_input("Code secret de l'atelier :", type="password")
    
    if mdp == MOT_DE_PASSE_ADMIN:
        st.success("Connexion Master validée. Contrôle total activé.")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📢 Titre d'Accueil", "🧥 Publication de Modèles", "👥 Fiches Mesures Clients", "📦 Validation & Commandes"])
        
        with tab1:
            nv_titre = st.text_input("Titre principal de la vitrine :", value=config.get("titre_principal", "L'ÉLÉGANCE MASCULINE, REDÉFINIE."))
            if st.button("Publier le nouveau titre"):
                donnees["configuration"]["titre_principal"] = nv_titre
                sauvegarder_donnees(donnees); st.success("Mis à jour !"); st.rerun()
                
        with tab2:
            st.write("### 🧥 Publier un nouveau modèle dans la galerie")
            with st.form("form_pub_modele"):
                m_nom = st.text_input("Nom de la création :")
                m_desc = st.text_area("Description du tissu / coupe :")
                m_prix = st.number_input("Prix de vente (FCFA) :", min_value=0, step=5000, value=125000)
                m_img = st.text_input("Lien internet de l'image (Ex: https://...) :", value="")
                if st.form_submit_button("Mettre en vitrine publique"):
                    if m_nom:
                        donnees["modeles"].append({
                            "id": f"mod_{len(donnees['modeles'])+1}",
                            "nom": m_nom, "description": m_desc, "prix": int(m_prix), "image": m_img
                        })
                        sauvegarder_donnees(donnees); st.success("Modèle publié !"); st.rerun()
                        
        with tab3:
            st.write("### 👥 Consultation et édition des fiches clients")
            for c_nom, c_data in list(donnees.get("clients", {}).items()):
                with st.expander(f"👤 CLIENT : {c_nom}"):
                    st.write(f"📞 Contact : {c_data.get('telephone')}")
                    # Le tailleur a une visibilité complète sur les mesures définies
                    st.json(c_data)
                    
        with tab4:
            st.write("### 📦 Commandes Reçues (Panier validés par les clients)")
            cmds_all = donnees.get("commandes", {})
            if cmds_all:
                for cid, cinfo in list(cmds_all.items()):
                    st.markdown(f"**{cid}** - Client : {cinfo['client']} | Modèle : {cinfo['modele']}")
                    nv_statut = st.selectbox(f"Statut {cid}", ["En attente", "Coupe", "Couture", "Finitions", "Prêt"], index=["En attente", "Coupe", "Couture", "Finitions", "Prêt"].index(cinfo.get('statut', 'En attente')), key=f"st_{cid}")
                    nv_avance = st.number_input(f"Avance reçue ({cid}) :", value=int(cinfo.get('avance', 0)), step=5000, key=f"av_{cid}")
                    nv_date = st.text_input(f"Date Livraison ({cid}) :", value=cinfo.get('date_livraison', ''), key=f"dt_{cid}")
                    
                    if st.button(f"Mettre à jour {cid}", key=f"up_{cid}"):
                        donnees["commandes"][cid]["statut"] = nv_statut
                        donnees["commandes"][cid]["avance"] = int(nv_avance)
                        donnees["commandes"][cid]["date_livraison"] = nv_date
                        sauvegarder_donnees(donnees); st.success("Modifié !"); st.rerun()
                    st.markdown("---")
            else:
                st.info("Aucune commande reçue dans le système.")
                
    elif mdp:
        st.error("Code de sécurité incorrect.")