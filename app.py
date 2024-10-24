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
    expected_response = request.form["expected"]
    # Ajouter la nouvelle donnée d'entraînement
    new_intent = {
        "tag": "user_feedback",
        "patterns": [conversation_memory[-1]["user"]],
        "responses": [expected_response],
        "context": [""]
    }
    intents["intents"].append(new_intent)
    with open(os.path.join(BASE_DIR, "intents.json"), "w") as file:
        json.dump(intents, file, indent=4)
    # Réentraîner le modèle avec les nouvelles données
    train_model()
    return "Feedback reçu et modèle mis à jour."

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
    prompt = f"User: {user_input}\nBot: {response}"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = nlp_model.generate(**inputs, max_length=50, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    generated_text = generated_text.replace("User:", "").replace("Bot:", "").strip()

    # Vérifier que la réponse est pertinente et ne contient pas la question initiale
    if user_input.lower() in generated_text.lower():
        generated_text = generated_text.replace(user_input, "").strip()

    if not generated_text or len(generated_text.split()) < 3 or not generated_text[-1] in ".!?":
        return response

    return generated_text

def train_model():
    # Charger les données d'entraînement
    words = []
    classes = []
    documents = []
    ignore_words = ["?", "!"]

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            w = nltk.word_tokenize(pattern)
            words.extend(w)
            documents.append((w, intent["tag"]))
            if intent["tag"] not in classes:
                classes.append(intent["tag"])

    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
    words = sorted(list(set(words)))
    classes = sorted(list(set(classes)))

    training = []
    output_empty = [0] * len(classes)

    for doc in documents:
        bag = []
        pattern_words = doc[0]
        pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    train_x = np.array([item[0] for item in training])
    train_y = np.array([item[1] for item in training])

    model = Sequential()
    model.add(Input(shape=(len(train_x[0]),)))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))

    initial_learning_rate = 0.01
    lr_schedule = ExponentialDecay(
        initial_learning_rate,
        decay_steps=100000,
        decay_rate=0.96,
        staircase=True)

    sgd = SGD(learning_rate=lr_schedule, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)
    model.save(os.path.join(BASE_DIR, "chatbot_model.keras"))

if __name__ == "__main__":
    app.run()