# Python Automation, Networking Scripts & Flask

A small educational collection of Python networking, automation, file-integrity, backup, and URL-analysis utilities, with a deliberately limited Flask API for local backup operations.

> **Status:** educational/portfolio project. The scripts are not a production security platform.

## Responsible use

Use the networking and security tools only against systems, networks, and URLs that you own or are explicitly authorized to test. Scanning or probing third-party systems without permission may be illegal or disruptive. Results are heuristic and must not be treated as proof that a system is safe or vulnerable. See [SECURITY.md](SECURITY.md).

## Features

- Local Flask health endpoint and controlled backup endpoint
- TCP port scanning utilities
- DNS and host lookup helpers
- URL pattern/reputation checks
- HTTP fetching
- File-integrity hashing and comparison
- Log and network-summary helpers
- Local password-hash demonstration using salted PBKDF2-HMAC-SHA256

## Setup

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\\Scripts\\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the Flask app safely

The application binds to `127.0.0.1` by default and runs with debug mode disabled.

```bash
python -m src.app
```

Endpoints:

- `GET /` — service information
- `GET /health` — health check
- `POST /backup` — create a backup within the configured backup root

Example:

```bash
curl -X POST http://127.0.0.1:5000/backup \
  -H 'Content-Type: application/json' \
  -d '{"src":"./data","dest":"./backups","keep":7}'
```

The default allowed root is the current working directory. Set `BACKUP_ROOT` to a dedicated directory before using the endpoint. Do not expose this development service directly to the internet; add authentication, authorization, HTTPS, rate limiting, and an audited storage policy first.

## Run the scripts

The scripts are standalone and can be run by path, for example:

```bash
python "src/automation_networking _scripts/port_scanner_advanced.py" --host 127.0.0.1 --ports 22,80,443
python "src/automation_networking _scripts/dns_lookup.py"
python "src/automation_networking _scripts/url_reputation_checker.py"
python "src/automation_networking _scripts/password_manager.py"
```

Some URL-analysis scripts require the third-party packages listed in `requirements.txt`.

## Project layout

```text
src/
  app.py                         Flask application factory and routes
  automation/backup.py           Backup implementation used by the API
  automation_networking _scripts/ Standalone utilities
requirements.txt                 Runtime dependencies
SECURITY.md                      Responsible-use and security notes
LICENSE                          MIT license
```

## Limitations

These tools are intentionally simple. They do not provide comprehensive vulnerability detection, secure secret management, malware detection, or a guarantee of URL safety. Review and test changes before using them with important data.

## License

Released under the MIT License. See [LICENSE](LICENSE).
