import os
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from colorama import init, Fore, Style

# Initialiser colorama pour les couleurs dans le terminal
init(autoreset=True)

# Initialisation du lemmatizer de NLTK
lemmatizer = WordNetLemmatizer()

# Téléchargement des ressources nécessaires de NLTK
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Fonction pour lemmatiser une phrase
def lemmatize_sentence(sentence):
    words = word_tokenize(sentence)
    lemmatized_words = [lemmatizer.lemmatize(word.lower()) for word in words]
    return ' '.join(lemmatized_words)

# Définir le répertoire de base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Charger le fichier intents.json
intents_path = os.path.join(base_dir, 'intents.json')
with open(intents_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Vérifier si le fichier de configuration existe
config_path = os.path.join(base_dir, 'config.json')
if os.path.exists(config_path):
    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
        ignored_choices_path = config['ignored_choices_path']
else:
    # Demander à l'utilisateur où installer le fichier ignored_choices.json
    ignored_choices_path = input(Fore.YELLOW + "Entrez le chemin où vous souhaitez installer le fichier ignored_choices.json : " + Style.RESET_ALL)

# S'assurer que le chemin se termine par 'ignored_choices.json'
if not ignored_choices_path.endswith('ignored_choices.json'):
    ignored_choices_path = os.path.join(ignored_choices_path, 'ignored_choices.json')

# Créer le répertoire parent s'il n'existe pas
os.makedirs(os.path.dirname(ignored_choices_path), exist_ok=True)

# Si le fichier de configuration n'existait pas, le créer maintenant
if not os.path.exists(config_path):
    config = {'ignored_choices_path': ignored_choices_path}
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=4)

# Charger ou créer le fichier des choix ignorés
if os.path.exists(ignored_choices_path):
    with open(ignored_choices_path, 'r', encoding='utf-8') as file:
        ignored_choices = json.load(file)
else:
    ignored_choices = {"questions": [], "responses": []}
    with open(ignored_choices_path, 'w', encoding='utf-8') as file:
        json.dump(ignored_choices, file, ensure_ascii=False, indent=4)

# Extraire les questions et réponses
questions = []
responses = []
for intent in data['intents']:
    for pattern in intent['patterns']:
        questions.append((intent['tag'], pattern))
    for response in intent['responses']:
        responses.append((intent['tag'], response))

# Lemmatiser les questions et réponses
lemmatized_questions = [(tag, lemmatize_sentence(question)) for tag, question in questions]
lemmatized_responses = [(tag, lemmatize_sentence(response)) for tag, response in responses]

# Fonction pour détecter les doublons entre les tags
def find_duplicates_between_tags(items, threshold=0.8):
    duplicates = []
    vectorizer = TfidfVectorizer().fit_transform([item[1] for item in items])
    vectors = vectorizer.toarray()
    cosine_matrix = cosine_similarity(vectors)
    for i in range(len(cosine_matrix)):
        for j in range(i + 1, len(cosine_matrix)):
            if cosine_matrix[i][j] > threshold and items[i][0] != items[j][0]:
                duplicates.append((items[i], items[j], cosine_matrix[i][j]))
    return duplicates

# Fonction pour calculer la similarité moyenne entre un item et un tag
def calculate_average_similarity(item, tag):
    tag_items = [pattern for intent in data['intents'] if intent['tag'] == tag for pattern in intent['patterns']]
    tag_items += [response for intent in data['intents'] if intent['tag'] == tag for response in intent['responses']]
    
    if not tag_items:
        return 0  # Retourner 0 si le tag n'a pas d'items

    # Utiliser le même vectorizer pour l'item et les tag_items
    vectorizer = TfidfVectorizer()
    all_items = [item] + tag_items
    vectors = vectorizer.fit_transform(all_items)
    
    item_vector = vectors[0]
    tag_vectors = vectors[1:]
    
    similarities = cosine_similarity(item_vector, tag_vectors)
    return similarities.mean()

# Fonction pour proposer une action et choisir le tag à conserver
def propose_action(item1, item2, similarity):
    sim1 = calculate_average_similarity(item1[1], item1[0])
    sim2 = calculate_average_similarity(item2[1], item2[0])
    
    if sim1 == sim2:
        suggested_tag = item1[0]  # ou item2[0], peu importe dans ce cas
    else:
        suggested_tag = item1[0] if sim1 > sim2 else item2[0]
    
    if similarity > 0.95:
        return f"Supprimer l'item du tag '{item1[0]}' ou du tag '{item2[0]}' (suggestion : conserver '{suggested_tag}')", suggested_tag
    elif similarity > 0.9:
        return f"Fusionner manuellement (suggestion : fusionner dans '{suggested_tag}')", suggested_tag
    else:
        return f"Vérifier manuellement (suggestion : conserver '{suggested_tag}')", suggested_tag

