# Real-Time Chat Application

A client-server chat system where multiple users can send and receive messages in real time using Python socket programming, threading, and SQLite database.

## 📋 Project Overview

This is a fully functional real-time chat application built with Python that allows multiple users to connect to a central server and communicate instantly. The application features a modern Tkinter-based GUI, persistent chat history stored in SQLite, and handles multiple concurrent connections using threading.

## 🏗️ Project Architecture

```
chat_application/
│
├── server/
│   └── server.py          # Server-side socket handling and message routing
│
├── client/
│   ├── client.py          # Client socket connection logic
│   └── gui.py             # Tkinter-based graphical user interface
│
├── database/
│   └── database.py        # SQLite database operations
│
├── requirements.txt       # Python dependencies (standard library only)
└── README.md             # This file
```

## ✨ Features

| Feature | Description |
|---------|-------------|
| **User Login** | Simple username-based login system |
| **Real-Time Messaging** | Instant message delivery to all connected users |
| **Chat History** | Persistent storage of all messages in SQLite database |
| **Multiple Clients** | Support for unlimited concurrent connections |
| **Timestamps** | Every message includes date and time |
| **Threading** | Efficient handling of multiple clients simultaneously |
| **GUI** | User-friendly Tkinter interface |

## 🛠️ Technologies Used

- **Python 3.x** - Programming language
- **Socket Programming** - TCP/IP for network communication
- **Threading** - Concurrent client handling
- **SQLite** - Lightweight database for chat history
- **Tkinter** - Built-in Python GUI library

## 🚀 How to Run

### Prerequisites

- Python 3.6 or higher installed
- No external packages required (uses standard library only)

### Step 1: Start the Server

Open a terminal and run:

```bash
cd chat_application
python server/server.py
```

The server will start on `127.0.0.1:5555` by default.

### Step 2: Start Clients

Open a new terminal for each client and run:

```bash
cd chat_application
python client/client.py
```

Each client will see a login window where they can:
- Enter a username
- Specify server host (default: 127.0.0.1)
- Specify server port (default: 5555)

### Step 3: Chat!

- Type messages in the input box
- Press Enter or click Send to send
- Messages appear instantly for all connected users

## 📖 How It Works

### Server (`server/server.py`)

1. Creates a TCP socket and listens for connections
2. When a client connects, spawns a new thread to handle it
3. Receives username from client and adds to active clients list
4. Broadcasts join/leave notifications to all clients
5. Routes messages from one client to all other clients
6. Stores messages in SQLite database

### Client (`client/client.py`)

1. Connects to server using socket
2. Sends username for identification
3. Spawns a thread to continuously receive messages
4. Main thread handles user input and GUI updates

### Database (`database/database.py`)

- Creates SQLite database file (`chat_history.db`)
- Stores messages with: username, message content, timestamp
- Provides methods for saving/retrieving messages

### GUI (`client/gui.py`)

- LoginWindow: Entry point for username and server details
- ChatGUI: Main chat interface with message display and input

## 🔧 Configuration

### Changing Server Port

In `server/server.py`, modify the port:

```python
server = ChatServer(host='127.0.0.1', port=5555)  # Change 5555 to desired port
```

### Changing Database Location

In `database/database.py`:

```python
db = Database(db_path='path/to/your/database.db')
```

## 📝 Usage Tips

1. **Multiple Clients**: Run multiple instances of client.py in different terminals to test multi-user chat
2. **Chat History**: New users automatically receive the last 50 messages when they join
3. **Disconnect**: Close the client window to disconnect gracefully

## ⚠️ Known Limitations

- No message encryption (plain text over TCP)
- No user authentication (username only)
- Server must be running before clients can connect
- GUI is basic (Tkinter default styling)

## 🎓 Educational Value

This project demonstrates:
- Socket programming fundamentals
- Multi-threaded server design
- Client-server architecture patterns
- Database integration with SQLite
- GUI development with Tkinter
- Real-time network communication

## 📄 License

This project is for educational purposes.

---

Built with ❤️ using Python
