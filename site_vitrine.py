import streamlit as st
import json
import os
import base64
import requests

# Configuration de la page
st.set_page_config(
    page_title="DEMSY COUTURE AU MASCULIN",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration GitHub automatique
GITHUB_REPO = "demsy-couture/demsy-couture"
FICHIER_DONNEES = "donnees_atelier.json"

# Listes globales des mesures (accessibles sur toutes les pages)
champs_haut = ["Épaule", "Longueur de Manche", "Tour de Manche", "Poitrine", "Ventre", "Longueur Haut", "Col", "Dos"]
champs_bas = ["Ceinture", "Bassin", "Cuisse", "Longueur Bas", "Mollet", "Bas", "Frappe"]

# Récupération sécurisée de la clé depuis les Secrets de Streamlit
TOKEN_GH = st.secrets.get("GITHUB_TOKEN", "")

def charger_donnees():
    structure_vide = {"configuration": {}, "modeles": [], "clients": {}, "commandes": {}}
    
    if TOKEN_GH:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FICHIER_DONNEES}"
        headers = {"Authorization": f"token {TOKEN_GH}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            try:
                contenu_b64 = res.json()["content"]
                contenu_json = base64.b64decode(contenu_b64).decode("utf-8")
                donnees_chargees = json.loads(contenu_json)
                for cle in structure_vide:
                    if cle not in donnees_chargees:
                        donnees_chargees[cle] = structure_vide[cle]
                return donnees_chargees
            except:
                pass

    if os.path.exists(FICHIER_DONNEES):
        with open(FICHIER_DONNEES, "r", encoding="utf-8") as f:
            try:
                contenu = f.read().strip()
                if contenu:
                    donnees_chargees = json.loads(contenu)
                    for cle in structure_vide:
                        if cle not in donnees_chargees:
                            donnees_chargees[cle] = structure_vide[cle]
                    return donnees_chargees
            except Exception as e:
                st.error(f"Erreur de lecture : {e}")
    return structure_vide

def sauvegarder_donnees(donnees):
    with open(FICHIER_DONNEES, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)
        
    if TOKEN_GH:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FICHIER_DONNEES}"
        headers = {"Authorization": f"token {TOKEN_GH}"}
        
        res_get = requests.get(url, headers=headers)
        sha = res_get.json().get("sha", "") if res_get.status_code == 200 else ""
        
        nouveau_contenu = json.dumps(donnees, indent=4, ensure_ascii=False)
        contenu_b64 = base64.b64encode(nouveau_contenu.encode("utf-8")).decode("utf-8")
        
        payload = {
            "message": "Mise à jour automatique de la base client (Demsy App)",
            "content": contenu_b64,
            "sha": sha
        }
        
        requests.put(url, headers=headers, json=payload)

donnees = charger_donnees()
config = donnees.get("configuration", {})

MOT_DE_PASSE_ADMIN = "16129489f"
liste_pages = ["ACCUEIL", "COLLECTIONS (GALERIE)", "MON PROFIL & PANIER", "📦 SUIVI DES COMMANDES", "⚙️ PARAMÈTRES"]

def changer_page(nouvelle_page):
    st.session_state.page_actuelle = nouvelle_page
    st.session_state.nav_radio = nouvelle_page

def connexion_client(nom, tel):
    nom_clean = nom.strip().upper()
    if nom_clean:
        st.session_state.client_connecte = nom_clean
        if nom_clean not in donnees["clients"]:
            donnees["clients"][nom_clean] = {"telephone": tel, "mesures_haut": {}, "mesures_bas": {}, "photo_profil": ""}
            sauvegarder_donnees(donnees)
        st.session_state.page_actuelle = "ACCUEIL"
        st.session_state.nav_radio = "ACCUEIL"

def deconnexion_client():
    st.session_state.client_connecte = None
    st.session_state.panier = []
    st.session_state.page_actuelle = "ACCUEIL"
    st.session_state.nav_radio = "ACCUEIL"

