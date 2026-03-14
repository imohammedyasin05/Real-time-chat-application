"""
GUI module for Real-Time Chat Application
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from datetime import datetime
import threading


class ChatGUI:
    
    def __init__(self, client_socket, username):
        self.client_socket = client_socket
        self.username = username
        self.root = tk.Tk()
        self.root.title(f"Chat - {username}")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.bg_color = "#2C3E50"
        self.text_bg = "#34495E"
        self.text_fg = "#ECF0F1"
        self.accent_color = "#3498DB"
        self.input_bg = "#95A5A6"
        
        self.is_fullscreen = True
        self.root.attributes("-fullscreen", True)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        
        self.setup_ui()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        header_frame = tk.Frame(main_frame, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            header_frame,
            text=f"💬 Real-Time Chat - Welcome, {self.username}!",
            font=("Arial", 14, "bold"),
            bg=self.bg_color,
            fg=self.text_fg
        )
        title_label.pack(side=tk.LEFT)
        
        
        self.fs_btn = tk.Button(
            header_frame,
            text="❐ Exit Full Screen",
            command=self.toggle_fullscreen,
            bg=self.accent_color,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        self.fs_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            width=70,
            height=20,
            font=("Consolas", 10),
            bg=self.text_bg,
            fg=self.text_fg,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.chat_display.tag_config("system", foreground="#F39C12")
        self.chat_display.tag_config("join", foreground="#27AE60")
        self.chat_display.tag_config("leave", foreground="#E74C3C")
        self.chat_display.tag_config("history", foreground="#9B59B6")
        
        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X)
        
        self.message_entry = tk.Entry(
            input_frame,
            font=("Arial", 11),
            bg=self.input_bg,
            fg="black",
            relief=tk.FLAT
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", self.send_message)
        
        send_btn = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=5
        )
        send_btn.pack(side=tk.RIGHT)
        
        self.status_label = tk.Label(
            main_frame,
            text="● Connected",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#27AE60"
        )
        self.status_label.pack(anchor=tk.W, pady=(5, 0))
        
    def append_message(self, message, tag=None):
        self.chat_display.config(state=tk.NORMAL)
        
        if "joined the chat" in message or "has joined the chat" in message:
            self.chat_display.insert(tk.END, message + "\n", "join")
        elif "left the chat" in message or "has left the chat" in message:
            self.chat_display.insert(tk.END, message + "\n", "leave")
        elif "--- Chat History ---" in message:
            self.chat_display.insert(tk.END, message + "\n", "history")
        elif tag:
            self.chat_display.insert(tk.END, message + "\n", tag)
        else:
            self.chat_display.insert(tk.END, message + "\n")
            
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        
        if message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_message = f"{timestamp}|{message}"
            
            try:
                self.client_socket.send(full_message.encode('utf-8'))
                # Display the message locally (sender sees their own messages)
                self.append_message(f"[{timestamp}] {self.username}: {message}")
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send message: {e}")
                self.update_status("● Disconnected", "#E74C3C")
                
    def update_status(self, status, color="#27AE60"):
        self.status_label.config(text=status, fg=color)
        
    def show_users(self):
        messagebox.showinfo("Users", "User list feature - showing recent chatters")
        
    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        if self.is_fullscreen:
            self.fs_btn.config(text="❐ Exit Full Screen")
        else:
            self.fs_btn.config(text="⛶ Full Screen")
            
    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)
        self.fs_btn.config(text="⛶ Full Screen")
        
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the chat?"):
            try:
                self.client_socket.close()
            except:
                pass
            self.root.destroy()
            
    def run(self):
        self.root.mainloop()


class LoginWindow:
    
    def __init__(self):
        print("[GUI] Debug: Initializing LoginWindow...")
        self.root = tk.Tk()
        print("[GUI] Debug: Tk root created.")
        self.root.title("Chat Login")
        self.root.geometry("400x400")
        self.root.resizable(True, True)
        
        self.bg_color = "#2C3E50"
        self.text_fg = "#ECF0F1"
        self.accent_color = "#3498DB"
        
        self.server_port = None
        
        self.setup_ui()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        print("[GUI] Debug: Starting Tk mainloop...")
        self.root.mainloop()
        print("[GUI] Debug: Tk mainloop exited.")
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        title = tk.Label(
            main_frame,
            text="🔐 Chat Login",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.text_fg
        )
        title.pack(pady=(0, 20))
        
        tk.Label(
            main_frame,
            text="Username:",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.text_fg
        ).pack(anchor=tk.W)
        
        self.username_entry = tk.Entry(
            main_frame,
            font=("Arial", 11),
            bg="white",
            relief=tk.FLAT
        )
        self.username_entry.pack(fill=tk.X, pady=(5, 15))
        
        tk.Label(
            main_frame,
            text="Server Host:",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.text_fg
        ).pack(anchor=tk.W)
        
        self.host_entry = tk.Entry(
            main_frame,
            font=("Arial", 11),
            bg="white",
            relief=tk.FLAT
        )
        self.host_entry.insert(0, "127.0.0.1")
        self.host_entry.pack(fill=tk.X, pady=(5, 15))
        
        tk.Label(
            main_frame,
            text="Server Port:",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.text_fg
        ).pack(anchor=tk.W)
        
        self.port_entry = tk.Entry(
            main_frame,
            font=("Arial", 11),
            bg="white",
            relief=tk.FLAT
        )
        self.port_entry.insert(0, "5555")
        self.port_entry.pack(fill=tk.X, pady=(5, 20))
        
        connect_btn = tk.Button(
            main_frame,
            text="Connect",
            command=self.connect,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=8
        )
        connect_btn.pack()
        
    def connect(self):
        username = self.username_entry.get().strip()
        host = self.host_entry.get().strip()
        port = self.port_entry.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
            
        if not host:
            messagebox.showerror("Error", "Please enter a server host")
            return
            
        try:
            port = int(port)
            if port < 1 or port > 65535:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid port number")
            return
            
        self.username = username
        self.server_host = host
        self.server_port = port
        self.root.quit()
        self.root.destroy()
        
    def get_credentials(self):
        return self.username, self.server_host, self.server_port


if __name__ == "__main__":
    login = LoginWindow()
    username, host, port = login.get_credentials()
    print(f"Username: {username}, Host: {host}, Port: {port}")
