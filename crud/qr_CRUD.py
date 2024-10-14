import sqlite3
import uuid
from datetime import datetime

class QRCRUD:
    def __init__(self, db_path):
        self.db_path = db_path
        print(f"Database path: {self.db_path}")

    def _execute_query(self, query, params=()):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def rechercher_reponse_par_mot_cle(self, mot_cle):
        query = """
            SELECT Reponse.texte
            FROM Reponse
            INNER JOIN Question ON Reponse.question_id = Question.id
            WHERE Question.texte LIKE ?
        """
        cursor = self._execute_query(query, (f"%{mot_cle}%",))
        result = cursor.fetchone()
        return result[0] if result else None

    # Méthodes pour Question
    def create_question(self, texte, categorie):
        id = str(uuid.uuid4())
        date_creation = datetime.now().date()
        query = """INSERT INTO Question (id, texte, categorie, date_creation)
                   VALUES (?, ?, ?, ?)"""
        self._execute_query(query, (id, texte, categorie, date_creation))
        return id

    def read_question(self, id):
        query = "SELECT * FROM Question WHERE id = ?"
        cursor = self._execute_query(query, (id,))
        return cursor.fetchone()

    def update_question(self, id, texte=None, categorie=None):
        updates = []
        params = []
        if texte:
            updates.append("texte = ?")
            params.append(texte)
        if categorie:
            updates.append("categorie = ?")
            params.append(categorie)
        params.append(id)
        query = f"UPDATE Question SET {', '.join(updates)} WHERE id = ?"
        cursor = self._execute_query(query, params)
        return cursor.rowcount > 0

    def delete_question(self, id):
        query = "DELETE FROM Question WHERE id = ?"
        cursor = self._execute_query(query, (id,))
        return cursor.rowcount > 0

    # Méthodes pour Réponse
    def create_reponse(self, texte, question_id):
        id = str(uuid.uuid4())
        date_creation = datetime.now().date()
        query = """INSERT INTO Reponse (id, texte, question_id, date_creation)
                   VALUES (?, ?, ?, ?)"""
        self._execute_query(query, (id, texte, question_id, date_creation))
        return id

    def read_reponse(self, id):
        query = "SELECT * FROM Reponse WHERE id = ?"
        cursor = self._execute_query(query, (id,))
        return cursor.fetchone()

    def update_reponse(self, id, texte=None):
        if texte:
            query = "UPDATE Reponse SET texte = ? WHERE id = ?"
            cursor = self._execute_query(query, (texte, id))
            return cursor.rowcount > 0
        return False

    def delete_reponse(self, id):
        query = "DELETE FROM Reponse WHERE id = ?"
        cursor = self._execute_query(query, (id,))
        return cursor.rowcount > 0

    # Méthodes pour Liaison_Q_R
    def create_liaison(self, question_id, reponse_id):
        id = str(uuid.uuid4())
        query = """INSERT INTO Liaison_Q_R (id, question_id, reponse_id)
                   VALUES (?, ?, ?)"""
        self._execute_query(query, (id, question_id, reponse_id))
        return id

    def read_liaison(self, id):
        query = "SELECT * FROM Liaison_Q_R WHERE id = ?"
        cursor = self._execute_query(query, (id,))
        return cursor.fetchone()

    def delete_liaison(self, id):
        query = "DELETE FROM Liaison_Q_R WHERE id = ?"
        cursor = self._execute_query(query, (id,))
        return cursor.rowcount > 0