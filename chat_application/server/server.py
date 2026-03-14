"""
Server module for Real-Time Chat Application
"""

import socket
import threading
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.database import Database


class ChatServer:
    
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}
        self.running = False
        self.db = Database()
        
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"[SERVER] Chat server started on {self.host}:{self.port}")
        
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"[SERVER] New connection from {client_address}")
                
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,),
                    daemon=True
                )
                client_thread.start()
            except Exception as e:
                print(f"[SERVER] Error accepting connection: {e}")
                break
                
    def handle_client(self, client_socket):
        username = None
        
        try:
            username_data = client_socket.recv(1024).decode('utf-8')
            if not username_data:
                return
                
            username = username_data
            self.clients[client_socket] = username
            
            print(f"[SERVER] {username} joined the chat")
            
            self.broadcast(f"📢 {username} has joined the chat!", exclude=client_socket)
            
            self.send_chat_history(client_socket)
            
            while self.running:
                try:
                    message = client_socket.recv(1024).decode('utf-8')
                    if not message:
                        break
                        
                    if '|' in message:
                        timestamp, msg_content = message.split('|', 1)
                    else:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        msg_content = message
                    
                    self.db.save_message(username, msg_content, timestamp)
                    
                    self.broadcast(f"[{timestamp}] {username}: {msg_content}", exclude=client_socket)
                    
                except ConnectionResetError:
                    break
                except Exception as e:
                    print(f"[SERVER] Error handling message: {e}")
                    break
                    
        except Exception as e:
            print(f"[SERVER] Error with client {username}: {e}")
            
        finally:
            if username and username in self.clients.values():
                print(f"[SERVER] {username} left the chat")
                self.broadcast(f"📢 {username} has left the chat")
                
            if client_socket in self.clients:
                del self.clients[client_socket]
                
            try:
                client_socket.close()
            except:
                pass
                
    def send_chat_history(self, client_socket):
        try:
            messages = self.db.get_messages(limit=50)
            if messages:
                history_msg = "--- Chat History ---\n"
                for msg in messages:
                    history_msg += f"[{msg['timestamp']}] {msg['username']}: {msg['message']}\n"
                history_msg += "--- End History ---\n"
                client_socket.send(history_msg.encode('utf-8'))
        except Exception as e:
            print(f"[SERVER] Error sending chat history: {e}")
            
    def broadcast(self, message, exclude=None):
        for client_socket in list(self.clients.keys()):
            if client_socket != exclude:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    del self.clients[client_socket]
                    
    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("[SERVER] Server stopped")


def main():
    server = ChatServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
        server.stop()


if __name__ == "__main__":
    main()
