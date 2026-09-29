#!/usr/bin/env python3
"""Genera l'email pronta da inviare.

`email.html` usa percorsi relativi (immagini/...) cosi' si puo' aprire e
modificare in locale. Le email pero' hanno bisogno di URL pubblici: questo
script crea `dist/email-da-inviare.html` sostituendo "immagini/" con l'URL
jsDelivr del repository GitHub.

Uso:
    python3 build.py                      # ricava owner/repo dal remote git "origin"
    python3 build.py --repo owner/nome    # oppure lo indichi tu
    python3 build.py --ref v2026          # usa un tag invece di "main"

Consiglio: dopo l'invio crea un tag (es. v2026) e rigenera con --ref v2026,
cosi' l'email gia' inviata non cambia anche se l'anno dopo modificate le immagini.
"""
import argparse
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent


def repo_from_git():
    try:
        url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"], cwd=ROOT, text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    m = re.search(r"github\.com[:/]([^/]+)/([^/.]+?)(?:\.git)?$", url)
    return f"{m[1]}/{m[2]}" if m else None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--repo", help="owner/nome del repository GitHub")
    p.add_argument("--ref", default="main", help="branch o tag da usare (default: main)")
    args = p.parse_args()

    repo = args.repo or repo_from_git()
    if not repo:
        sys.exit("Non trovo il repository: usa --repo owner/nome")

    base = f"https://cdn.jsdelivr.net/gh/{repo}@{args.ref}/immagini/"
    html = (ROOT / "email.html").read_text(encoding="utf-8")
    out, n = re.subn(r'src="immagini/', f'src="{base}', html)

    missing = [f for f in re.findall(r'src="immagini/([^"]+)"', html) if not (ROOT / "immagini" / f).exists()]
    if missing:
        sys.exit(f"Immagini mancanti in immagini/: {', '.join(sorted(set(missing)))}")

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    (dist / "email-da-inviare.html").write_text(out, encoding="utf-8")
    print(f"OK: {n} immagini -> {base}")
    print("Creato dist/email-da-inviare.html")


if __name__ == "__main__":
    main()
