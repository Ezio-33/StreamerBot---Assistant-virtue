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

# Initialisation
init(autoreset=True)
lemmatizer = WordNetLemmatizer()
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Chemins des fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, 'intents.json')
USER_FEEDBACK_PATH = os.path.join(BASE_DIR, 'data', 'user_feedback.json')
BACKUP_DIR = os.path.join(BASE_DIR, 'data', 'Backup', 'Instants')

def lemmatize_sentence(sentence):
    words = word_tokenize(sentence)
    return ' '.join([lemmatizer.lemmatize(word.lower()) for word in words])

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def backup_file(file_path):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    filename = os.path.basename(file_path)
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Ss")
    backup_path = os.path.join(BACKUP_DIR, f"{filename.split('.')[0]}_{timestamp}.json")
    shutil.copy2(file_path, backup_path)

def find_similar_questions(question, intents, threshold=0.8):
    all_patterns = [(intent['tag'], pattern) for intent in intents['intents'] for pattern in intent['patterns']]
    vectorizer = TfidfVectorizer().fit([q for _, q in all_patterns])
    question_vector = vectorizer.transform([question])
    all_vectors = vectorizer.transform([q for _, q in all_patterns])
    similarities = cosine_similarity(question_vector, all_vectors)[0]
    similar = [(all_patterns[i][0], all_patterns[i][1], similarities[i]) for i in range(len(all_patterns)) if similarities[i] > threshold]
    return sorted(similar, key=lambda x: x[2], reverse=True)

def update_intents_with_feedback(intents, user_feedback):
    for feedback in user_feedback:
        question = feedback['question']
        expected_response = feedback['expected_response']
        similar_questions = find_similar_questions(question, intents)
        
        if similar_questions:
            # Update existing intent
            tag = similar_questions[0][0]
            for intent in intents['intents']:
                if intent['tag'] == tag:
                    if question not in intent['patterns']:
                        intent['patterns'].append(question)
                    if expected_response not in intent['responses']:
                        intent['responses'].append(expected_response)
                    break
        else:
            # Create new intent
            new_tag = f"{question.replace(' ', '_').lower()[:30]}"
            new_intent = {
                "tag": new_tag,
                "patterns": [question],
                "responses": [expected_response]
            }
            intents['intents'].append(new_intent)
    
    return intents

def main():
    # Load data
    intents = load_json_file(INTENTS_PATH)
    user_feedback = load_json_file(USER_FEEDBACK_PATH)

    # Backup original intents file
    backup_file(INTENTS_PATH)

    # Update intents with user feedback
    updated_intents = update_intents_with_feedback(intents, user_feedback)

    # Save updated intents
    save_json_file(updated_intents, INTENTS_PATH)

    print(Fore.GREEN + "Intents file updated successfully.")

    # Clear user feedback after processing
    save_json_file([], USER_FEEDBACK_PATH)

if __name__ == "__main__":
    main()