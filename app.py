# bibliothèques
import random
import numpy as np
import pickle
import json
from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize

lemmatizer = WordNetLemmatizer()
nltk.download('punkt')

# initialisation du chat
model = load_model("/root/StreamerBot---Assistant-virtuel-pour-Streamer-Dashboard/chatbot_model.h5")
data_file = open("/root/StreamerBot---Assistant-virtuel-pour-Streamer-Dashboard/intents.json").read()
words = pickle.load(open("/root/StreamerBot---Assistant-virtuel-pour-Streamer-Dashboard/words.pkl", "rb"))
classes = pickle.load(open("/root/StreamerBot---Assistant-virtuel-pour-Streamer-Dashboard/classes.pkl", "rb"))

app = Flask(__name__)
# run_with_ngrok(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]

    # Charger et traiter le fichier JSON des intentions
    data_file = open("/root/StreamerBot---Assistant-virtuel-pour-Streamer-Dashboard/intents.json").read()
    intents = json.loads(data_file)

    # Segmenter le message en phrases distinctes
    sentences = sent_tokenize(msg)
    responses = []

    for sentence in sentences:
        if sentence.startswith("Je m'appelle"):
            name = sentence[11:].strip()
            ints = predict_class(sentence, model)
            res = getResponse(ints, intents, name)
        elif sentence.startswith("Bonjour, je m'appelle"):
            name = sentence[20:].strip()
            ints = predict_class(sentence, model)
            res = getResponse(ints, intents, name)
        else:
            ints = predict_class(sentence, model)
            res = getResponse(ints, intents)
        responses.append(res)

    # Combiner les réponses pour chaque phrase en une seule réponse
    final_response = " ".join(responses)
    return final_response

# fonctionnalités du chat
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# retourner le sac de mots sous forme de tableau : 0 ou 1 pour chaque mot dans le sac qui existe dans la phrase
def bow(sentence, words, show_details=True):
    # tokeniser le modèle
    sentence_words = clean_up_sentence(sentence)
    # sac de mots - matrice de N mots, matrice de vocabulaire
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assigner 1 si le mot actuel est dans la position du vocabulaire
                bag[i] = 1
                if show_details:
                    print("trouvé dans le sac : %s" % w)
    return np.array(bag)

def predict_class(sentence, model):
    # filtrer les prédictions en dessous d'un seuil
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # trier par force de probabilité
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json, name=None):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            if name:
                result = result.replace("{n}", name)
            break
    return result

if __name__ == "__main__":
    app.run()