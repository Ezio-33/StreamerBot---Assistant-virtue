<p align="center">
   <img src="https://presentation-streamerbot.netlify.app/img/streamerbot_logo.png" alt="StreamerBot Logo">
</p>

# StreamerBot - Assistant virtuel pour Streamer Dashboard

## Introduction

StreamerBot est un assistant virtuel intelligent conçu pour optimiser l'expérience des utilisateurs du site [Streamer Dashboard](https://streamer-dashboard.ailicia.live/signup?via=ref-ezio_33). Ce chatbot local offre une interaction fluide et naturelle, sans nécessiter de connexion internet, et fonctionne sur des configurations matérielles modestes.

### Liens importants

- [Site de présentation du projet](https://presentation-streamerbot.netlify.app)
- [Profil LinkedIn de l'auteur](www.linkedin.com/in/samuel-verschueren)
- [Article de blog final](https://www.linkedin.com/pulse/streamerbot-un-assistant-virtuel-intelligent-pour-des-verschueren-xub3e/?trackingId=1hJ4av66R4uFJ9VsSQuDbQ%3D%3D)

## Démonstration

Voici une vidéo de démonstration du StreamerBot en action :

<p align="center">
  <a href="https://presentation-streamerbot.netlify.app/videos/Feedback.mp4" target="_blank" rel="noopener noreferrer">
    <img src="https://presentation-streamerbot.netlify.app/img/streamerbot_int.png" alt="Démonstration du StreamerBot" style="display: block; margin: auto;">
  </a>
</p>

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
   - Ajustez les paramètres dans le fichier de configuration `.env` pour adapter le bot à vos besoins.
   - L'installation ne nécessite pas de connexion Internet une fois les dépendances installées.

## Personnalisations

**Données d'entraînement** :

- Le bot utilise des données locales pour ajuster ses réponses. Pour personnaliser les interactions, modifiez le fichier `intents.json`.

Explication de la section JSON:

```json
{
  "tag": "greetings",
  "patterns": ["bonjour"],
  "responses": [
    "Bonjour ! Comment puis-je vous aider avec la configuration ou l'utilisation d'AI-licia ?"
  ],
  "context": [""]
}
```

- **tag** : Ce champ est une étiquette qui identifie la catégorie ou le type de message. Dans cet exemple, l'étiquette est "greetings" (salutations).

- **patterns** : Ce champ contient une liste de motifs ou de phrases que le chatbot doit reconnaître. Ici, le motif est "bonjour". Lorsque l'utilisateur tape "bonjour", le chatbot reconnaît ce motif.

- **responses** : Ce champ contient une liste de réponses que le chatbot peut donner lorsqu'il reconnaît un des motifs. Dans cet exemple, la réponse est "Bonjour ! Comment puis-je vous aider avec la configuration ou l'utilisation d'AI-licia ?".

- **context** : Ce champ est utilisé pour définir le contexte dans lequel cette réponse est valide. Dans cet exemple, le contexte est vide, ce qui signifie que cette réponse est toujours valide.

## Utilisation

1. Lancez le script d’entraînement si c'est la premiere fois que vous utiliser le chatbot:
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

## Technologies utilisées

- **Langage** : Python
- **Bibliothèques IA** : `transformers`, `torch`, `tensorflow` (pour le modèle de traitement du langage naturel)
- **Gestion des dialogues** : `nltk` pour les interactions conversationnelles

## Projets connexes

- [Streamer Dashboard](https://streamer-dashboard.ailicia.live/signup?via=ref-ezio_33) : Plateforme de gestion pour streamers

## Licence

Ce projet est sous licence CC BY-NC. Voir le fichier [LICENSE](Licence.txt) pour plus de détails.

## Auteur

Développé avec ❤️ par **Ezio-33** (Samuel Verschueren)

---

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue ou à me contacter directement via [LinkedIn](www.linkedin.com/in/samuel-verschueren).
