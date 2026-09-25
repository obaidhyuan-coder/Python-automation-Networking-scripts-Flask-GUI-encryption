"""Password manager: store and verify passwords with hashing."""

import hashlib
import json
from pathlib import Path

# Hash a password using SHA256 and return the hex digest.
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Store a password hash for a service in a JSON file.
def store_password(service, password, db_file="passwords.json"):
    db = {}
    if Path(db_file).exists():
        with open(db_file, "r") as f:
            db = json.load(f)
    hashed = hash_password(password)
    db[service] = hashed
    with open(db_file, "w") as f:
        json.dump(db, f, indent=2)
    print(f"Password for {service} stored")

# Compare a provided password against the stored hash.
def verify_password(service, password, db_file="passwords.json"):
    if not Path(db_file).exists():
        print("No password database found")
        return False
    with open(db_file, "r") as f:
        db = json.load(f)
    if service not in db:
        print(f"Service {service} not found")
        return False
    hashed = hash_password(password)
    if db[service] == hashed:
        print(f"Password for {service} is correct")
        return True
    else:
        print(f"Password for {service} is incorrect")
        return False

# List the stored service names in the password database.
def list_services(db_file="passwords.json"):
    if not Path(db_file).exists():
        print("No password database found")
        return
    with open(db_file, "r") as f:
        db = json.load(f)
    print("Stored services:")
    for service in db.keys():
        print(f"  - {service}")

# Main menu for the password manager.
def main():
    print("Password Manager")
    action = input("(1) Store password, (2) Verify password, (3) List services? Enter 1, 2, or 3: ")
    if action == "1":
        service = input("Enter service name: ")
        password = input("Enter password: ")
        store_password(service, password)
    elif action == "2":
        service = input("Enter service name: ")
        password = input("Enter password to verify: ")
        verify_password(service, password)
    elif action == "3":
        list_services()
    else:
        print("Invalid action")


if __name__ == "__main__":
    main()
