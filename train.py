import os
import json
import pickle
import numpy as np
import random
from datetime import datetime
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from nltk.stem import WordNetLemmatizer
import nltk

# Initialisation du lemmatizer de NLTK
lemmatizer = WordNetLemmatizer()

# Téléchargement des ressources nécessaires de NLTK
nltk.download('omw-1.4')
nltk.download("punkt")
nltk.download("wordnet")

# Définir le répertoire de base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Vérifier si le fichier de modèle existe et le renommer avec un timestamp
model_path = os.path.join(base_dir, "chatbot_model.keras")
if os.path.exists(model_path):
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Ss")
    os.rename(model_path, f"{model_path}_{timestamp}")

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
        # Tokeniser chaque mot dans la phrase
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # Ajouter au corpus
        documents.append((w, intent["tag"]))
        # Ajouter à notre liste de classes
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
    # Lemmatisation de chaque mot - création de la base de mots
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # Création du sac de mots : 1 si le mot existe dans le pattern, sinon 0
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # Sortie est un 0 pour chaque tag et 1 pour le tag actuel (pour chaque pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# Mélanger les données et les convertir en array
random.shuffle(training)

# Vérification des longueurs des sacs de mots et des sorties
for i in range(len(training)):
    if len(training[i][0]) != len(words):
        print(f"Erreur de longueur dans le sac de mots à l'index {i}")
    if len(training[i][1]) != len(classes):
        print(f"Erreur de longueur dans la sortie à l'index {i}")

# Conversion en array NumPy
train_x = np.array([item[0] for item in training])
train_y = np.array([item[1] for item in training])

# Création du modèle - 3 couches. Première couche 128 neurones, deuxième couche 64 neurones et troisième couche de sortie contient le nombre de neurones
# égal au nombre d'intentions pour prédire l'intention de sortie avec softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compilation du modèle. Définir la perte et l'optimiseur
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Entraînement et sauvegarde du modèle
hist = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)
model.save(model_path, hist)

print("Modèle créé")

# Sauvegarde des mots et des classes
# Sauvegarde des mots et des classes avec vérification de l'existence des fichiers
words_path = os.path.join(base_dir, "words.pkl")
classes_path = os.path.join(base_dir, "classes.pkl")

if os.path.exists(words_path):
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Ss")
    os.rename(words_path, f"{words_path}_{timestamp}")

if os.path.exists(classes_path):
    timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Ss")
    os.rename(classes_path, f"{classes_path}_{timestamp}")

pickle.dump(words, open(words_path, "wb"))
pickle.dump(classes, open(classes_path, "wb"))