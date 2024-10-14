import sys
import os

# Ajoutez le dossier racine du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.moteur_nlp import traiter_requete

# Test des différentes requêtes
print("Test 1:")
requete1 = "Bonjour, comment ça va ?"
reponse1 = traiter_requete(requete1)
print(f"Requête: {requete1}")
print(f"Réponse: {reponse1}\n")

print("Test 2:")
requete2 = "Je voudrais poser une question sur le streaming."
reponse2 = traiter_requete(requete2)
print(f"Requête: {requete2}")
print(f"Réponse: {reponse2}\n")

print("Test 3:")
requete3 = "Merci pour votre aide, au revoir !"
reponse3 = traiter_requete(requete3)
print(f"Requête: {requete3}")
print(f"Réponse: {reponse3}\n")