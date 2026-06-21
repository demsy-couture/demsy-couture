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
                contenu = f.read().strip()
                if contenu:
                    return json.loads(contenu)
            except Exception as e:
                st.error(f"Erreur de lecture de la base de données : {e}")
    return {"configuration": {}, "modeles": [], "clients": {}, "commandes": {}}

def sauvegarder_donnees(donnees):
    with open(FICHIER_DONNEES, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)

donnees = charger_donnees()
config = donnees.get("configuration", {})

# Liste officielle des pages
liste_pages = ["ACCUEIL", "COLLECTIONS (GALERIE)", "MON PROFIL & PANIER", "📦 SUIVI DES COMMANDES", "⚙️ PARAMÈTRES"]

# --- FONCTIONS DE NAVIGATION (CALLBACKS) ---
def changer_page(nouvelle_page):
    st.session_state.page_actuelle = nouvelle_page
    st.session_state.nav_radio = nouvelle_page

def connexion_client(nom, tel):
    nom_clean = nom.strip().upper()
    if nom_clean:
        st.session_state.client_connecte = nom_clean
        if nom_clean not in donnees["clients"]:
            donnees["clients"][nom_clean] = {"telephone": tel, "mesures_haut": {}, "mesures_bas": {}}
            sauvegarder_donnees(donnees)
        st.session_state.page_actuelle = "ACCUEIL"
        st.session_state.nav_radio = "ACCUEIL"

def deconnexion_client():
    st.session_state.client_connecte = None
    st.session_state.panier = []
    st.session_state.page_actuelle = "ACCUEIL"
    st.session_state.nav_radio = "ACCUEIL"

# --- INITIALISATION DES SESSIONS ---
if "page_actuelle" not in st.session_state:
    st.session_state.page_actuelle = "ACCUEIL"
if "client_connecte" not in st.session_state:
    st.session_state.client_connecte = None
if "panier" not in st.session_state:
    st.session_state.panier = []
if "admin_authentifie" not in st.session_state:
    st.session_state.admin_authentifie = False

# --- NAVIGATION SIDEBAR ---
st.sidebar.markdown('<div style="color: #d4af37; font-size: 22px; font-weight: bold; text-align: center; margin-bottom: 5px; letter-spacing: 1px; font-family: \'Playfair Display\', serif;">DEMSY<br><span style="font-size:12px; color:#aaa;">COUTURE AU MASCULIN</span></div>', unsafe_allow_html=True)
st.sidebar.write("---")

st.sidebar.write("### 🔑 Espace Client")
if st.session_state.client_connecte is None:
    nom_saisi = st.sidebar.text_input("Votre Nom Complet :", value="", key="connexion_nom")
    tel_saisi = st.sidebar.text_input("Votre Téléphone :", value="", key="connexion_tel").strip()
    st.sidebar.button("Se connecter / S'inscrire", on_click=connexion_client, args=(nom_saisi, tel_saisi))
else:
    st.sidebar.success(f"Connecté : {st.session_state.client_connecte}")
    st.sidebar.button("❌ Se déconnecter", on_click=deconnexion_client)

st.sidebar.write("---")
theme_choisi = st.sidebar.selectbox("🎨 Style visuel :", ["Sombre & Or", "Clair & Prestige"])
st.sidebar.write("---")

# Gestion de l'index du menu radio basé sur la session globale
if st.session_state.page_actuelle in liste_pages:
    index_page = liste_pages.index(st.session_state.page_actuelle)
else:
    index_page = 0

menu = st.sidebar.radio(
    "Navigation :", 
    liste_pages, 
    index=index_page,
    key="nav_radio"
)

if menu != st.session_state.page_actuelle:
    st.session_state.page_actuelle = menu

# --- THEMATISATION DES COULEURS ---
if theme_choisi == "Sombre & Or":
    bg_app, text_main, bg_sidebar = "#0d0d0d", "#ffffff", "#1a1a1a"
    card_bg, card_border = "linear-gradient(135deg, #1a1a1a 0%, #111111 100%)", "#333333"
    hero_overlay, tab_text_color = "rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.8)", "#ffffff"
