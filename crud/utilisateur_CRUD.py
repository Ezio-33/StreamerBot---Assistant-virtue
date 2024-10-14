import sqlite3
import uuid
from datetime import datetime

class UtilisateurCRUD:
    def __init__(self, db_path):
        self.db_path = db_path

    def _execute_query(self, query, params=()):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def create(self, nom_utilisateur, mot_de_passe_hash, role, email):
        id = str(uuid.uuid4())
        date_inscription = datetime.now().date()
        query = """INSERT INTO Utilisateur (id, nom_utilisateur, mot_de_passe_hash, Role, email, date_inscription)
                   VALUES (?, ?, ?, ?, ?, ?)"""
        self._execute_query(query, (id, nom_utilisateur, mot_de_passe_hash, role, email, date_inscription))
        return id

    def read(self, id):
        query = "SELECT * FROM Utilisateur WHERE id = ?"
        cursor = self._execute_query(query, (id,))
        return cursor.fetchone()

    def update(self, id, nom_utilisateur=None, mot_de_passe_hash=None, role=None, email=None):
        updates = []
        params = []
        if nom_utilisateur:
            updates.append("nom_utilisateur = ?")
            params.append(nom_utilisateur)
        if mot_de_passe_hash:
            updates.append("mot_de_passe_hash = ?")
            params.append(mot_de_passe_hash)
        if role:
            updates.append("Role = ?")
            params.append(role)
        if email:
            updates.append("email = ?")
            params.append(email)
        params.append(id)
        query = f"UPDATE Utilisateur SET {', '.join(updates)} WHERE id = ?"
        cursor = self._execute_query(query, params)
        return cursor.rowcount > 0

    def delete(self, id):
        query = "DELETE FROM Utilisateur WHERE id = ?"
        cursor = self._execute_query(query, (id,))
        return cursor.rowcount > 0