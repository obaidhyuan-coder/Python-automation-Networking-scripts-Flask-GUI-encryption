"""Backup helpers used by the Flask app and command-line tools."""

from datetime import datetime, timezone
from pathlib import Path
import shutil


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def build_backup(src: Path, dest: Path) -> Path:
    src = Path(src).expanduser().resolve()
    dest = Path(dest).expanduser().resolve()
    if not src.exists():
        raise ValueError("source path does not exist")
    if src == dest:
        raise ValueError("source and destination must differ")
    ensure_directory(dest)
    return Path(shutil.make_archive(str(dest / f"backup-{timestamp()}"), "gztar", root_dir=str(src)))


def rotate_backups(dest: Path, keep: int = 7) -> None:
    if keep < 1:
        raise ValueError("keep must be at least 1")
    backups = sorted(Path(dest).glob("backup-*.tar.gz"), key=lambda path: path.stat().st_mtime, reverse=True)
    for old in backups[keep:]:
        old.unlink()
