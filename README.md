# 🔐 In House Password Manager

A simple and secure terminal-based password manager built with **Python** and **SQLite**.  
Passwords are encrypted using **SHA-256 hashing** and stored locally.  

## ✨ Features
- 🗂️ Store and manage your passwords securely  
- 🔎 Display saved credentials through an interactive menu  
- 🔒 Passwords are hashed with **SHA-256** for security  
- 🖥️ Simple **command-line menu interface**  

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rujhannajib/IHPM.git
   cd IHPM
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
3. **Run the application**
   ```bash
   python app.py

## Usage

- When you run the program, you’ll see a menu with options like:
1. Add a new password
2. Get a password
3. List all services
4. Delete a password
5. Quit

## How It Works

1. The application uses SQLite to store account and password data.
2. Passwords are encrypted with SHA-256 hashing before being saved.
3. You can interact with the program using a menu-driven interface in the terminal.

## 📦 Dependencies
- cffi==1.17.1
- cryptography==45.0.6
- pycparser==2.22

## 🔮 Future Improvements

- Add support for password generation
- Implement search and filtering
- Enable export/import of encrypted data

