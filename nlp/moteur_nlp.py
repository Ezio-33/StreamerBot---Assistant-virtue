import sys
import os
import spacy
import torch
from transformers import CamembertTokenizer, CamembertForCausalLM


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crud.qr_CRUD import QRCRUD

nlp = spacy.load("fr_core_news_sm")

tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
model = CamembertForCausalLM.from_pretrained("camembert-base")

db_path = '/root/StreamerBot---Assistant-virtuel-pour-Streamer-Dashboard/data/database.db'
qr_crud = QRCRUD(db_path)

def pretraiter_requete(requete):
    """Prétraite la requête en la tokenisant et en extrayant les lemmes."""
    doc = nlp(requete.lower())
    return [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

def rechercher_reponse_db(mots_cles):
    """Recherche une réponse dans la base de données en utilisant les mots-clés."""
    for mot in mots_cles:
        reponse = qr_crud.rechercher_reponse_par_mot_cle(mot)
        if reponse:
            return reponse
    return None

def generer_reponse(requete):
    """Génère une réponse en utilisant le modèle de langage pré-entraîné."""
    inputs = tokenizer.encode(requete, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(inputs, max_length=512, max_new_tokens=100, num_return_sequences=1, no_repeat_ngram_size=2)
    reponse = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reponse

def traiter_requete(requete):
    """Traite la requête de l'utilisateur et retourne une réponse appropriée."""
    mots_cles = pretraiter_requete(requete)


    reponse_db = rechercher_reponse_db(mots_cles)
    if reponse_db:
        return reponse_db

    reponse_generee = generer_reponse(requete)
    return reponse_generee


if __name__ == "__main__":
    print(traiter_requete("Comment puis-je configurer mon stream avec mon ordinateur I5?"))