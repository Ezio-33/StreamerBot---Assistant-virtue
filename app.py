import os
import random
import numpy as np
import pickle
import json
from flask import Flask, render_template, request
import nltk
from tensorflow.keras.models import load_model
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from transformers import CamembertTokenizer, CamembertForCausalLM
import subprocess
from datetime import datetime

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
nlp_model = CamembertForCausalLM.from_pretrained("camembert-base")

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
    save_feedback(question, expected_response)
    return "Feedback reçu et sauvegardé."

@app.route("/quit", methods=["POST"])
def quit():
    # Réentraîner le modèle avec les nouvelles données
    subprocess.Popen(["python", os.path.join(BASE_DIR, "update_model.py")])
    subprocess.Popen(["python", os.path.join(BASE_DIR, "train.py")])
    return "Modèle mis à jour et application fermée."

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
    prompt = f"Bot: {response}"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = nlp_model.generate(**inputs, max_length=100, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    generated_text = generated_text.replace("Bot:", "").strip()

    if not generated_text or len(generated_text.split()) < 3 or not generated_text[-1] in ".!?":
        return response
    return generated_text

if __name__ == "__main__":
    app.run()
