"""
TOYA AUTOMATION SCRIPT
======================
Ce script surveille Trello et envoie automatiquement
un email à Alice quand Yannick déplace une carte dans "À valider"

INSTALLATION :
pip install -r requirements.txt

CONFIGURATION :
Crée un fichier .env dans le même dossier avec :
TRELLO_API_KEY=ta_cle_api
TRELLO_TOKEN=ton_token
GMAIL_USER=ton_email@gmail.com
GMAIL_PASSWORD=ton_mot_de_passe_application
ALICE_EMAIL=alice@example.com
BOARD_ID=jHdTBDKu
"""

import requests
import smtplib
import sys
import time
import os

# Windows terminal (cp1252) : évite UnicodeEncodeError sur les emojis
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
ALICE_EMAIL = os.getenv("ALICE_EMAIL")
BOARD_ID = os.getenv("BOARD_ID", "jHdTBDKu")

# Liste des cartes déjà traitées (évite les doublons)
cartes_traitees = set()


def _trello_get(url, params=None):
    """GET Trello avec message d'erreur lisible."""
    p = {"key": TRELLO_API_KEY, "token": TRELLO_TOKEN}
    if params:
        p.update(params)
    response = requests.get(url, params=p, timeout=30)
    if not response.ok:
        print(f"❌ Trello HTTP {response.status_code}: {response.text[:300]}")
        return None
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"❌ Réponse Trello invalide: {response.text[:300]}")
        return None


def get_liste_id(nom_liste):
    """Récupère l'ID d'une liste par son nom"""
    url = f"https://api.trello.com/1/boards/{BOARD_ID}/lists"
    listes = _trello_get(url)
    if not listes:
        return None, None
    
    for liste in listes:
        if nom_liste.lower() in liste["name"].lower():
            return liste["id"], liste["name"]
    return None, None


def get_cartes_liste(liste_id):
    """Récupère toutes les cartes d'une liste"""
    url = f"https://api.trello.com/1/lists/{liste_id}/cards"
    cartes = _trello_get(url)
    return cartes if cartes else []


def envoyer_email_alice(carte_nom, carte_url, carte_desc):
    """Envoie l'email à Alice avec les détails du rapport"""
    
    semaine = datetime.now().strftime("%W")
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📊 Rapport hebdo TOYA — Semaine {semaine} — À valider"
    msg["From"] = GMAIL_USER
    msg["To"] = ALICE_EMAIL
    
    corps_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #1a1a2e; padding: 20px; border-radius: 10px;">
            <h1 style="color: #e94560;">🚗 TOYA</h1>
            <h2 style="color: white;">Rapport Hebdomadaire — Semaine {semaine}</h2>
        </div>
        
        <div style="padding: 20px; background-color: #f9f9f9; border-radius: 10px; margin-top: 15px;">
            <p>Bonjour Alice,</p>
            
            <p>Le rapport hebdomadaire de Yannick est prêt et en attente de ta validation.</p>
            
            <h3>📋 Détails :</h3>
            <ul>
                <li><strong>Carte :</strong> {carte_nom}</li>
                <li><strong>Semaine :</strong> {semaine}</li>
                <li><strong>Statut :</strong> À valider ✅</li>
            </ul>
            
            <h3>📝 Contenu du rapport :</h3>
            <div style="background-color: white; padding: 15px; border-left: 4px solid #e94560; border-radius: 5px;">
                {carte_desc if carte_desc else "Voir la carte Trello pour les détails"}
            </div>
            
            <div style="margin-top: 20px; text-align: center;">
                <a href="{carte_url}" 
                   style="background-color: #e94560; color: white; padding: 12px 25px; 
                          text-decoration: none; border-radius: 5px; font-weight: bold;">
                    👉 Voir le rapport sur Trello
                </a>
            </div>
            
            <p style="margin-top: 20px; color: #666;">
                Une fois validé, merci de déplacer la carte vers "Envoyé" 
                pour informer l'équipe.
            </p>
        </div>
        
        <div style="text-align: center; padding: 15px; color: #999; font-size: 12px;">
            TOYA Automation — Rapport généré automatiquement
        </div>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(corps_html, "html"))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, ALICE_EMAIL, msg.as_string())
        print(f"✅ Email envoyé à Alice pour : {carte_nom}")
        return True
    except Exception as e:
        print(f"❌ Erreur envoi email : {e}")
        return False


def surveiller_trello():
    """Boucle principale — surveille Trello toutes les 2 minutes"""
    missing = [n for n, v in [
        ("TRELLO_API_KEY", TRELLO_API_KEY),
        ("TRELLO_TOKEN", TRELLO_TOKEN),
        ("GMAIL_USER", GMAIL_USER),
        ("GMAIL_PASSWORD", GMAIL_PASSWORD),
        ("ALICE_EMAIL", ALICE_EMAIL),
    ] if not v]
    if missing:
        print(f"❌ Variables manquantes dans .env : {', '.join(missing)}")
        return

    print("🚗 TOYA Automation démarré...")
    print(f"📧 Surveillance active — Envoi vers : {ALICE_EMAIL}")
    print("=" * 50)
    
    # Récupérer l'ID de la liste "À valider"
    liste_id, liste_nom = get_liste_id("valider")
    
    if not liste_id:
        print("❌ Liste 'À valider' introuvable. Vérifie le nom de la liste dans Trello.")
        return
    
    print(f"✅ Liste surveillée : {liste_nom} (ID: {liste_id})")
    print("⏳ Vérification toutes les 2 minutes...\n")
    
    while True:
        try:
            cartes = get_cartes_liste(liste_id)
            
            for carte in cartes:
                carte_id = carte["id"]
                
                # Si carte pas encore traitée
                if carte_id not in cartes_traitees:
                    print(f"🔔 Nouvelle carte détectée : {carte['name']}")
                    
                    # Envoyer email à Alice
                    succes = envoyer_email_alice(
                        carte_nom=carte["name"],
                        carte_url=carte.get("url", ""),
                        carte_desc=carte.get("desc", "")
                    )
                    
                    if succes:
                        cartes_traitees.add(carte_id)
            
            # Attendre 2 minutes avant prochaine vérification
            time.sleep(120)
            
        except Exception as e:
            print(f"❌ Erreur : {e}")
            time.sleep(60)


if __name__ == "__main__":
    surveiller_trello()
