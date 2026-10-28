from pathlib import Path

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

if not ENV_FILE.exists():
    raise FileNotFoundError("Missing .env file. Copy .env.example to .env.")

settings = {}

for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
    line = line.strip()

    if not line or line.startswith("#"):
        continue

    key, separator, value = line.partition("=")

    if separator:
        settings[key.strip()] = value.strip()

BASE_URL = settings["BASE_URL"]
API_KEY = settings["API_KEY"]
MODEL = settings["MODEL"]