# Python Automation, Networking Scripts & Flask GUI

A Python project combining a Tkinter desktop vault application, file-protection workflows, a Flask backup API, and standalone automation/networking utilities.

## Projects

### Secure Local Vault

A Tkinter desktop application with:

- Login and account lockout handling
- PBKDF2-HMAC-SHA256 password verification
- Fernet-based text and file encryption
- Local vault metadata and backup records
- QR-token generation

Run it with:

```bash
python cyber_station.py
```

### Flask Backup API

A separate Flask example for local backup automation. It provides health information and a JSON endpoint for creating and rotating backup archives.

Run it with:

```bash
python -m src.app
```

The API runs locally by default and is not intended for direct public deployment without authentication, authorization, TLS, rate limiting, and further security review.

### Automation and networking scripts

The repository also contains standalone Python scripts for:

- TCP and UDP port scanning
- DNS and host lookups
- HTTP requests
- URL validation and reputation checks
- File-integrity hashing and comparison
- Log and text statistics
- Network summaries
- Backup automation
- Basic vulnerability-checking experiments
- Password-hashing examples

These scripts are independent utilities and are not required by the desktop vault or Flask application.

## Project structure

```text
.
├── AdvancedCipher.py                 QR-token helper
├── Controller.py                     Tkinter application controller
├── Login_View.py                     Login interface
├── System_Auth.py                    Authentication and lockout logic
├── Vault.py                          Vault metadata and backups
├── View.py                           Main Tkinter interface
├── cyber_station.py                  Desktop application entry point
├── src/
│   ├── app.py                        Flask backup API
│   ├── automation/backup.py          Backup implementation
│   └── automation_networking _scripts/ Standalone utilities
├── tests/                            Automated tests
├── docs/                             Additional documentation
├── assets/screenshots/               Application screenshots
├── requirements.txt
├── SECURITY.md
└── LICENSE
```

## Installation

Python 3.10 or newer is recommended.

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Initial password

For a new local installation, set the initial application password before starting the desktop app:

```bash
# macOS/Linux
export APP_DEFAULT_PASSWORD='your-local-password'

# Windows PowerShell
$env:APP_DEFAULT_PASSWORD = 'your-local-password'
```

Do not use production credentials with this project.

## Tests

```bash
pytest
```

## Screenshots

Application screenshots can be placed in `assets/screenshots/` and included here:

```md
![Login screen](assets/screenshots/login.png)
![Vault interface](assets/screenshots/vault.png)
```

## Security and responsible use

This is an educational and portfolio project. The encryption, authentication, URL-analysis, scanning, and backup features have not been independently audited and should not be used as a replacement for professional security software.

Use the networking and security utilities only on systems, networks, files, and URLs that you own or are authorized to test. Do not commit passwords, keys, tokens, private files, or generated local data to the repository.

See [SECURITY.md](SECURITY.md) for additional guidance.

## License

MIT License. See [LICENSE](LICENSE).
