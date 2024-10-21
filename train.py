import random
import os
from datetime import datetime
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
print("Importations réussies")
import numpy as np
import pickle
import json
import nltk
from nltk.stem import WordNetLemmatizer

import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# Initialisation du lemmatizer de NLTK
lemmatizer = WordNetLemmatizer()

# Téléchargement des ressources nécessaires de NLTK
nltk.download('omw-1.4')
nltk.download("punkt")
nltk.download("wordnet")
nltk.download('punkt_tab')

# Définir le répertoire de base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Vérifier si le fichier de modèle existe et le renommer avec un timestamp
model_path = os.path.join(base_dir, "chatbot_model.keras")
if os.path.exists(model_path):
    stat = os.stat(model_path)
    try:
        creation_time = datetime.fromtimestamp(stat.st_birthtime).strftime('%d-%m-%Y_%Hh%Mmin%Ss')
    except AttributeError:
        # st_birthtime n'est pas disponible, utiliser st_ctime à la place
        creation_time = datetime.fromtimestamp(stat.st_ctime).strftime('%d-%m-%Y_%Hh%Mmin%Ss')
    new_model_path = os.path.join(base_dir, f"chatbot_model_{creation_time}.keras")
    os.rename(model_path, new_model_path)
    print(f"\033[92m\033[1mL'ancien modèle {os.path.basename(model_path)} a été renommé en {os.path.basename(new_model_path)}\033[0m")

# Initialisation des listes pour les mots, classes et documents
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
        # Tokenisation des mots dans chaque pattern
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # Ajout des documents (pattern, tag)
        documents.append((w, intent["tag"]))
        # Ajout des classes (tags) uniques
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# Lemmatisation et tri des mots, suppression des doublons
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# Tri des classes
classes = sorted(list(set(classes)))

# Affichage des informations sur les documents, classes et mots
print(len(documents), "documents")
print(len(classes), "classes", classes)
print(len(words), "mots lemmatisés uniques", words)

# Sauvegarde des mots et des classes dans des fichiers pickle
pickle.dump(words, open(os.path.join(base_dir, "words.pkl"), "wb"))
pickle.dump(classes, open(os.path.join(base_dir, "classes.pkl"), "wb"))

# Initialisation des données d'entraînement
training = []
output_empty = [0] * len(classes)

# Création des sacs de mots pour chaque document
for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

# Mélange des données d'entraînement
random.shuffle(training)

# Séparation des caractéristiques (X) et des étiquettes (Y)
train_x = [item[0] for item in training]
train_y = [item[1] for item in training]

# Conversion en tableaux NumPy
train_x = np.array(train_x)
train_y = np.array(train_y)
print("Données d'entraînement créées")

# Création du modèle de réseau de neurones
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))
model.summary()

# Compilation du modèle avec l'optimiseur SGD
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

# Entraînement du modèle
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

# Sauvegarde du modèle entraîné
model.save(os.path.join(base_dir, "chatbot_model.keras"))
print(f"\033[92m\033[1mL'ancien modèle {os.path.basename(new_model_path)} a été renommé en {os.path.basename(new_model_path)}\033[0m")
date_du_jour = datetime.now().strftime('%d-%m-%Y_%Hh%Mmin%Ss')
print(f"\033[92m\033[1mNouveau modèle créé le {date_du_jour}\033[0m")