# Fonction pour supprimer un item (question ou réponse) d'un tag
def remove_item_from_tag(tag, item_to_remove, item_type):
    for intent in data['intents']:
        if intent['tag'] == tag:
            if item_type == 'questions':
                intent['patterns'] = [pattern for pattern in intent['patterns'] if pattern.strip().lower() != item_to_remove.strip().lower()]
            elif item_type == 'responses':
                intent['responses'] = [response for response in intent['responses'] if response.strip().lower() != item_to_remove.strip().lower()]
            break

    save_intents()
    print(Fore.GREEN + f"L'item '{item_to_remove}' a été supprimé du tag '{tag}'.")

def save_intents():
    with open(intents_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# Fonction pour fusionner deux tags
def merge_tags(tag1, tag2):
    tag2_intent = None
    for intent in data['intents']:
        if intent['tag'] == tag2:
            tag2_intent = intent
            break
    
    if tag2_intent is None:
        print(f"Le tag '{tag2}' n'a pas été trouvé. Fusion annulée.")
        return False

    for intent in data['intents']:
        if intent['tag'] == tag1:
            # Supprimer les doublons lors de la fusion
            intent['patterns'] = list(set(intent['patterns'] + tag2_intent['patterns']))
            intent['responses'] = list(set(intent['responses'] + tag2_intent['responses']))
            data['intents'].remove(tag2_intent)
            break

    save_intents()
    return True

# Mode de suppression automatique par défaut
# auto_remove = True

# Décommentez la ligne suivante pour passer en mode interactif
auto_remove = False

# Trouver les doublons dans les questions et réponses entre les tags
duplicate_questions = find_duplicates_between_tags(lemmatized_questions)
duplicate_responses = find_duplicates_between_tags(lemmatized_responses)

# Fonction pour afficher le contenu d'un tag
def display_tag_content(tag):
    for intent in data['intents']:
        if intent['tag'] == tag:
            print(Fore.GREEN + f"\nContenu du tag '{tag}':")
            print(Fore.CYAN + "Questions:")
            for pattern in intent['patterns']:
                print(Fore.CYAN + f"- {pattern}")
            print(Fore.MAGENTA + "Réponses:")
            for response in intent['responses']:
                print(Fore.MAGENTA + f"- {response}")
            break

# Fonction pour sauvegarder les choix ignorés
def save_ignored_choices():
    with open(ignored_choices_path, 'w', encoding='utf-8') as file:
        json.dump(ignored_choices, file, ensure_ascii=False, indent=2)

# Fonction pour vérifier si un doublon a déjà été ignoré
def is_already_ignored(item1, item2, item_type):
    for ignored_pair in ignored_choices[item_type]:
        if (item1[0] == ignored_pair[0] and item1[1] == ignored_pair[1] and item2[0] == ignored_pair[2] and item2[1] == ignored_pair[3]) or \
           (item2[0] == ignored_pair[0] and item2[1] == ignored_pair[1] and item1[0] == ignored_pair[2] and item1[1] == ignored_pair[3]):
            return True
    return False

# Fonction pour traiter les doublons
def process_duplicates(duplicates, item_type):
    print(Fore.YELLOW + f"\n{item_type} en doublon entre les tags :")
    i = 0
    while i < len(duplicates):
        item1, item2, similarity = duplicates[i]
        
        # Vérifier si le doublon a déjà été ignoré
        if is_already_ignored(item1, item2, item_type):
            print(Fore.YELLOW + f"Doublon ignoré précédemment : {item1[1]} - {item2[1]}")
            i += 1
            continue

        print(Fore.BLUE + f"\nTag 1: {item1[0]}")
        display_tag_content(item1[0])
        print(Fore.BLUE + f"\nTag 2: {item2[0]}")
        display_tag_content(item2[0])
        print(Fore.RED + f"\n{item_type} en doublon:")
        print(Fore.RED + f"Tag 1: {item1[0]} - {item1[1]}")
        print(Fore.RED + f"Tag 2: {item2[0]} - {item2[1]}")
        print(Fore.WHITE + f"Similarité: {similarity:.2f}")
        action, suggested_tag = propose_action(item1, item2, similarity)
        print(Fore.WHITE + f"Action proposée: {action}")

        if auto_remove:
            if suggested_tag == item1[0]:
                remove_item_from_tag(item2[0], item2[1], item_type)
                print(Fore.GREEN + f"L'item '{item2[1]}' a été supprimé automatiquement du tag '{item2[0]}'.")
            else:
                remove_item_from_tag(item1[0], item1[1], item_type)
                print(Fore.GREEN + f"L'item '{item1[1]}' a été supprimé automatiquement du tag '{item1[0]}'.")
        
            duplicates.pop(i)  # Supprimer l'élément traité de la liste des doublons
        
        else:
            print(Fore.YELLOW + "\nQue voulez-vous faire ?")
            print(Fore.CYAN + f"1. Supprimer l'item du tag '{item1[0]}'{' (suggéré)' if suggested_tag != item1[0] else ''}")
            print(Fore.CYAN + f"2. Supprimer l'item du tag '{item2[0]}'{' (suggéré)' if suggested_tag != item2[0] else ''}")
            print(Fore.CYAN + f"3. Fusionner manuellement les tags")
            print(Fore.CYAN + "4. Ignorer et passer au suivant")
            print(Fore.CYAN + "5. Ignorer définitivement")            
            
            user_action = input(Fore.YELLOW + "Entrez votre choix (1/2/3/4/5) : " + Style.RESET_ALL)
            
            if user_action == '1':
                remove_item_from_tag(item1[0], item1[1], item_type)
                print(Fore.GREEN + f"L'item '{item1[1]}' a été supprimé du tag '{item1[0]}'.")
                save_ignored_choices()
                duplicates.pop(i)  # Supprimer l'élément traité de la liste des doublons
            
            elif user_action == '2':
                remove_item_from_tag(item2[0], item2[1], item_type)
                print(Fore.GREEN + f"L'item '{item2[1]}' a été supprimé du tag '{item2[0]}'.")
                save_ignored_choices()
                duplicates.pop(i)  # Supprimer l'élément traité de la liste des doublons
            
            elif user_action == '3':
                print(Fore.YELLOW + f"Dans quel tag voulez-vous fusionner les items ?")
                print(Fore.CYAN + f"1. {item1[0]}{' (suggéré)' if suggested_tag == item1[0] else ''}")
                print(Fore.CYAN + f"2. {item2[0]}{' (suggéré)' if suggested_tag == item2[0] else ''}")
                
                merge_choice = input(Fore.YELLOW + "Entrez votre choix (1/2) : " + Style.RESET_ALL)
                
                if merge_choice == '1':
                    if merge_tags(item1[0], item2[0]):
                        print(Fore.GREEN + f"Les items du tag '{item2[0]}' ont été fusionnés dans le tag '{item1[0]}'.")
                        duplicates.pop(i)  # Supprimer l'élément traité de la liste des doublons
                
                elif merge_choice == '2':
                    if merge_tags(item2[0], item1[0]):
                        print(Fore.GREEN + f"Les items du tag '{item1[0]}' ont été fusionnés dans le tag '{item2[0]}'.")
                        duplicates.pop(i)  # Supprimer l'élément traité de la liste des doublons

                else:
                    print(Fore.RED + "Choix invalide. Fusion annulée.")

                save_ignored_choices()

            elif user_action == '4':
                print(Fore.YELLOW + "Doublon ignoré pour cette session.")
                i += 1  # Passer au doublon suivant

            elif user_action == '5':
                if not is_already_ignored(item1, item2, item_type):
                    ignored_choices[item_type].append([item1[0], item1[1], item2[0], item2[1]])
                    print(Fore.GREEN + "Ce doublon sera ignoré dans les futures exécutions.")
                    save_ignored_choices()
                    duplicates.pop(i)  # Supprimer l'élément traité de la liste des doublons
                else:
                    print(Fore.YELLOW + "Ce doublon est déjà ignoré.")
                    i += 1
            else:
                print(Fore.YELLOW + "Action invalide. Veuillez choisir une option valide.")
                    # Ne pas incrémenter i ici pour permettre à l'utilisateur de réessayer

        print()

# Traiter les doublons
process_duplicates(duplicate_questions, "questions")
process_duplicates(duplicate_responses, "responses")

print(Fore.GREEN + "Traitement des doublons terminé.")