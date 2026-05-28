"""
Vérifie Trello + Gmail à partir de scripts/.env (ne jamais committer .env).
Usage: py -3 check_tokens.py
"""

import os
import smtplib
import sys

import requests
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

load_dotenv()

KEY = os.getenv("TRELLO_API_KEY", "").strip()
TOKEN = os.getenv("TRELLO_TOKEN", "").strip()
BOARD = os.getenv("BOARD_ID", "").strip()
GMAIL_USER = os.getenv("GMAIL_USER", "").strip()
GMAIL_PASS = os.getenv("GMAIL_PASSWORD", "").strip()
ALICE = os.getenv("ALICE_EMAIL", "").strip()


def mask(s: str, show: int = 4) -> str:
    if not s:
        return "(vide)"
    if len(s) <= show * 2:
        return "*" * len(s)
    return f"{s[:show]}...{s[-show:]} (len={len(s)})"


def check_trello() -> bool:
    print("\n--- Trello ---")
    if not KEY or not TOKEN:
        print("❌ TRELLO_API_KEY ou TRELLO_TOKEN manquant dans .env")
        return False
    print(f"  API Key : {mask(KEY)}")
    print(f"  Token   : {mask(TOKEN)}")
    print(f"  Board   : {BOARD or '(vide)'}")

    r = requests.get(
        "https://api.trello.com/1/members/me",
        params={"key": KEY, "token": TOKEN},
        timeout=20,
    )
    if r.status_code == 401:
        print(f"❌ Trello 401 : {r.text.strip()}")
        print("   → Régénère clé + token : https://trello.com/power-ups/admin")
        return False
    if not r.ok:
        print(f"❌ Trello HTTP {r.status_code} : {r.text[:200]}")
        return False

    me = r.json()
    print(f"✅ Connecté en tant que : {me.get('fullName') or me.get('username')}")

    if BOARD:
        rb = requests.get(
            f"https://api.trello.com/1/boards/{BOARD}",
            params={"key": KEY, "token": TOKEN},
            timeout=20,
        )
        if rb.ok:
            print(f"✅ Board OK : {rb.json().get('name')}")
            rl = requests.get(
                f"https://api.trello.com/1/boards/{BOARD}/lists",
                params={"key": KEY, "token": TOKEN},
                timeout=20,
            )
            if rl.ok:
                listes = [x["name"] for x in rl.json()]
                print(f"   Listes ({len(listes)}) : {', '.join(listes[:8])}{'...' if len(listes) > 8 else ''}")
                valider = [x for x in rl.json() if "valid" in x["name"].lower()]
                if valider:
                    print(f"✅ Liste « à valider » trouvée : {valider[0]['name']}")
                else:
                    print("⚠️  Aucune liste contenant « valider » — renomme ou adapte le script")
        else:
            print(f"❌ Board {BOARD} : HTTP {rb.status_code} {rb.text[:120]}")
            return False
    return True


def check_gmail() -> bool:
    print("\n--- Gmail (SMTP) ---")
    if not GMAIL_USER or not GMAIL_PASS:
        print("❌ GMAIL_USER ou GMAIL_PASSWORD manquant")
        return False
    print(f"  From : {GMAIL_USER}")
    print(f"  To   : {ALICE or '(non défini)'}")
    pwd = GMAIL_PASS
    non_ascii = [c for c in pwd if ord(c) > 127]
    if non_ascii:
        print(f"⚠️  Mot de passe avec caractères non-ASCII : {non_ascii[:5]}")
        print("   → Recopie le mot de passe d'application Google (16 lettres latines)")
    print(f"  Pass  : {mask(pwd)} (len={len(pwd)})")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
            server.login(GMAIL_USER, pwd)
        print("✅ Connexion Gmail OK")
        return True
    except smtplib.SMTPAuthenticationError:
        print("❌ Gmail : identifiants refusés (mauvais mot de passe d'application ?)")
        print("   → https://myaccount.google.com/apppasswords")
        return False
    except Exception as e:
        print(f"❌ Gmail : {e}")
        return False


def main():
    print("TOYA — vérification des tokens (.env)")
    ok_t = check_trello()
    ok_g = check_gmail()
    print("\n" + "=" * 40)
    if ok_t and ok_g:
        print("✅ Tout est prêt → py -3 toya_automation.py")
    elif ok_t:
        print("⚠️  Trello OK, Gmail à corriger")
    elif ok_g:
        print("⚠️  Gmail OK, Trello à corriger")
    else:
        print("❌ Corrige .env puis relance ce script")
    return 0 if (ok_t and ok_g) else 1


if __name__ == "__main__":
    raise SystemExit(main())
