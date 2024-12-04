import os
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from colorama import init, Fore, Style
import shutil
from datetime import datetime

# Initialisation de colorama pour la coloration du texte dans le terminal
init(autoreset=True)

# Création d'une instance de lemmatiseur pour normaliser les mots
lemmatizer = WordNetLemmatizer()

# Téléchargement des ressources nécessaires de NLTK pour la tokenisation et la lemmatisation
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Définition des chemins des fichiers nécessaires au projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, 'intents.json')
USER_FEEDBACK_PATH = os.path.join(BASE_DIR, 'data', 'user_feedback.json')
BACKUP_DIR = os.path.join(BASE_DIR, 'data', 'Backup', 'Intents')

# Fonction pour lemmatiser une phrase, retourne la phrase normalisée
def lemmatize_sentence(sentence):
    words = word_tokenize(sentence)  # Découpe la phrase en mots individuels
    # Applique la lemmatisation à chaque mot et retourne la phrase reconstruite
    return ' '.join([lemmatizer.lemmatize(word.lower()) for word in words])

# Fonction pour charger un fichier JSON et retourner son contenu sous forme de dictionnaire Python
def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Fonction pour sauvegarder des données dans un fichier JSON
def save_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# Fonction pour créer une copie de sauvegarde d'un fichier avec un horodatage unique
def backup_file(file_path):
    os.makedirs(BACKUP_DIR, exist_ok=True)  # Crée le répertoire de sauvegarde s'il n'existe pas
    filename = os.path.basename(file_path)
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Ss")
    backup_path = os.path.join(BACKUP_DIR, f"{filename.split('.')[0]}_{timestamp}.json")
    shutil.copy2(file_path, backup_path)  # Copie le fichier original vers l'emplacement de sauvegarde

# Fonction pour trouver des questions similaires à une question donnée en utilisant la similarité cosinus
def find_similar_questions(question, intents, threshold=0.8):
    # Récupère toutes les paires (tag, pattern) des intentions
    all_patterns = [(intent['tag'], pattern) for intent in intents['intents'] for pattern in intent['patterns']]
    vectorizer = TfidfVectorizer().fit([q for _, q in all_patterns])  # Entraîne le vecteur TF-IDF sur les patterns existants
    question_vector = vectorizer.transform([question])  # Transforme la question en vecteur TF-IDF
    all_vectors = vectorizer.transform([q for _, q in all_patterns])  # Transforme tous les patterns en vecteurs TF-IDF
    similarities = cosine_similarity(question_vector, all_vectors)[0]  # Calcule la similarité cosinus entre la question et tous les patterns
    # Filtre et retourne les questions similaires au-dessus du seuil de similarité donné
    similar = [(all_patterns[i][0], all_patterns[i][1], similarities[i]) for i in range(len(all_patterns)) if similarities[i] > threshold]
    return sorted(similar, key=lambda x: x[2], reverse=True)  # Trie par ordre décroissant de similarité

# Fonction pour mettre à jour les intentions avec les retours des utilisateurs
def update_intents_with_feedback(intents, user_feedback):
    for feedback in user_feedback:
        question = feedback['question']
        expected_response = feedback['expected_response']
        similar_questions = find_similar_questions(question, intents)
        
        if similar_questions:
            # Mise à jour d'une intention existante si une question similaire est trouvée
            tag = similar_questions[0][0]
            for intent in intents['intents']:
                if intent['tag'] == tag:
                    if question not in intent['patterns']:
                        intent['patterns'].append(question)
                    if expected_response not in intent['responses']:
                        intent['responses'].append(expected_response)
                    break
        else:
            # Création d'une nouvelle intention si aucune question similaire n'est trouvée
            new_tag = f"{question.replace(' ', '_').lower()[:30]}"
            new_intent = {
                "tag": new_tag,
                "patterns": [question],
                "responses": [expected_response]
            }
            intents['intents'].append(new_intent)
    
    return intents

def main():
    # Charger les données des intentions et des retours utilisateurs depuis les fichiers JSON respectifs
    intents = load_json_file(INTENTS_PATH)
    user_feedback = load_json_file(USER_FEEDBACK_PATH)

    # Sauvegarder une copie de sauvegarde du fichier des intentions avant modification
    backup_file(INTENTS_PATH)

    # Mettre à jour les intentions avec les retours des utilisateurs traités dans update_intents_with_feedback()
    updated_intents = update_intents_with_feedback(intents, user_feedback)

    # Sauvegarder les intentions mises à jour dans le fichier JSON original des intentions
    save_json_file(updated_intents, INTENTS_PATH)

    print(Fore.GREEN + "Le fichier d'intentions a été mis à jour avec succès.")  # Message de succès affiché en vert

    # Effacer les retours des utilisateurs après traitement pour éviter les doublons lors de prochaines mises à jour
    save_json_file([], USER_FEEDBACK_PATH)

if __name__ == "__main__":
    main()  # Exécution du programme principal si ce script est exécuté directement