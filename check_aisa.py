import requests
from bs4 import BeautifulSoup
import os
import json

WEBHOOK = os.environ["DISCORD_WEBHOOK"]


r = requests.post(
    WEBHOOK,
    json={"content": "🧪 GitHub Action funguje"},
    timeout=10
)

print("Webhook status:", r.status_code)
print("Webhook response:", r.text)

def get_aisa_state():
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


def load_state():
    if not os.path.exists(STATE_FILE):
        return None

    with open(STATE_FILE, "r") as f:
        return json.load(f)["state"]


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump({"state": state}, f)


def send_discord(message):
    requests.post(
        WEBHOOK,
        json={"content": message},
        timeout=10
    )


current = get_aisa_state()
previous = load_state()

print("Previous:", previous)
print("Current:", current)

if previous is None:
    save_state(current)

elif previous != current:

    if current == "UP":
        send_discord(
            "@everyone 🟢 AISA je opäť dostupná."
        )

    elif current == "DOWN":
        send_discord(
            "@everyone 🔴 AISA je nedostupná."
        )

    else:
        send_discord(
            "@everyone 🟡 Stav AISA sa nepodarilo zistiť."
        )

    save_state(current)
