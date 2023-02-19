#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
import shlex
import argparse

SKIP_PATTERNS = [
    ".DS_Store",
    ".idea/misc.xml",
    ".idea/modules.xml",
    ".idea/runConfigurations/",
    ".idea/vcs.xml",
    "data/.DS_Store",
]

def run(cmd, cwd=None, check=True, capture_output=False):
    return subprocess.run(cmd, cwd=cwd, check=check,
                          text=True, capture_output=capture_output)

def list_untracked(repo_path: Path):
    # only untracked files; respects .gitignore
    res = run(["git", "ls-files", "--others", "--exclude-standard"], cwd=repo_path, capture_output=True)
    files = [line.strip() for line in res.stdout.splitlines() if line.strip()]
    return files

def should_skip(path_str: str) -> bool:
    p = path_str.strip().lstrip("./")
    # exact file skips
    exact = {s.rstrip("/") for s in SKIP_PATTERNS if not s.endswith("/")}
    if p in exact:
        return True
    # directory prefix skips (patterns ending with '/')
    for s in SKIP_PATTERNS:
        if s.endswith("/") and (p == s[:-1] or p.startswith(s)):
            return True
    return False

def ensure_git_repo(repo_path: Path):
    try:
        run(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_path)
    except subprocess.CalledProcessError:
        print("Hiba: nem egy git repository gyökerében futtattad.", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Untracked fájlok egyenkénti hozzáadása és visszadátumozott commitolása.")
    parser.add_argument("--start-date", default="2023-02-14", help="Kezdődátum (YYYY-MM-DD). Alapértelmezés: 2023-02-26")
    parser.add_argument("--time", default="14:30:00", help="Idő a commit dátumhoz (HH:MM:SS). Alapértelmezés: 14:30:00")
    parser.add_argument("--dry-run", action="store_true", help="Csak kiírja, mit tenne; nem ad és nem commitol.")
    parser.add_argument("--path", default=".", help="Repo útvonala. Alapértelmezés: jelen könyvtár.")
    args = parser.parse_args()

    repo = Path(args.path).resolve()
    ensure_git_repo(repo)

    untracked = list_untracked(repo)
    # szűrés
    files = [f for f in untracked if not should_skip(f)]
    # determinisztikus sorrend
    files.sort()

    if not files:
        print("Nincs hozzáadandó untracked fájl (a megadott szűrések után).")
        return

    try:
        base_dt = datetime.strptime(args.start_date + " " + args.time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Hibás dátum/idő formátum. Várható: YYYY-MM-DD és HH:MM:SS", file=sys.stderr)
        sys.exit(1)

    print(f"{len(files)} fájl kerül feldolgozásra. Kezdődátum: {base_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    for idx, relpath in enumerate(files):
        commit_dt = base_dt + timedelta(days=idx)
        iso_date = commit_dt.strftime("%Y-%m-%d %H:%M:%S")
        msg = f"File add: {relpath}"
        add_cmd = ["git", "add", "--", relpath]
        commit_cmd = ["git", "commit", f'--date={iso_date}', "-m", msg]

        if args.dry_run:
            print(f"[DRY] git add -- {relpath}")
            print(f"[DRY] git commit --date=\"{iso_date}\" -m {shlex.quote(msg)}")
        else:
            # add
            run(add_cmd, cwd=repo)
            # commit
            try:
                run(commit_cmd, cwd=repo)
                print(f"Committed: {relpath} @ {iso_date}")
            except subprocess.CalledProcessError as e:
                # ha valamiért nem sikerül (pl. üres commit), lépjünk tovább
                print(f"Figyelem: commit sikertelen ennél a fájlnál: {relpath}. Hiba: {e}", file=sys.stderr)
                # rollback az add-ra, hogy tiszta maradjon
                try:
                    run(["git", "reset", "HEAD", "--", relpath], cwd=repo)
                except subprocess.CalledProcessError:
                    pass

if __name__ == "__main__":
    main()