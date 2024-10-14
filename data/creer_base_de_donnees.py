import os
import sqlite3

def creer_base_de_donnees():
    os.makedirs('data', exist_ok=True)
    connection = sqlite3.connect('data/database.db')
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Utilisateur (
            id TEXT PRIMARY KEY,
            nom_utilisateur VARCHAR(255),
            mot_de_passe_hash VARCHAR(255),
            Role VARCHAR(50),
            email VARCHAR(255),
            date_inscription DATE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Question (
            id TEXT PRIMARY KEY,
            texte VARCHAR(1000),
            categorie VARCHAR(100),
            date_creation DATE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reponse (
            id TEXT PRIMARY KEY,
            texte VARCHAR(2000),
            question_id TEXT,
            date_creation DATE,
            FOREIGN KEY (question_id) REFERENCES Question (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Interaction (
            id TEXT PRIMARY KEY,
            utilisateur_id TEXT,
            id_Liaison_Q_R TEXT,
            date_interaction DATE,
            feedback VARCHAR(255),
            FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur (id),
            FOREIGN KEY (id_Liaison_Q_R) REFERENCES Liaison_Q_R (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Liaison_Q_R (
            id TEXT PRIMARY KEY,
            question_id TEXT,
            reponse_id TEXT,
            FOREIGN KEY (question_id) REFERENCES Question (id),
            FOREIGN KEY (reponse_id) REFERENCES Reponse (id)
        )
    ''')
    
    connection.commit()
    connection.close()

creer_base_de_donnees()