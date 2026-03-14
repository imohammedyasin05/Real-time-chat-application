"""
Client module for Real-Time Chat Application
"""

import socket
import threading
import sys
import os
from gui import ChatGUI, LoginWindow


class ChatClient:
    
    def __init__(self):
        self.client_socket = None
        self.username = None
        self.running = False
        self.gui = None
        
    def connect(self, host, port, username):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            self.username = username
            self.running = True
            
            self.client_socket.send(username.encode('utf-8'))
            
            print(f"[CLIENT] Connected to {host}:{port}")
            return True
            
        except ConnectionRefusedError:
            print("[CLIENT] Connection refused - is the server running?")
            return False
        except Exception as e:
            print(f"[CLIENT] Connection error: {e}")
            return False
            
    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(4096).decode('utf-8')
                if not message:
                    break
                    
                if self.gui:
                    self.gui.append_message(message)
                    
            except ConnectionResetError:
                print("[CLIENT] Connection lost")
                break
            except Exception as e:
                print(f"[CLIENT] Error receiving message: {e}")
                break
                
        self.running = False
        if self.gui:
            self.gui.update_status("● Disconnected", "#E74C3C")
            
    def send_message(self, message):
        try:
            if self.client_socket and self.running:
                self.client_socket.send(message.encode('utf-8'))
                return True
        except Exception as e:
            print(f"[CLIENT] Error sending message: {e}")
            return False
        return False
        
    def disconnect(self):
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass


def main():
    login_window = LoginWindow()
    print("[CLIENT] Debug: LoginWindow initialized, calling get_credentials...")
    username, host, port = login_window.get_credentials()
    
    if not username:
        print("[CLIENT] No username provided, exiting...")
        return
        
    client = ChatClient()
    
    print(f"[CLIENT] Attempting to connect to {host}:{port}...")
    
    if not client.connect(host, port, username):
        input("Failed to connect. Press Enter to exit...")
        return
        
    gui = ChatGUI(client.client_socket, username)
    client.gui = gui
    
    receive_thread = threading.Thread(target=client.receive_messages, daemon=True)
    receive_thread.start()
    
    gui.run()
    
    client.disconnect()
    print("[CLIENT] Client closed")


if __name__ == "__main__":
    main()
