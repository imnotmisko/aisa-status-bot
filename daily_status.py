import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

WEBHOOK = os.environ["DISCORD_WEBHOOK"]


def get_aisa_state():
    try:
        html = requests.get(
            "https://status.fi.muni.cz",
            timeout=10
        ).text

        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)

        idx = text.find("Aisa")

        if idx == -1:
            return "UNKNOWN"

        snippet = text[idx:idx + 100]

        if "OK" in snippet:
            return "UP"

        return "DOWN"

    except Exception:
        return "UNKNOWN"


state = get_aisa_state()

emoji = {
    "UP": "🟢",
    "DOWN": "🔴",
    "UNKNOWN": "🟡"
}.get(state, "⚪")

today = datetime.now().strftime("%d.%m.%Y")

requests.post(
    WEBHOOK,
    json={
        "content":
        f"🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹\n"
        f"📅 Dátum: {today}\n"
        f"-----------------------------\n"
        f"✅ AISA monitor je aktívny.\n"
        f"Aktuálny stav: {emoji} {state} \n"
        f"🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹"
    },
    timeout=10
)
