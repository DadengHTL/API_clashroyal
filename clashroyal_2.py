
import random
import tkinter as tk
import requests

# 1. Daten von RoyaleAPI laden
url = "https://royaleapi.github.io/cr-api-data/json/cards.json"
response = requests.get(url, timeout=10)
response.raise_for_status()
cards = response.json()
#hallo
seltenheiten = {
    "gewöhnlich": "Common",
    "common": "Common",
    "selten": "Rare",
    "rare": "Rare",
    "episch": "Epic",
    "epic": "Epic",
    "legendär": "Legendary",
    "legendary": "Legendary",
    "champion": "Champion",
}

fenster = tk.Tk()
fenster.title("Clash Royale Suche & Deck-Generator")
fenster.geometry("520x540")
fenster.config(bg="#0f2547")

tk.Label(
    fenster,
    text="CLASH ROYALE SUCHE",
    font=("Arial", 16, "bold"),
    bg="#0f2547",
    fg="#ffcc00",
).pack(pady=10)

tk.Label(
    fenster,
    text="Name (z. B. Pekka), Seltenheit (z. B. Selten, Episch) oder '8er':",
    bg="#0f2547",
    fg="white",
).pack()

eingabe = tk.Entry(fenster, width=36, font=("Arial", 12), justify="center")
eingabe.pack(pady=8)


def zeige_karten_info(karte):
  ausgabe.insert(tk.END, f"--- Infos zu {karte['name']} ---\n")
  ausgabe.insert(tk.END, f"Typ: {karte.get('type')}\n")
  ausgabe.insert(tk.END, f"Seltenheit: {karte.get('rarity')}\n")
  ausgabe.insert(tk.END, f"Elixier-Kosten: {karte.get('elixir')}\n")
  ausgabe.insert(tk.END, f"Beschreibung: {karte.get('description')}\n")


def generiere_8er_deck():
  ausgabe.delete("1.0", tk.END)
  ausgabe.insert(tk.END, "--- Zufälliges 8er-Deck ---\n\n")

  deck = random.sample(cards, 8)
  gesamt_elixier = 0

  for card in deck:
    elixier = card.get("elixir", 0)
    gesamt_elixier += elixier
    ausgabe.insert(
        tk.END,
        f"- {card['name']} (Seltenheit: {card.get('rarity')}, "
        f"Elixier-Kosten: {elixier})\n",
    )

  schnitt = gesamt_elixier / len(deck)
  ausgabe.insert(tk.END, f"\nDurchschnitts-Elixier: {schnitt:.2f}")


def suchen(event=None):
  ausgabe.delete("1.0", tk.END)
  gesucht = eingabe.get().strip().lower()

  if not gesucht:
    ausgabe.insert(
        tk.END,
        "Bitte gib einen Kartennamen, eine Seltenheit oder '8er' ein.",
    )
    return

  if gesucht == "8er":
    generiere_8er_deck()
    return

  if gesucht in seltenheiten:
    englische_seltenheit = seltenheiten[gesucht]
    ausgabe.insert(tk.END, f"Alle Karten mit Seltenheit '{gesucht}':\n\n")

    treffer = [
        card for card in cards if card.get("rarity") == englische_seltenheit
    ]
    for card in treffer:
      ausgabe.insert(tk.END, f"- {card['name']}\n")

    ausgabe.insert(
        tk.END,
        "\nWelche Karte davon möchtest du genauer sehen? (Oben eingeben)",
    )
  else:
    gefundene_karte = None
    for card in cards:
      if gesucht in card["name"].lower():
        gefundene_karte = card
        break

    if gefundene_karte:
      zeige_karten_info(gefundene_karte)
    else:
      ausgabe.insert(tk.END, "Karte wurde nicht gefunden!")


eingabe.bind("<Return>", suchen)

button_rahmen = tk.Frame(fenster, bg="#0f2547")
button_rahmen.pack(pady=5)

tk.Button(
    button_rahmen,
    text="Suchen",
    command=suchen,
    font=("Arial", 11, "bold"),
    bg="#ffcc00",
    fg="black",
    padx=12,
).pack(side=tk.LEFT, padx=6)

tk.Button(
    button_rahmen,
    text="Zufälliges 8er-Deck",
    command=generiere_8er_deck,
    font=("Arial", 11, "bold"),
    bg="#38bdf8",
    fg="black",
    padx=12,
).pack(side=tk.LEFT, padx=6)

ausgabe = tk.Text(
    fenster,
    width=54,
    height=19,
    font=("Arial", 10),
    bg="#16325c",
    fg="white",
    wrap="word",
)
ausgabe.pack(pady=10, padx=15)

fenster.mainloop()