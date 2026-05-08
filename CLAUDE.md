# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚠️ IDENTITÉ DE MARQUE — Source unique de vérité

**Avant tout travail visuel, marketing ou éditorial, lire `documents/identite-marque-TOYA.md`.**

Cette brand bible est la référence officielle. Elle prime sur tous les autres documents en cas de conflit visuel ou de couleur.

**Logo :** `assets/logo-toya.jpg` (à uploader dans Nano Banana / Veo 3 pour tout visuel)
**Slogan :** « Le continent en mouvement »

**Palette HEX officielle :**
- TOYA Aubergine `#190334` — primaire, fonds
- TOYA Ivoire `#F6F5FB` — texte clair
- TOYA Lavande `#E0D4EE` — accents doux
- TOYA Violet `#644090` — accents punchy

**Règle 70/20/10 :** 70% aubergine, 20% ivoire, 10% violet+lavande.

## Contexte du projet

Ce dépôt contient la documentation stratégique et marketing pour **TOYA**, une startup de mobilité africaine. Le ride-hailing au Cameroun (Douala en priorité) est la première verticale ; le logo et le slogan signalent une **ambition panafricaine** (« Le continent en mouvement »).

**Confidentialité :** Tous les documents sont confidentiels (mai 2026). Co-fondateurs : Dominique & Alice Nolla.

## Documents disponibles

| Fichier | Contenu |
|---|---|
| `documents/identite-marque-TOYA.md` | **Brand bible** — logo, palette HEX, ton, typo, règles de composition. À lire en premier. |
| `documents/yango_offres_produit_TOYA.md` | Offres TOYA (Éco, Confort, Confort+, Moto), grilles tarifaires FCFA, specs véhicules |
| `documents/yango_croissance_marketing_TOYA.md` | Stratégie de croissance : historique Yango 2018–2025, leviers marketing |
| `documents/yango_analyse_afrique_TOYA.md` | Analyse concurrentielle : positionnement vs Yango, données marché, opportunités |
| `documents/yango_marketing_analyse_TOYA.md` | Analyse marketing digitale : ton site Yango, réseaux sociaux, posts modèles, budget |

## Agents disponibles (`.claude/agents/`)

13 agents sont configurés dans ce projet. Ils respectent tous le format Claude Code (frontmatter `name` kebab-case, `tools` en ligne).

**Agents stratégiques (texte) :**
- `analyse-afrique` — concurrentiel et marché Afrique
- `croissance-marketing` — leviers de croissance, modèle asset-light
- `marketing-digital` — calendrier éditorial, posts, budget
- `offres-produit` — classes de service, tarifs, specs

**Agents visuels (Nano Banana — Gemini) :**
- `nano-banana-post-instagram` — post carré 1080×1080
- `nano-banana-story-instagram` — story verticale 1080×1920
- `nano-banana-campagne-visuelle` — série de 3-5 visuels cohérents

**Agents vidéo (Veo 3 — Gemini) :**
- `veo3-reels-instagram` — Reels 9:16 jusqu'à 8s
- `veo3-tiktok` — TikTok 9:16 viral
- `veo3-campagne-video` — série multiplateforme Reels + TikTok

**Agents équipe campagne (workflow à 3 agents) :**
- `campagne-stratege` — Agent 1 : brief stratégique, cible, promesse, KPI, répartition des tâches
- `campagne-creatif` — Agent 2 : idées créatives, contenus, scripts, prompts, calendrier
- `campagne-correcteur` — Agent 3 : critique, correction, arbitrage et validation finale

Chaque agent visuel / vidéo lit obligatoirement `documents/identite-marque-TOYA.md` avant de produire un prompt et applique le logo + la palette + le ton TOYA dans chaque sortie.

## Architecture de la réflexion stratégique

Ordre de lecture recommandé :

1. **Identité de marque** (`documents/identite-marque-TOYA.md`) — qui on est, comment on parle, comment on apparaît
2. **Analyse marché** (`yango_analyse_afrique_TOYA.md`) — le terrain concurrentiel
3. **Offres produit** (`yango_offres_produit_TOYA.md`) — ce que TOYA propose
4. **Stratégie de croissance** (`yango_croissance_marketing_TOYA.md`) — comment grandir
5. **Exécution marketing** (`yango_marketing_analyse_TOYA.md`) — contenus, canaux, budget

## Dossiers de travail

| Dossier | Usage |
|---|---|
| `assets/` | Logo et matériel visuel de marque (logo-toya.jpg) |
| `documents/` | Documents stratégiques + brand bible |
| `contenu-hebdo/` | Lots de contenus hebdomadaires générés (vide pour l'instant) |
| `data/` | Données brutes (chiffres marché, enquêtes) |
| `pos/` | Matériaux point de vente / terrain |
| `reseau/` | Stratégie réseau chauffeurs / partenaires |
| `trimestre/` | Plans et bilans trimestriels |

## Backups automatiques

`.claude/agents/_backup_avant_correction/` et `.claude/agents/_backup_avant_brand_bible/` contiennent les versions historiques des agents (avant correction du frontmatter et avant injection de la brand bible). Sûr à supprimer une fois la stabilité confirmée.