if "page_actuelle" not in st.session_state: st.session_state.page_actuelle = "ACCUEIL"
if "client_connecte" not in st.session_state: st.session_state.client_connecte = None
if "panier" not in st.session_state: st.session_state.panier = []
if "admin_authentifie" not in st.session_state: st.session_state.admin_authentifie = False

if os.path.exists("logo.jpg"):
    st.sidebar.image("logo.jpg", use_container_width=True)
else:
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

index_page = liste_pages.index(st.session_state.page_actuelle) if st.session_state.page_actuelle in liste_pages else 0
menu = st.sidebar.radio("Navigation :", liste_pages, index=index_page, key="nav_radio")
if menu != st.session_state.page_actuelle: st.session_state.page_actuelle = menu

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
    st.markdown(f'<div class="hero-container"><div class="hero-title">{titre_dynamique}</div><div class="hero-subtitle">APPELEZ-NOUS / ECRIVEZ-NUOS AU 05 46 13 77 01</div></div>', unsafe_allow_html=True)
    
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
                        if st.session_state.client_connecte is None: st.warning("Connectez-vous à gauche d'abord !")
                        else:
                            st.session_state.panier.append(mod)
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("🧥 Aucun modèle n'est exposé dans la galerie pour l'instant. Connectez-vous en tant qu'administrateur dans l'onglet PARAMÈTRES pour ajouter vos premières créations !")

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
            client_data = donnees["clients"].get(nom_c, {"telephone": "", "mesures_haut": {}, "mesures_bas": {}, "photo_profil": ""})
            st.write(f"**Téléphone enregistré :** {client_data.get('telephone', 'Non renseigné')}")
            
            photo_actuelle = client_data.get("photo_profil", "")
            if photo_actuelle: st.image(photo_actuelle, caption="Votre photo de profil", width=150)
            
            with st.form("modif_mesures_client"):
                nv_tel = st.text_input("Mettre à jour mon téléphone :", value=client_data.get("telephone", ""))
                fichier_photo = st.file_uploader("Choisissez une photo de vous (JPG ou PNG) :", type=["png", "jpg", "jpeg"])
                
                colh, colb = st.columns(2)
                mesures_haut_maj, mesures_bas_maj = {}, {}
                
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
                    if fichier_photo:
                        bytes_data = fichier_photo.getvalue()
                        b64_img = base64.b64encode(bytes_data).decode("utf-8")
                        ext = fichier_photo.name.split(".")[-1]
                        photo_actuelle = f"data:image/{ext};base64,{b64_img}"
                    
                    donnees["clients"][nom_c] = {
                        "telephone": nv_tel, "mesures_haut": mesures_haut_maj, "mesures_bas": mesures_bas_maj, "photo_profil": photo_actuelle
                    }
                    sauvegarder_donnees(donnees)
                    st.success("Profil enregistré et synchronisé avec GitHub !")
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
                st.info("Votre panier est vide. Parcourez la Galerie pour ajouter des tenues.")

# 4. SUIVI COMMANDES PUBLIC
elif st.session_state.page_actuelle == "📦 SUIVI DES COMMANDES":
    st.button("⬅️ Retour à l'Accueil", key="btn_ret_suivi", on_click=changer_page, args=("ACCUEIL",))
    st.markdown("<h1 style='text-align: center; color: #d4af37;'>📦 SUIVI DE VOS CONFECTIONS</h1>", unsafe_allow_html=True)
    nom_rech = st.session_state.client_connecte if st.session_state.client_connecte else st.text_input("Entrez votre Nom Complet pour le suivi :").strip().upper()
    if nom_rech:
        cmds = donnees.get("commandes", {})
        cmds_client = {k: v for k, v in cmds.items() if v.get("client", "").upper() == nom_rech}
        if cmds_client:
            for id_cmd, cmd in cmds_client.items():
                st.info(f"Commande {id_cmd} ({cmd['modele']}) : Statut = {cmd['statut']} | Date de livraison prévue = {cmd.get('date_livraison', 'À définir')} | Reste à payer = {int(cmd['prix']) - int(cmd['avance'])} FCFA")
                
                modeles_liste = donnees.get("modeles", [])
                image_trouvee = next((m["image"] for m in modeles_liste if m["nom"].strip().lower() == cmd.get("modele", "").strip().lower()), None)
                if image_trouvee:
                    st.image(image_trouvee, width=150)
                st.markdown("---")
        else: st.info("Aucune commande enregistrée pour ce nom.")

