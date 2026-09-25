# Secure Local Vault Demo

A Python portfolio project that combines a local desktop vault, file-protection workflows, a small Flask backup API, and educational automation and networking utilities.

This repository is designed to demonstrate practical Python skills in an honest, beginner-friendly way. The **Secure Local Vault** is the main desktop project. The Flask API and networking scripts are separate supporting examples rather than one production security platform.

> **Status:** learning and portfolio project. It is not a professionally audited password manager, encryption product, or enterprise cybersecurity platform.

## Project story

I built this project to practice turning a security-focused idea into a usable desktop workflow. A user authenticates, enters a key, encrypts or restores local text and files, and records basic metadata in a local vault.

The repository also contains a separate Flask backup example and smaller automation/networking scripts created while learning Python. Together, the projects demonstrate GUI development, file processing, authentication logic, local backups, HTTP/DNS work, and command-line automation.

## What is included

### Main project: Secure Local Vault

- Tkinter desktop interface
- Local login screen with lockout logic
- PBKDF2-HMAC-SHA256 password verification
- Fernet-based authenticated encryption workflow
- Local vault metadata and backup records
- QR-token demonstration

### Separate Flask example

- Local health endpoint
- JSON-based backup request handling
- Backup archive creation and rotation
- Path and retention validation
- Localhost-first configuration

The Flask example is independent of the desktop GUI. You can run either project without needing the other.

### Automation and networking utilities

The repository also includes standalone educational scripts for:

- TCP and UDP port scanning
- DNS and host lookups
- HTTP fetching
- URL reputation and suspicious-pattern checks
- File-integrity hashing and comparison
- Log and text statistics
- Network summaries
- Backup automation
- Basic vulnerability-checking experiments
- Password-hashing demonstrations

These utilities are supporting learning examples. They are not presented as a complete security toolkit and should only be used on systems, files, and URLs that you own or are authorized to test.

## Repository structure

```text
.
├── README.md
├── LICENSE
├── SECURITY.md
├── requirements.txt
├── cyber_station.py                 # Desktop app entry point
├── Login_View.py                    # Login window
├── View.py                          # Main Tkinter vault interface
├── Controller.py                    # GUI actions and encryption workflow
├── System_Auth.py                   # Password hashing and lockout logic
├── Vault.py                         # Local metadata and vault backups
├── AdvancedCipher.py                # QR-token and encryption helper
├── src/
│   ├── app.py                       # Separate Flask backup API
│   ├── automation/backup.py         # Flask backup implementation
│   └── automation_networking _scripts/ # Standalone learning utilities
├── docs/
│   └── flask-api.md                 # Flask example notes
├── assets/
│   └── screenshots/                 # Optional portfolio screenshots
└── tests/                            # Automated tests
```

## Why this project is useful for small freelance jobs

This repository demonstrates experience with:

- Python desktop applications
- Tkinter GUI development
- File reading, writing, and transformation
- Password verification and lockout flows
- JSON data storage
- Local backup automation
- Flask routes and JSON APIs
- DNS, HTTP, and networking utilities
- Command-line scripts and input validation

This is relevant to small freelance tasks such as:

- Python automation scripts
- File-management utilities
- Tkinter interface fixes
- JSON or CSV processing
- Local backup tools
- Simple Flask endpoints
- Beginner Python debugging and improvements

## Screenshots

Add screenshots to `assets/screenshots/` when available:

```text
assets/screenshots/
├── login.png
├── vault.png
├── qr-token.png
└── app-overview.png
```

Then include them in this section:

```md
![Login screen](assets/screenshots/login.png)

![Vault workspace](assets/screenshots/vault.png)
```

Screenshots should show the application with demonstration data only. Do not capture real passwords, private files, or production secrets.

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the desktop vault

```bash
python cyber_station.py
```

For a new local demo, set an initial password before starting the app:

```bash
# macOS/Linux
export APP_DEFAULT_PASSWORD='choose-a-local-password'

# Windows PowerShell
$env:APP_DEFAULT_PASSWORD = 'choose-a-local-password'
```

Do not use a real production password in this demo repository.

### 4. Run the separate Flask example

```bash
python -m src.app
```

The Flask app binds to localhost by default. See [`docs/flask-api.md`](docs/flask-api.md) for its purpose and limitations.

### 5. Run tests

```bash
pytest
```

## Generated local files

The applications may create local files such as:

```text
security.json
central_vault.json
vault_backups/
access_token.png
*.secured
*.restored
```

These are local demo data and should remain excluded from version control. Never commit real passwords, keys, tokens, or private files.

## Limitations and responsible use

Use the networking, URL, backup, and security utilities only with systems, networks, files, and URLs that you own or are explicitly authorized to test. Scanning or probing third-party systems may be illegal or disruptive.

The tools use simple demonstrations and heuristics. They can produce false positives and false negatives. This project should not be marketed as:

- A production-grade password manager
- An enterprise file-encryption platform
- A professional penetration-testing toolkit
- A compliance or hardening product
- A guarantee that a file, URL, or system is safe

The Flask backup endpoint is intended for local development. Do not expose it to an untrusted network without authentication, authorization, TLS, rate limiting, and a security review. See [`SECURITY.md`](SECURITY.md).

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE).

## Portfolio description

> Python portfolio project featuring a Tkinter secure local vault demo, password protection, file-encryption workflows, a separate Flask backup API, and educational automation/networking utilities.
