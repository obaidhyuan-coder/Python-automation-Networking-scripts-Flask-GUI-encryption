from flask import Flask, jsonify, request
from pathlib import Path
import os

from automation.backup import build_backup, rotate_backups


def _configured_root() -> Path:
    return Path(os.environ.get("BACKUP_ROOT", Path.cwd())).expanduser().resolve()


def _inside_root(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["BACKUP_ROOT"] = _configured_root()
    app.config["MAX_KEEP"] = int(os.environ.get("MAX_BACKUPS", "100"))

    @app.get("/")
    def index():
        return jsonify(message="Python automation Flask app is running", status="ready", routes=["/health", "/backup"])

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.post("/backup")
    def backup():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="Request body must be a JSON object"), 400

        source_value = payload.get("src")
        dest_value = payload.get("dest")
        if not isinstance(source_value, str) or not isinstance(dest_value, str) or not source_value or not dest_value:
            return jsonify(error="Missing required string fields: src and dest"), 400

        try:
            keep = int(payload.get("keep", 7))
        except (TypeError, ValueError):
            return jsonify(error="keep must be an integer"), 400

        if not 1 <= keep <= app.config["MAX_KEEP"]:
            return jsonify(error=f"keep must be between 1 and {app.config['MAX_KEEP']}"), 400

        root = app.config["BACKUP_ROOT"]
        source = Path(source_value).expanduser().resolve()
        destination = Path(dest_value).expanduser().resolve()
        if not _inside_root(source, root) or not _inside_root(destination, root):
            return jsonify(error="src and dest must be inside BACKUP_ROOT"), 400
        if not source.exists():
            return jsonify(error="Source path does not exist"), 400
        if source == destination:
            return jsonify(error="Source and destination must be different"), 400

        try:
            archive = build_backup(source, destination)
            rotate_backups(destination, keep)
        except (OSError, ValueError) as exc:
            app.logger.warning("Backup failed: %s", exc)
            return jsonify(error="Backup could not be created"), 400

        return jsonify(message="Backup complete", archive=str(archive), source=str(source), dest=str(destination), keep=keep)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host=os.environ.get("FLASK_HOST", "127.0.0.1"), port=int(os.environ.get("FLASK_PORT", "5000")), debug=False)
