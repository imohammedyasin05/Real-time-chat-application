"""
Database module for Real-Time Chat Application
"""

import sqlite3
import os
from datetime import datetime


class Database:
    
    def __init__(self, db_path='chat_history.db'):
        self.db_path = db_path
        self.conn = None
        self.create_connection()
        self.create_tables()
        
    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            print(f"[DB] Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"[DB] Error connecting to database: {e}")
            
    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    logout_time TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            print("[DB] Database tables created successfully")
            
        except sqlite3.Error as e:
            print(f"[DB] Error creating tables: {e}")
            
    def save_message(self, username, message, timestamp=None):
        try:
            if timestamp is None:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            cursor = self.conn.cursor()
            cursor.execute(
                'INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)',
                (username, message, timestamp)
            )
            self.conn.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"[DB] Error saving message: {e}")
            return False
            
    def get_messages(self, limit=100, offset=0):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                'SELECT username, message, timestamp FROM messages ORDER BY id DESC LIMIT ? OFFSET ?',
                (limit, offset)
            )
            rows = cursor.fetchall()
            return list(reversed([{'username': row[0], 'message': row[1], 'timestamp': row[2]} for row in rows]))
            
        except sqlite3.Error as e:
            print(f"[DB] Error retrieving messages: {e}")
            return []
            
    def search_messages(self, search_term):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                'SELECT username, message, timestamp FROM messages WHERE message LIKE ? OR username LIKE ? ORDER BY id DESC',
                (f'%{search_term}%', f'%{search_term}%')
            )
            rows = cursor.fetchall()
            return [{'username': row[0], 'message': row[1], 'timestamp': row[2]} for row in rows]
            
        except sqlite3.Error as e:
            print(f"[DB] Error searching messages: {e}")
            return []
            
    def get_user_messages(self, username):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                'SELECT username, message, timestamp FROM messages WHERE username = ? ORDER BY id DESC',
                (username,)
            )
            rows = cursor.fetchall()
            return [{'username': row[0], 'message': row[1], 'timestamp': row[2]} for row in rows]
            
        except sqlite3.Error as e:
            print(f"[DB] Error retrieving user messages: {e}")
            return []
            
    def add_user(self, username):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                'INSERT OR IGNORE INTO users (username) VALUES (?)',
                (username,)
            )
            self.conn.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"[DB] Error adding user: {e}")
            return False
            
    def update_user_logout(self, username):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                'UPDATE users SET logout_time = CURRENT_TIMESTAMP WHERE username = ? AND logout_time IS NULL',
                (username,)
            )
            self.conn.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"[DB] Error updating user logout: {e}")
            return False
            
    def get_online_users(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT DISTINCT username FROM messages ORDER BY timestamp DESC')
            rows = cursor.fetchall()
            return [row[0] for row in rows]
            
        except sqlite3.Error as e:
            print(f"[DB] Error getting online users: {e}")
            return []
            
    def clear_history(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM messages')
            self.conn.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"[DB] Error clearing history: {e}")
            return False
            
    def close(self):
        if self.conn:
            self.conn.close()
            print("[DB] Database connection closed")


if __name__ == "__main__":
    db = Database()
    db.save_message("TestUser", "Hello, this is a test message!")
    messages = db.get_messages()
    print("\nAll messages:")
    for msg in messages:
        print(f"  [{msg['timestamp']}] {msg['username']}: {msg['message']}")
    db.close()