else:
    bg_app, text_main, bg_sidebar = "#fcfaf2", "#1a1a1a", "#f4ebd0"
    card_bg, card_border = "#ffffff", "#e2d1b3"
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
        st.button("Ouvrir mon espace", key="go_profil", use_container_width=True, on_click=changer_page, args=("MON PROFIL & PANIER",))
    with col2:
        st.markdown('<div class="card-capsule">📦<h4>Suivi Commandes</h4><p>Suivez vos confections en temps réel.</p></div>', unsafe_allow_html=True)
        st.button("Suivre mes commandes", key="go_commandes", use_container_width=True, on_click=changer_page, args=("📦 SUIVI DES COMMANDES",))
    with col3:
        st.markdown('<div class="card-capsule">🧥<h4>Galerie Modèles</h4><p>Découvrez nos collections exclusives.</p></div>', unsafe_allow_html=True)
        st.button("Voir la collection", key="go_galerie", use_container_width=True, on_click=changer_page, args=("COLLECTIONS (GALERIE)",))

# 2. GALERIE
elif st.session_state.page_actuelle == "COLLECTIONS (GALERIE)":
    st.button("⬅️ Retour à l'Accueil", key="btn_ret_galerie", on_click=changer_page, args=("ACCUEIL",))
    st.markdown("<h1 style='text-align: center; color: #d4af37;'>MODÈLES & CRÉATIONS</h1>", unsafe_allow_html=True)
    
    modeles = donnees.get("modeles", [])
    if modeles:
        cols = st.columns(3)
        for idx, mod in enumerate(modeles):
            with cols[idx % 3]:
                st.markdown("<div class='card-capsule'>", unsafe_allow_html=True)
                if mod["image"].startswith("data:image") or mod["image"].startswith("http") or mod["image"].startswith("images/"):
                    st.image(mod["image"], use_container_width=True)
                st.markdown(f"<h3 style='color:#d4af37;'>{mod['nom']}</h3>", unsafe_allow_html=True)
                st.write(mod["description"])
                st.markdown(f"<p style='color:#d4af37; font-weight:bold; font-size:18px;'>{mod['prix']} FCFA</p>", unsafe_allow_html=True)
                
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

# 3. PROFIL & PANIER CLIENT
elif st.session_state.page_actuelle == "MON PROFIL & PANIER":
    st.button("⬅️ Retour à l'Accueil", key="btn_ret_profil", on_click=changer_page, args=("ACCUEIL",))
    
    if st.session_state.client_connecte is None:
        st.warning("Veuillez vous connecter dans l'Espace Client sur la barre latérale gauche pour voir votre profil.")
    else:
        nom_c = st.session_state.client_connecte
        st.markdown(f"<h1 style='text-align: center; color: #d4af37;'>ESPACE DE {nom_c}</h1>", unsafe_allow_html=True)
        tab_profil, tab_panier = st.tabs(["👤 Mes Informations & Mesures", "🛒 Mon Panier d'Achat"])
        
        with tab_profil:
            client_data = donnees["clients"].get(nom_c, {"telephone": "", "mesures_haut": {}, "mesures_bas": {}})
            st.write(f"**Téléphone enregistré :** {client_data.get('telephone', 'Non renseigné')}")
            
            with st.form("modif_mesures_client"):
                nv_tel = st.text_input("Mettre à jour mon téléphone :", value=client_data.get("telephone", ""))
                colh, colb = st.columns(2)
                mesures_haut_maj = {}
                mesures_bas_maj = {}
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
                    donnees["clients"][nom_c] = {"telephone": nv_tel, "mesures_haut": mesures_haut_maj, "mesures_bas":  mesures_bas_maj}
                    sauvegarder_donnees(donnees)
                    st.success("Profil mis à jour avec succès !")
                    st.rerun()
            
        with tab_panier:
            st.write("### 🛒 Votre panier actuel")
            if st.session_state.panier:
                total_panier = 0
                for idx, item in enumerate(st.session_state.panier):
                    col_p1, col_p2, col_p3 = st.columns([3, 2, 1])
                    with col_p1: st.write(f"**{item['nom']}**")
                    with col_p2:
                        st.write(f"{item['prix']} FCFA")
                        total_panier += int(item['prix'])
                    with col_p3:
                        if st.button("Retirer", key=f"del_pan_{idx}"):
                            st.session_state.panier.remove(item)
                            st.rerun()
                st.markdown("---")
                st.markdown(f"### 💰 TOTAL À PAYER : {total_panier} FCFA")
                if st.button("🚀 VALIDER LA COMMANDE", use_container_width=True):
                    if "commandes" not in donnees: donnees["commandes"] = {}
                    for item in st.session_state.panier:
                        new_id = f"CMD-{len(donnees['commandes']) + 101}"
                        donnees["commandes"][new_id] = {
                            "client": nom_c, "modele": item["nom"], "prix": int(item["prix"]),
                            "avance": 0, "statut": "En attente", "date_livraison": "À définir"
                        }
                    sauvegarder_donnees(donnees)
                    st.session_state.panier = []
                    st.success("🎉 Commande envoyée !")
                    st.rerun()
            else:
                st.info("Votre panier est vide.")

