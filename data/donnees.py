import sqlite3
import uuid
from datetime import datetime, timedelta

def generer_uuid():
    return str(uuid.uuid4())

def inserer_donnees():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()


    utilisateurs = [
        (generer_uuid(), "admin", "hashed_password_admin", "admin", "admin@example.com", datetime.now().date()),
        (generer_uuid(), "client", "hashed_password_client", "client", "client@example.com", datetime.now().date())
    ]
    cursor.executemany("""
        INSERT INTO Utilisateur (id, nom_utilisateur, mot_de_passe_hash, Role, email, date_inscription)
        VALUES (?, ?, ?, ?, ?, ?)
    """, utilisateurs)

    questions_reponses = [
        ("Comment configurer AI_Licia pour mon stream Twitch ?", "Configuration", 
         "Pour configurer AI_Licia, rendez-vous sur le site officiel getailicia.com, connectez-vous à votre compte Twitch, puis suivez les instructions pour lier AI_Licia à votre chaîne."),
        ("Quelles sont les principales fonctionnalités d'AI_Licia ?", "Fonctionnalités", 
         "AI_Licia offre plusieurs fonctionnalités clés : animation du chat, réponse aux questions des viewers, création de mini-jeux, et personnalisation des interactions selon vos préférences."),
        ("Comment personnaliser le comportement d'AI_Licia ?", "Personnalisation", 
         "Vous pouvez personnaliser AI_Licia via le dashboard sur getailicia.com. Ajustez son ton, ses réponses, et ses interactions pour qu'elle corresponde à l'ambiance de votre stream.")
    ]

    for question, categorie, reponse in questions_reponses:
        question_id = generer_uuid()
        reponse_id = generer_uuid()
        liaison_id = generer_uuid()
        date_creation = datetime.now().date()


        cursor.execute("""
            INSERT INTO Question (id, texte, categorie, date_creation)
            VALUES (?, ?, ?, ?)
        """, (question_id, question, categorie, date_creation))


        cursor.execute("""
            INSERT INTO Reponse (id, texte, question_id, date_creation)
            VALUES (?, ?, ?, ?)
        """, (reponse_id, reponse, question_id, date_creation))


        cursor.execute("""
            INSERT INTO Liaison_Q_R (id, question_id, reponse_id)
            VALUES (?, ?, ?)
        """, (liaison_id, question_id, reponse_id))

    conn.commit()
    conn.close()

    print("Données insérées avec succès !")

if __name__ == "__main__":
    inserer_donnees()