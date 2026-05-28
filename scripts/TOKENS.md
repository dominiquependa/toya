# Gestion des tokens TOYA

## Fichier secret (local uniquement)

`scripts/.env` — **jamais commité** (déjà dans `.gitignore`).

```env
TRELLO_API_KEY=
TRELLO_TOKEN=
GMAIL_USER=
GMAIL_PASSWORD=
ALICE_EMAIL=
BOARD_ID=jHdTBDKu
```

## Trello — régénérer clé + token

1. https://trello.com/power-ups/admin
2. Ouvrir le Power-Up **TOYA**
3. Onglet **API Key** → **Generate a new API Key**
4. Cliquer le lien **Token** → **Allow** → copier le token
5. Coller les deux valeurs dans `.env`
6. Tester : `py -3 check_tokens.py`

La clé et le token doivent être générés **ensemble** (même Power-Up).

## Gmail — mot de passe d'application

1. https://myaccount.google.com/apppasswords
2. Créer un mot de passe pour « Mail » / « Autre »
3. Copier les **16 lettres latines** (sans espaces, sans caractères cyrilliques)
4. Mettre dans `GMAIL_PASSWORD=`
5. Tester : `py -3 check_tokens.py`

## Vérification rapide

```powershell
cd "C:\Users\domin\OneDrive\Bureau\yango marketing\scripts"
py -3 check_tokens.py
```

## Lancer l'automation

```powershell
py -3 toya_automation.py
```

## Sécurité

- Ne pas envoyer `.env` par email, chat ou GitHub
- Si un secret a été exposé : régénérer sur Trello et Google
