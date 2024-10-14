import sqlite3
import uuid
from datetime import datetime

class InteractionCRUD:
    def __init__(self, db_path):
        self.db_path = db_path

    def _execute_query(self, query, params=()):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def create(self, utilisateur_id, id_Liaison_Q_R, feedback=None):
        id = str(uuid.uuid4())
        date_interaction = datetime.now().date()
        query = """INSERT INTO Interaction (id, utilisateur_id, id_Liaison_Q_R, date_interaction, feedback)
                   VALUES (?, ?, ?, ?, ?)"""
        self._execute_query(query, (id, utilisateur_id, id_Liaison_Q_R, date_interaction, feedback))
        return id

    def read(self, id):
        query = "SELECT * FROM Interaction WHERE id = ?"
        cursor = self._execute_query(query, (id,))
        return cursor.fetchone()

    def update(self, id, feedback):
        query = "UPDATE Interaction SET feedback = ? WHERE id = ?"
        cursor = self._execute_query(query, (feedback, id))
        return cursor.rowcount > 0

    def delete(self, id):
        query = "DELETE FROM Interaction WHERE id = ?"
        cursor = self._execute_query(query, (id,))
        return cursor.rowcount > 0

    def read_all_by_user(self, utilisateur_id):
        query = "SELECT * FROM Interaction WHERE utilisateur_id = ?"
        cursor = self._execute_query(query, (utilisateur_id,))
        return cursor.fetchall()