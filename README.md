# Secure Local Vault Demo

A beginner-friendly Python desktop utility for local file protection and access control. It demonstrates Tkinter GUI development, password hashing, authenticated file encryption with Fernet, local vault metadata, and a separate Flask backup API.

## Project story

I built this project to practice turning a security-focused idea into a usable desktop workflow: a user authenticates, enters a key, encrypts or restores a local file, and records basic vault metadata. The Flask API is intentionally separate and demonstrates how the same project can expose a small local automation service.

This is a portfolio and learning project—not a replacement for a professionally audited password manager or enterprise security product.

## Features

- Tkinter desktop interface
- PBKDF2-HMAC-SHA256 password verification with lockout logic
- Fernet-based authenticated encryption for text and files
- Local vault metadata and backup records
- QR token demo
- Separate localhost-only Flask backup example

## Screenshots

Screenshots can be added to `assets/screenshots/` and linked here:

| Login | Vault workspace |
| --- | --- |
| Add `assets/screenshots/login.png` | Add `assets/screenshots/vault.png` |

## Quick start

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the desktop app:

```bash
python cyber_station.py
```

On first run, set an initial password before starting the app:

```bash
# macOS/Linux
export APP_DEFAULT_PASSWORD='choose-a-local-password'

# Windows PowerShell
$env:APP_DEFAULT_PASSWORD = 'choose-a-local-password'
```

Do not use a real production password in this demo.

## Separate Flask example

The Flask backup API is not required by the desktop app. It is kept as an independent local automation example:

```bash
python -m src.app
```

It listens on localhost by default. Do not expose it publicly without authentication, authorization, TLS, rate limiting, and a security review. More details are in `docs/flask-api.md`.

## Repository layout

```text
cyber_station.py       Desktop app entry point
Login_View.py          Login window
View.py                Tkinter vault interface
Controller.py          GUI actions and encryption workflow
System_Auth.py         Password hashing and lockout logic
Vault.py               Local metadata and vault backups
AdvancedCipher.py      QR-token demo helper
src/app.py             Separate Flask backup example
src/automation/backup.py Flask backup implementation
tests/                 Automated tests
assets/screenshots/    Portfolio screenshots
```

## Limitations and responsible use

Use this only with files and systems you own or are authorized to test. Keep generated files such as `security.json`, `central_vault.json`, `vault_backups/`, and `access_token.png` out of version control. This project has not been independently audited and should not be used to protect sensitive production data.

## License

MIT License. See `LICENSE`.