# 4. SUIVI COMMANDES
elif st.session_state.page_actuelle == "📦 SUIVI DES COMMANDES":
    st.button("⬅️ Retour à l'Accueil", key="btn_ret_suivi", on_click=changer_page, args=("ACCUEIL",))
    st.markdown("<h1 style='text-align: center; color: #d4af37;'>📦 SUIVI DE VOS CONFECTIONS</h1>", unsafe_allow_html=True)
    
    nom_rech = st.session_state.client_connecte if st.session_state.client_connecte else st.text_input("Entrez votre Nom Complet pour le suivi :").strip().upper()
    
    if nom_rech:
        cmds = donnees.get("commandes", {})
        cmds_client = {k: v for k, v in cmds.items() if v.get("client", "").upper() == nom_rech}
        if cmds_client:
            for id_cmd, cmd in cmds_client.items():
                st.info(f"Commande {id_cmd} ({cmd['modele']}) : Statut = {cmd['statut']} | Reste à payer = {int(cmd['prix']) - int(cmd['avance'])} FCFA")
        else:
            st.info("Aucune commande enregistrée pour ce nom.")

# 5. PARAMÈTRES (ADMIN)
elif st.session_state.page_actuelle == "⚙️ PARAMÈTRES":
    st.button("⬅️ Retour à l'Accueil", key="btn_ret_admin", on_click=changer_page, args=("ACCUEIL",))
    st.markdown("<h1 style='color: #d4af37;'>WORKSHOP INTERFACE (PRO)</h1>", unsafe_allow_html=True)
    
    # --- FORMULAIRE DE CONNEXION SÉCURISÉ POUR L'ADMIN ---
    if not st.session_state.admin_authentifie:
        with st.form("login_admin_form"):
            st.write("🔑 Entrez le code secret pour accéder à la gestion de l'atelier :")
            mdp_saisi = st.text_input("Code secret :", type="password", key="admin_password_field")
            bouton_valider = st.form_submit_button("🔓 Valider le mot de passe", use_container_width=True)
            
            if bouton_valider:
                if mdp_saisi == MOT_DE_PASSE_ADMIN:
                    st.session_state.admin_authentifie = True
                    st.success("Accès autorisé !")
                    st.rerun()
                else:
                    st.error("❌ Code secret incorrect.")
                    
    # --- INTERFACE DE GESTION (S'affiche uniquement si authentifié) ---
    if st.session_state.admin_authentifie:
        if st.button("🔒 Se déconnecter de l'Atelier", key="btn_logout_admin"):
            st.session_state.admin_authentifie = False
            st.rerun()
            
        # NOUVEAUTÉ : On crée 4 onglets, dont un dédié à la Base Clients
        tab1, tab2, tab3, tab4 = st.tabs(["🧥 Ajouter un modèle", "🗑️ Gérer la vitrine", "👥 Base Clients", "📦 Suivi Commandes"])
        
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
                    with col_m1: st.write(f"👔 **{mod['nom']}** — {mod['prix']} FCFA")
                    with col_m2:
                        if st.button("❌ Supprimer", key=f"del_admin_{mod['id']}"):
                            donnees["modeles"].pop(idx)
                            sauvegarder_donnees(donnees)
                            st.success(f"{mod['nom']} supprimé !")
                            st.rerun()
            else:
                st.info("Aucun modèle enregistré.")

        with tab3:
            st.write("### 👥 Annuaire et Base de données Clients")
            
            # FILTRE DE RECHERCHE
            recherche = st.text_input("🔍 Rechercher un client (Nom ou Numéro de téléphone) :").strip().upper()
            
            clients_dict = donnees.get("clients", {})
            commandes_dict = donnees.get("commandes", {})
            
            if not clients_dict:
                st.info("Aucun client n'est encore enregistré dans la base.")
            else:
                for nom_client, infos in clients_dict.items():
                    tel_client = infos.get('telephone', 'Non renseigné')
                    
                    # Logique du filtre
                    if recherche and (recherche not in nom_client) and (recherche not in tel_client):
                        continue # Passe au client suivant si ça ne correspond pas à la recherche
                        
                    # Vérifier si le client a une commande en cours
                    cmds_client = {id_cmd: cmd for id_cmd, cmd in commandes_dict.items() if cmd['client'] == nom_client}
                    indicateur_commande = "🟢 OUI" if cmds_client else "🔴 NON"
                    
                    # ACCORDÉON (Clic pour ouvrir le profil)
                    with st.expander(f"👤 {nom_client} | 📞 {tel_client} | Commande en cours : {indicateur_commande}"):
                        col_h, col_b = st.columns(2)
                        
                        # Affichage des mesures
                        with col_h:
                            st.markdown("**📏 Haut du corps :**")
                            mesures_haut = infos.get("mesures_haut", {})
                            if mesures_haut:
                                for k, v in mesures_haut.items():
                                    if v > 0: st.write(f"- {k} : {v} cm")
                            else:
                                st.write("Aucune mesure")
                                
                        with col_b:
                            st.markdown("**📐 Bas du corps :**")
                            mesures_bas = infos.get("mesures_bas", {})
                            if mesures_bas:
                                for k, v in mesures_bas.items():
                                    if v > 0: st.write(f"- {k} : {v} cm")
                            else:
                                st.write("Aucune mesure")
                        
                        # Affichage des commandes spécifiques à ce client
                        if cmds_client:
                            st.markdown("---")
                            st.markdown("#### 📦 État des commandes de ce client :")
                            for id_cmd, cmd in cmds_client.items():
                                st.info(f"**N° {id_cmd}** ({cmd['modele']}) | Statut actuel : **{cmd['statut']}**")

        with tab4:
            st.write("### 📦 Mettre à jour l'évolution des commandes")
            commandes_dict = donnees.get("commandes", {})
            if commandes_dict:
                for id_cmd, cmd in list(commandes_dict.items()):
                    with st.expander(f"⚙️ Commande {id_cmd} — Client : {cmd['client']}"):
                        st.write(f"**Modèle commandé :** {cmd['modele']}")
                        st.write(f"**Prix total :** {cmd['prix']} FCFA")
                        
                        # Modification du statut et de l'avance
                        nv_avance = st.number_input(f"Avance reçue (FCFA) :", value=int(cmd.get('avance', 0)), step=5000, key=f"av_{id_cmd}")
                        nv_statut = st.selectbox(f"Statut confection :", ["En attente", "En coupe", "Au montage", "Finitions", "Prêt !"], index=["En attente", "En coupe", "Au montage", "Finitions", "Prêt !"].index(cmd.get('statut', 'En attente')), key=f"st_{id_cmd}")
                        
                        if st.button("💾 Mettre à jour la commande", key=f"save_{id_cmd}"):
                            donnees["commandes"][id_cmd]["avance"] = int(nv_avance)
                            donnees["commandes"][id_cmd]["statut"] = nv_statut
                            sauvegarder_donnees(donnees)
                            st.success("Statut de la commande mis à jour !")
                            st.rerun()
            else:
                st.info("Aucune commande en cours à l'atelier.")
