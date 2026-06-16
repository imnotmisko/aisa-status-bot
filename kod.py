import discord
import requests
from bs4 import BeautifulSoup
import asyncio
import os

TOKEN = os.environ["TOKEN"]
CHANNEL_ID = 1516517422562148483

STATUS_FILE = "aisa_state.txt"


def load_last_state():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None


def save_last_state(state):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(state)


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


intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Prihlásený ako {client.user}")

    channel = await client.fetch_channel(CHANNEL_ID)

    last_state = load_last_state()

    while True:
        current_state = get_aisa_state()
        
        print("Aktuálny stav:", current_state)

        if last_state is None:
            print("Prvý štart:", current_state)
            save_last_state(current_state)
            last_state = current_state

        elif current_state != last_state:

            if current_state == "UP":
                await channel.send(
                    "@everyone 🟢 **AISA je opäť dostupná.**"
                )

            elif current_state == "DOWN":
                await channel.send(
                    "@everyone 🔴 **AISA je nedostupná.**"
                )

            else:
                await channel.send(
                    "@everyone 🟡 **Nie je možné zistiť stav AISA.**"
                )

            save_last_state(current_state)
            last_state = current_state

        await asyncio.sleep(60)


client.run(TOKEN)