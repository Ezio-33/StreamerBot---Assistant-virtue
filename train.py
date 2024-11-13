import os
import json
import pickle
import numpy as np
import random
from datetime import datetime
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.optimizers.schedules import ExponentialDecay
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.models import Sequential
from nltk.stem import WordNetLemmatizer
import nltk
import shutil

# Initialisation du lemmatizer de NLTK pour la normalisation des mots
lemmatizer = WordNetLemmatizer()

# Téléchargement des ressources nécessaires de NLTK
nltk.download('omw-1.4')
nltk.download("punkt")
nltk.download("wordnet")

# Définition des chemins de base et de sauvegarde
base_dir = os.path.dirname(os.path.abspath(__file__))
backup_dir = os.path.join(base_dir, "data", "Backup")
model_backup_dir = os.path.join(backup_dir, "Model")
intents_backup_dir = os.path.join(backup_dir, "Intents")

# Création des répertoires de sauvegarde
os.makedirs(backup_dir, exist_ok=True)
os.makedirs(model_backup_dir, exist_ok=True)
os.makedirs(intents_backup_dir, exist_ok=True)

# Sauvegarde du modèle existant avec un timestamp
model_path = os.path.join(base_dir, "chatbot_model.keras")
if os.path.exists(model_path):
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Ss")
    new_model_path = os.path.join(model_backup_dir, f"chatbot_model.keras_{timestamp}")
    os.rename(model_path, new_model_path)

# Sauvegarde du fichier intents.json avec un timestamp
intents_path = os.path.join(base_dir, "intents.json")
if os.path.exists(intents_path):
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Ss")
    new_intents_path = os.path.join(intents_backup_dir, f"intents_{timestamp}.json")
    shutil.copy2(intents_path, new_intents_path)

# Initialisation des listes pour le traitement du langage
words = []
classes = []
documents = []
ignore_words = ["?", "!"]

# Chargement du fichier JSON contenant les intentions
data_file_path = os.path.join(base_dir, "intents.json")
with open(data_file_path, 'r') as data_file:
    intents = json.load(data_file)

# Traitement des intentions pour extraire les mots et les classes
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        # Tokenisation de chaque mot dans la phrase
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # Ajout au corpus de documents
        documents.append((w, intent["tag"]))
        # Ajout du tag à la liste des classes s'il n'est pas déjà présent
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# Lemmatisation et tri des mots, suppression des doublons
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# Tri des classes
classes = sorted(list(set(classes)))

# Création des données d'entraînement
training = []
output_empty = [0] * len(classes)

for doc in documents:
    # Initialisation du sac de mots
    bag = []
    # Liste des mots tokenisés pour le pattern
    pattern_words = doc[0]
    # Lemmatisation de chaque mot
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # Création du sac de mots
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # Préparation de la sortie
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

# Mélange des données d'entraînement
random.shuffle(training)

# Vérification des longueurs des sacs de mots et des sorties
for i in range(len(training)):
    if len(training[i][0]) != len(words):
        print(f"Erreur de longueur dans le sac de mots à l'index {i}")
    if len(training[i][1]) != len(classes):
        print(f"Erreur de longueur dans la sortie à l'index {i}")

# Conversion en arrays NumPy pour l'entraînement
train_x = np.array([item[0] for item in training])
train_y = np.array([item[1] for item in training])

# Création du modèle neural
model = Sequential()
model.add(Input(shape=(len(train_x[0]),)))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Configuration du taux d'apprentissage avec décroissance exponentielle
initial_learning_rate = 0.01
lr_schedule = ExponentialDecay(
    initial_learning_rate,
    decay_steps=100000,
    decay_rate=0.96,
    staircase=True)

# Compilation du modèle
sgd = SGD(learning_rate=lr_schedule, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Entraînement du modèle
hist = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# Sauvegarde du modèle entraîné
model.save(model_path)

print("Modèle créé")

# Sauvegarde des mots et des classes
words_path = os.path.join(base_dir, "words.pkl")
classes_path = os.path.join(base_dir, "classes.pkl")

# Définition des répertoires de sauvegarde pour les mots et les classes
words_backup_dir = os.path.join(backup_dir, "words")
classes_backup_dir = os.path.join(backup_dir, "Classes")

# Création des répertoires de sauvegarde
os.makedirs(words_backup_dir, exist_ok=True)
os.makedirs(classes_backup_dir, exist_ok=True)

# Sauvegarde des fichiers existants avec un timestamp
if os.path.exists(words_path):
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Ss")
    new_words_path = os.path.join(words_backup_dir, f"words.pkl_{timestamp}")
    os.rename(words_path, new_words_path)

if os.path.exists(classes_path):
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Ss")
    new_classes_path = os.path.join(classes_backup_dir, f"classes.pkl_{timestamp}")
    os.rename(classes_path, new_classes_path)

# Sauvegarde des nouvelles listes de mots et de classes
pickle.dump(words, open(words_path, "wb"))
pickle.dump(classes, open(classes_path, "wb"))