# 5. PARAMÈTRES (ADMIN)
elif st.session_state.page_actuelle == "⚙️ PARAMÈTRES":
    st.button("⬅️ Retour à l'Accueil", key="btn_ret_admin", on_click=changer_page, args=("ACCUEIL",))
    st.markdown("<h1 style='color: #d4af37;'>WORKSHOP INTERFACE (PRO)</h1>", unsafe_allow_html=True)
    
    if not st.session_state.admin_authentifie:
        with st.form("login_admin_form"):
            mdp_saisi = st.text_input("Code secret :", type="password")
            if st.form_submit_button("🔓 Valider"):
                if mdp_saisi == MOT_DE_PASSE_ADMIN:
                    st.session_state.admin_authentifie = True
                    st.rerun()
                else: st.error("❌ Code secret incorrect.")
                    
    if st.session_state.admin_authentifie:
        if st.button("🔒 Se déconnecter de l'Atelier"):
            st.session_state.admin_authentifie = False
            st.rerun()
            
        tab1, tab2, tab3, tab4 = st.tabs(["🧥 Ajouter un modèle", "🗑️ Gérer la vitrine", "👥 Base Clients", "📦 Suivi Commandes"])
        
        with tab1:
            with st.form("form_pub_modele"):
                m_nom = st.text_input("Nom de la création :")
                m_desc = st.text_area("Description :")
                m_prix = st.number_input("Prix (FCFA) :", min_value=0, step=5000)
                m_file = st.file_uploader("Photo :", type=["png", "jpg", "jpeg"])
                if st.form_submit_button("Mettre en vitrine"):
                    if m_nom and m_file:
                        bytes_data = m_file.getvalue()
                        b64_img = base64.b64encode(bytes_data).decode("utf-8")
                        ext = m_file.name.split(".")[-1]
                        donnees["modeles"].append({"id": f"mod_{len(donnees['modeles'])+1}", "nom": m_nom, "description": m_desc, "prix": int(m_prix), "image": f"data:image/{ext};base64,{b64_img}"})
                        sauvegarder_donnees(donnees)
                        st.success("Publié avec succès !")
                        st.rerun()

        with tab2:
            st.write("### 🗑️ Gestion des modèles exposés")
            modeles = donnees.get("modeles", [])
            if modeles:
                for idx, mod in enumerate(modeles):
                    col_m1, col_m2 = st.columns([4, 1])
                    with col_m1: st.write(f"👔 **{mod['nom']}** — {mod['prix']} FCFA")
                    with col_m2:
                        if st.button("❌ Supprimer", key=f"del_admin_{mod['id']}"):
                            modeles.pop(idx)
                            sauvegarder_donnees(donnees)
                            st.rerun()
            else:
                st.info("Aucun modèle n'est enregistré dans la vitrine. Utilisez le premier onglet pour en ajouter.")

        with tab3:
            st.write("### 👥 Annuaire et Base de données Clients")
            recherche = st.text_input("🔍 Rechercher un client :").strip().upper()
            clients_dict = donnees.get("clients", {})
            
            if clients_dict:
                for nom_client, infos in list(clients_dict.items()):
                    tel_client = infos.get('telephone', 'Non renseigné')
                    if recherche and (recherche not in nom_client) and (recherche not in str(tel_client)): continue
                    
                    with st.expander(f"👤 {nom_client} | 📞 {tel_client}"):
                        photo_p = infos.get("photo_profil", "")
                        if photo_p: st.image(photo_p, width=120)
                        
                        with st.form(f"form_admin_edit_{nom_client}"):
                            nv_tel_admin = st.text_input("Téléphone :", value=tel_client, key=f"ad_tel_{nom_client}")
                            col_h, col_b = st.columns(2)
                            mesures_haut_admin, mesures_bas_admin = {}, {}
                            
                            with col_h:
                                st.markdown("**📏 Haut du corps :**")
                                for m in champs_haut:
                                    v = infos.get("mesures_haut", {}).get(m, 0.0)
                                    mesures_haut_admin[m] = st.number_input(f"{m} (cm)", value=float(v), step=0.5, key=f"ad_h_{m}_{nom_client}")
                            with col_b:
                                st.markdown("**📐 Bas du corps :**")
                                for m in champs_bas:
                                    v = infos.get("mesures_bas", {}).get(m, 0.0)
                                    mesures_bas_admin[m] = st.number_input(f"{m} (cm)", value=float(v), step=0.5, key=f"ad_b_{m}_{nom_client}")
                            
                            if st.form_submit_button("💾 Sauvegarder pour ce client"):
                                donnees["clients"][nom_client] = {"telephone": nv_tel_admin, "mesures_haut": mesures_haut_admin, "mesures_bas": mesures_bas_admin, "photo_profil": photo_p}
                                sauvegarder_donnees(donnees)
                                st.success("Mis à jour avec succès sur GitHub !")
                                st.rerun()
            else:
                st.info("Aucun client enregistré pour le moment.")

        with tab4:
            st.write("### 📦 Gestion du suivi des commandes reçues")
            commandes_dict = donnees.get("commandes", {})
            if commandes_dict:
                # Créer une liste figée des clés pour éviter tout bug lors de la suppression
                liste_cles_commandes = list(commandes_dict.keys())
                for id_cmd in liste_cles_commandes:
                    if id_cmd not in donnees["commandes"]: continue
                    cmd = donnees["commandes"][id_cmd]
                    
                    with st.expander(f"⚙️ Commande {id_cmd} — {cmd['client']}"):
                        st.markdown(f"**Modèle commandé :** {cmd.get('modele')} | **Prix total :** {cmd.get('prix')} FCFA")
                        
                        # Recherche robuste et affichage de la photo
                        modeles_liste = donnees.get("modeles", [])
                        image_trouvee = next((m["image"] for m in modeles_liste if m["nom"].strip().lower() == cmd.get("modele", "").strip().lower()), None)
                        
                        if image_trouvee:
                            st.image(image_trouvee, width=200)
                        
                        nv_avance = st.number_input(f"Avance reçue (FCFA) :", value=int(cmd.get('avance', 0)), key=f"av_{id_cmd}")
                        nv_statut = st.selectbox(f"Statut actuel :", ["En attente", "En coupe", "Au montage", "Finitions", "Prêt !"], index=["En attente", "En coupe", "Au montage", "Finitions", "Prêt !"].index(cmd.get('statut', 'En attente')), key=f"st_{id_cmd}")
                        nv_date = st.text_input(f"Date de livraison prévue :", value=cmd.get('date_livraison', 'À définir'), key=f"dt_{id_cmd}")
                        
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            if st.button("💾 Mettre à jour la commande", key=f"save_{id_cmd}", use_container_width=True):
                                donnees["commandes"][id_cmd]["avance"] = int(nv_avance)
                                donnees["commandes"][id_cmd]["statut"] = nv_statut
                                donnees["commandes"][id_cmd]["date_livraison"] = nv_date
                                sauvegarder_donnees(donnees)
                                st.success("Commande mise à jour !")
                                st.rerun()
                        with btn_col2:
                            if st.button("❌ Supprimer définitivement la commande", key=f"del_cmd_{id_cmd}", use_container_width=True):
                                del donnees["commandes"][id_cmd]
                                sauvegarder_donnees(donnees)
                                st.success("Commande supprimée avec succès !")
                                st.rerun()
            else:
                st.info("Aucune commande n'a encore été passée par les clients.")
