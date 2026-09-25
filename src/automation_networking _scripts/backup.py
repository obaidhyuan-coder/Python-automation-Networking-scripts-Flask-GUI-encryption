#!/usr/bin/env python3
"""
Backup automation script.
"""
import argparse
from pathlib import Path
import shutil
from datetime import datetime, timezone

# Create the destination folder if it does not exist.
def ensure_directory(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

# Generate a UTC timestamp string for the backup filename.
def timestamp():
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

# Build a compressed archive of the source path.
def build_backup(src: Path, dest: Path):
    ensure_directory(dest)
    archive_base = dest / f"backup-{timestamp()}"
    archive_path = shutil.make_archive(str(archive_base), "gztar", root_dir=str(src))
    return Path(archive_path)

def rotate_backups(dest: Path, keep: int):
    # Remove the oldest backup files beyond the number we want to keep.
    if not dest.exists():
        print("Destination path does not exist:", dest)
        return
    backups = sorted(
        [p for p in dest.iterdir() if p.is_file()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not backups:
        print("No backups to rotate yet.")
        return
    for old in backups[keep:]:
        print("Removing old backup:", old.name)
        old.unlink()

# Parse command-line arguments for source, destination, keep count, and dry run.
def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a backup archive and rotate old backups."
    )
    parser.add_argument("--src", required=True, help="Source folder or file to back up")
    parser.add_argument("--dest", required=True, help="Destination folder for backups")
    parser.add_argument("--keep", type=int, default=7, help="How many backups to keep")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files, just show actions")
    return parser.parse_args()

def main():
    args = parse_args()
    src_path = Path(args.src).expanduser().resolve()
    dest_path = Path(args.dest).expanduser().resolve()
    if not src_path .exists():
        print("Source path does not exist:", src_path)
        return
    if not dest_path.exists():
        print("Destination path does not exist:", dest_path)
        return
    print("src:", src_path)
    print("dest:", dest_path)
    print("keep:", args.keep)
    print("dry run:", args.dry_run)

    if args.dry_run:
        print("Dry run only. No backup created.")
        return

    archive_path = build_backup(src_path,dest_path)
    print("Created backup:", archive_path)

   
    rotate_backups(dest_path, keep=args.keep)


if __name__ == "__main__":
    main()