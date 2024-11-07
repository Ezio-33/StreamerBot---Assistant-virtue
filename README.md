# StreamerBot - Assistant virtuel pour Streamer Dashboard

## Introduction

StreamerBot est un assistant virtuel intelligent conçu pour optimiser l'expérience des utilisateurs du site [Streamer Dashboard](https://streamer-dashboard.ailicia.live/signup?via=ref-ezio_33). Ce chatbot local offre une interaction fluide et naturelle, sans nécessiter de connexion internet, et fonctionne sur des configurations matérielles modestes.

### Liens importants

- [Site de présentation du projet](https://presentation-streamerbot.netlify.app)
- [Profil LinkedIn de l'auteur](www.linkedin.com/in/samuel-verschueren)
- [Article de blog final](https://www.linkedin.com/pulse/streamerbot-un-assistant-virtuel-intelligent-pour-des-verschueren-xub3e/?trackingId=1hJ4av66R4uFJ9VsSQuDbQ%3D%3D)

## Démonstration

Voici une vidéo de démonstration du StreamerBot en action :

[![Démonstration StreamerBot](https://presentation-streamerbot.netlify.app/videos/Feedback.mp4)](https://presentation-streamerbot.netlify.app/videos/Feedback.mp4)

## Fonctionnalités

- 💬 **Chatbot local** : Réponses intelligentes sans connexion Internet
- ⚙️ **Personnalisable** : Ajustement des réponses selon les besoins
- 🖥️ **Performance optimisée** : Fonctionne sur hardware modeste

## Installation

1. **Cloner le dépôt** :

   ```bash
   git clone https://github.com/Ezio-33/StreamerBot---Assistant-virtuel-pour-Streamer-Dashboard.git
   cd StreamerBot---Assistant-virtuel-pour-Streamer-Dashboard
   git checkout Dev
   ```

2. **Installer les dépendances** :

   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration** :
   - Ajustez les paramètres dans le fichier `.env`
   - Modifiez `intents.json` pour personnaliser les interactions

## Utilisation

1. Lancez le script d’entraînement :
   ```bash
   python train.py
   ```
2. Lancez le script principal :
   ```bash
   python main.py
   ```
3. Interagissez avec le chatbot via l'interface console

4. Pour quitté sans entraîner le model a la fin de la session faire:
   ```bash
   ctrl c
   ```

## Prérequis

- **Matériel** :
  - Processeur Intel 8ème génération ou équivalent
  - 8 Go de RAM DDR4
  - Pas de GPU nécessaire
- **Logiciel** :
  - Python 3.8+
  - OS : Windows/Linux/Mac

## Projets connexes

- [Streamer Dashboard](https://streamer-dashboard.ailicia.live/signup?via=ref-ezio_33) : Plateforme de gestion pour streamers

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteur

Développé avec ❤️ par **Ezio-33** (Samuel Verschueren)

---

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue ou à me contacter directement via [LinkedIn](www.linkedin.com/in/samuel-verschueren).
