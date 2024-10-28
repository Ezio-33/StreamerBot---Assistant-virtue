# StreamerBot - Assistant virtuel pour Streamer Dashboard

## Description

**StreamerBot** est un assistant virtuel intelligent fonctionnant localement, conçu pour optimiser l'expérience des utilisateurs du site [Streamer Dashboard](https://streamer-dashboard.ailicia.live/signup?via=ref-ezio_33). Ce chatbot vise à fournir une interaction fluide et naturelle, sans besoin de connexion internet, et s'exécute sur des machines modestes (processeur Intel de 8ème génération, 8 Go de RAM DDR4, sans carte graphique).

## Fonctionnalités

- 💬 **Chatbot local** : Offre des réponses intelligentes en fonction des interactions avec les utilisateurs, sans connexion à Internet.
- 🚀 **Optimisation de l'expérience utilisateur** : Prévus pour s'intégrer dans le futur au site Streamer Dashboard pour améliorer la fluidité de navigation et l'accès aux informations.
- ⚙️ **Personnalisable** : Les réponses et le comportement du chatbot peuvent être ajustés pour mieux correspondre aux besoins spécifiques des streamers.
- 🖥️ **Performance optimisée** : Fonctionne sur des configurations matérielles modérées sans nécessiter de GPU.

## Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/Ezio-33/StreamerBot---Assistant-virtuel-pour-Streamer-Dashboard.git
   cd StreamerBot---Assistant-virtuel-pour-Streamer-Dashboard
   git checkout Dev
   ```
2. **Installer les dépendances** :
   Utilisez `pip` pour installer les dépendances nécessaires :
   ```bash
   pip install -r requirements.txt
   ```
3. **Configuration** :
   - Ajustez les paramètres dans le fichier de configuration `.env` pour adapter le bot à vos besoins.
   - L'installation ne nécessite pas de connexion Internet une fois les dépendances installées.

## Configuration

**Données d'entraînement** :

- Le bot utilise des données locales pour ajuster ses réponses. Pour personnaliser les interactions, modifiez le fichier `intents.json`.

## Prérequis

- **Matériel** :
  - Processeur Intel 8ème génération
  - 8 Go de RAM DDR4
  - Pas de carte graphique nécessaire
- **Logiciel** :
  - Python 3.8 ou supérieur
  - OS : Windows/Linux/Mac

## Technologies utilisées

- **Langage** : Python
- **Bibliothèques IA** : `transformers`, `torch`, `tensorflow` (pour le modèle de traitement du langage naturel)
- **Gestion des dialogues** : `nltk` pour les interactions conversationnelles

## Contribuer

Les contributions sont les bienvenues ! Pour proposer une nouvelle fonctionnalité ou rapporter un bug :

1. Fork le projet.
2. Crée une branche (`feature/nom-de-la-feature`).
3. Committez vos modifications (`git commit -m 'Ajouter nouvelle fonctionnalité'`).
4. Pushez vers la branche (`git push origin feature/nom-de-la-feature`).
5. Ouvrez une Pull Request.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Crédits

Développé avec ❤️ par **Ezio-33** pour améliorer l'expérience des streamers et rendre leur gestion de contenu plus fluide et agréable.
