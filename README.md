# Secure Local Vault Demo

This project is a small Python desktop application focused on secure local file handling and basic authentication. It combines a Tkinter GUI, simple file encryption/decryption, a local JSON-based vault, and a Flask backup endpoint for local automation experiments.

> This project is intended as a learning and portfolio project. It is not a production-grade enterprise security product.

## What it includes

- Local login screen with lockout logic
- File encryption and restoration flow
- Local vault metadata records
- QR-token generation for a simple payload handshake
- A small Flask API for backup operations
- Networking utility scripts for experimentation and learning

## How to run

### 1) Create a virtual environment

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Start the desktop app

```bash
python cyber_stastion.py
```

The first login uses the default password from the environment variable `APP_DEFAULT_PASSWORD` if it is set, otherwise it defaults to `change-me`. Change that immediately before any real use.

### 4) Run the Flask app (optional)

```bash
python -m src.app
```

## Project structure

```text
AdvancedCipher.py        QR-token and payload helper
Caesar.py                Legacy demo cipher
Controller.py            GUI controller and secure file logic
Login_View.py            Auth UI
System_Auth.py           Password hashing and lockout logic
View.py                 Main encrypted file UI
Vault.py                Local vault and file backup utilities
cyber_stastion.py        App launcher
src/app.py               Flask backup API
src/automation/backup.py Backup helper functions
requirements.txt         Python dependencies
SECURITY.md              Security and responsible-use guidance
LICENSE                  MIT license
```

## Security notes

- Never store real passwords or production secrets in version control.
- Do not expose the Flask API on a public network without authentication and TLS.
- Treat the app as a local demo only.
- For real data protection, use hardened, maintained libraries and proper secret management.

## License

This project is licensed under the MIT License. See `LICENSE`.
