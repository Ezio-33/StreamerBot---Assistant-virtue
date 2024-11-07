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

[![Démonstration StreamerBot](https://presentation-streamerbot.netlify.app/videos/Feedback.mp4)](https://presentation-streamerbot.netlify.app/videos/Feedback.mp4)

<button onclick="toggleVideo()">Afficher/Masquer la vidéo</button>

<div id="videoContainer">
  <video width="600" controls>
    <source
      src="https://presentation-streamerbot.netlify.app/videos/Feedback.mp4"
      type="video/mp4"
    />
    Votre navigateur ne supporte pas la vidéo.
  </video>
</div>

<script>
  function toggleVideo() {
    var videoContainer = document.getElementById("videoContainer");
    if (videoContainer.style.display === "none") {
      videoContainer.style.display = "block";
    } else {
      videoContainer.style.display = "none";
    }
  }
</script>

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

Exemple:

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

Bien sûr ! Voici une explication détaillée pour aider les lecteurs à comprendre cette section du fichier

README.md

et à la personnaliser :

### Explication de la section JSON

Cette section du fichier

README.md

contient un exemple de configuration JSON pour un système de chatbot. Voici une explication des différents éléments :

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

### Comment personnaliser cette section

Pour personnaliser cette section, vous pouvez modifier les valeurs des champs selon vos besoins. Voici quelques exemples :

1. **Changer l'étiquette (tag)** :

   ```json
   "tag": "farewell"
   ```

2. **Ajouter des motifs (patterns)** :

   ```json
   "patterns": [
      "au revoir",
      "à bientôt"
   ]
   ```

3. **Ajouter des réponses (responses)** :

   ```json
   "responses": [
      "Au revoir ! Passez une bonne journée !",
      "À bientôt ! N'hésitez pas à revenir si vous avez d'autres questions."
   ]
   ```

4. **Définir un contexte spécifique** :
   ```json
   "context": ["user_logged_in"]
   ```

### Exemple personnalisé

Voici un exemple personnalisé pour un message d'adieu :

```json
{
  "tag": "farewell",
  "patterns": ["au revoir", "à bientôt"],
  "responses": [
    "Au revoir ! Passez une bonne journée !",
    "À bientôt ! N'hésitez pas à revenir si vous avez d'autres questions."
  ],
  "context": ["user_logged_in"]
}
```

Bien sûr ! Voici une explication détaillée pour aider les lecteurs à comprendre cette section du fichier

README.md

et à la personnaliser :

### Explication de la section JSON

Cette section du fichier

README.md

contient un exemple de configuration JSON pour un système de chatbot. Voici une explication des différents éléments :

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

### Comment personnaliser cette section

Pour personnaliser cette section, vous pouvez modifier les valeurs des champs selon vos besoins. Voici quelques exemples :

1. **Changer l'étiquette (tag)** :

   ```json
   "tag": "farewell"
   ```

2. **Ajouter des motifs (patterns)** :

   ```json
   "patterns": [
      "au revoir",
      "à bientôt"
   ]
   ```

3. **Ajouter des réponses (responses)** :

   ```json
   "responses": [
      "Au revoir ! Passez une bonne journée !",
      "À bientôt ! N'hésitez pas à revenir si vous avez d'autres questions."
   ]
   ```

4. **Définir un contexte spécifique** :
   ```json
   "context": ["user_logged_in"]
   ```

### Exemple personnalisé

Voici un exemple personnalisé pour un message d'adieu :

```json
{
  "tag": "farewell",
  "patterns": ["au revoir", "à bientôt"],
  "responses": [
    "Au revoir ! Passez une bonne journée !",
    "À bientôt ! N'hésitez pas à revenir si vous avez d'autres questions."
  ],
  "context": ["user_logged_in"]
}
```

- **tag** : Ce champ est une étiquette qui identifie la catégorie ou le type de message. Dans cet exemple, l'étiquette est "greetings" (salutations).

- **patterns** : Ce champ contient une liste de motifs ou de phrases que le chatbot doit reconnaître. Ici, le motif est "bonjour". Lorsque l'utilisateur tape "bonjour", le chatbot reconnaît ce motif.

- **responses** : Ce champ contient une liste de réponses que le chatbot peut donner lorsqu'il reconnaît un des motifs. Dans cet exemple, la réponse est "Bonjour ! Comment puis-je vous aider avec la configuration ou l'utilisation d'AI-licia ?".

- **context** (par défaut vide) : Ce champ est utilisé pour définir le contexte dans lequel cette réponse est valide. Dans cet exemple, le contexte est vide, ce qui signifie que cette réponse est toujours valide.

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

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteur

Développé avec ❤️ par **Ezio-33** (Samuel Verschueren)

---

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue ou à me contacter directement via [LinkedIn](www.linkedin.com/in/samuel-verschueren).
