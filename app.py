import os
import random
import numpy as np
import pickle
import json
import nltk
import torch
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from transformers import CamembertTokenizer, CamembertForCausalLM
from datetime import datetime
from threading import Thread
import subprocess

lemmatizer = WordNetLemmatizer()
nltk.download('punkt', quiet=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Charger le modèle entraîné et les fichiers nécessaires
model = load_model(os.path.join(BASE_DIR, "chatbot_model.keras"))
with open(os.path.join(BASE_DIR, "intents.json")) as file:
    intents = json.load(file)
words = pickle.load(open(os.path.join(BASE_DIR, "words.pkl"), "rb"))
classes = pickle.load(open(os.path.join(BASE_DIR, "classes.pkl"), "rb"))

# Initialiser le tokenizer et le modèle de langage avancé
tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
nlp_model = CamembertForCausalLM.from_pretrained("camembert-base", is_decoder=True)
nlp_model.resize_token_embeddings(len(tokenizer))
nlp_model.eval()  # Mettre le modèle en mode évaluation

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mémoire de la conversation
conversation_memory = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    sentences = sent_tokenize(msg)
    responses = []

    for sentence in sentences:
        if sentence.lower().startswith(("je m'appelle", "bonjour, je m'appelle")):
            name = sentence.split("appelle", 1)[1].strip()
            ints = predict_class(sentence)
            res = get_response(ints, name)
        else:
            ints = predict_class(sentence)
            res = get_response(ints) if ints else "Désolé, je ne vous ai pas compris."

        res = generate_contextual_response(res, sentence)
        responses.append(res)

    conversation_memory.append({"user": msg, "bot": responses})
    return " ".join(responses)

@app.route("/feedback", methods=["POST"])
def feedback():
    question = request.form["question"]
    expected_response = request.form["expected"]
    Thread(target=save_feedback, args=(question, expected_response)).start()
    return "Feedback reçu et sauvegardé."

@app.route("/quit", methods=["POST"])
def quit():
    Thread(target=update_and_quit).start()
    return "Modèle mis à jour et application fermée."

def update_and_quit():
    feedback_path = os.path.join(BASE_DIR, "data", "user_feedback.json")
    if os.path.exists(feedback_path):
        with open(feedback_path, 'r', encoding='utf-8') as file:
            feedback = json.load(file)
        if feedback:
            subprocess.run(["python", os.path.join(BASE_DIR, "update_model.py")])
            subprocess.run(["python", os.path.join(BASE_DIR, "train.py")])
    os._exit(0)

def save_feedback(question, expected_response):
    feedback_path = os.path.join(BASE_DIR, "data", "user_feedback.json")
    os.makedirs(os.path.dirname(feedback_path), exist_ok=True)
    
    if os.path.exists(feedback_path):
        with open(feedback_path, 'r', encoding='utf-8') as file:
            feedback = json.load(file)
    else:
        feedback = []

    feedback.append({"question": question, "expected_response": expected_response})

    with open(feedback_path, 'w', encoding='utf-8') as file:
        json.dump(feedback, file, ensure_ascii=False, indent=2)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    return [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print(f"trouvé dans le sac : {w}")
    return np.array(bag)

def predict_class(sentence):
    p = bow(sentence, words, show_details=False)
    if len(p) != len(words):
        p = np.pad(p, (0, len(words) - len(p)), mode='constant')
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]

def get_response(ints, name=None):
    if not ints:
        return "Désolé, je ne vous ai pas compris."
    tag = ints[0]["intent"]
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            response = random.choice(intent["responses"])
            return response.replace("{n}", name) if name else response
    return "Désolé, je ne vous ai pas compris."

def generate_contextual_response(response, user_input):
    try:
        prompt = f"Utilisateur: {user_input}\nBot: {response}"
        with torch.no_grad():
            inputs = tokenizer(prompt, return_tensors="pt", padding=True)
            outputs = nlp_model.generate(
                inputs.input_ids,
                attention_mask=inputs.attention_mask,
                max_length=150,
                max_new_tokens=80,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                early_stopping=True,
                num_beams=1,  # Réduit de 5 à 1 pour accélérer le temps de reponse
            )
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        generated_text = generated_text.split("Bot:")[-1].strip()
        if not generated_text or len(generated_text.split()) < 3 or generated_text[-1] not in ".!?":
            return response
        return generated_text
    except Exception as e:
        print(f"Erreur dans generate_contextual_response: {e}")
        return response

if __name__ == "__main__":
    app.run()