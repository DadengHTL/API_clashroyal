import random
import requests

# 1. Daten von RoyaleAPI laden
url = "https://royaleapi.github.io/cr-api-data/json/cards.json"
response = requests.get(url)
cards = response.json()

seltenheiten = { # dictory für die Übersetzung der Seltenheiten
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
try: # Fehlerbehandlung für die Eingabe und Ausgabe der Karteninfos
  # 2. Eingabe vom User
  gesucht = input("Suche nach Name (z.B. Knight) ODER Seltenheit (z.B. Selten, Episch) ODER random 8er-Deck generieren(befehl: 8er): ").lower() # in Kleinbuchstaben umwandeln

  # Deutsche Begriffe in die englischen Begriffe der API übersetzen


  # Prüfen, ob der User eine Seltenheit eingegeben hat
  if gesucht in seltenheiten:# Wenn der User eine Seltenheit eingegeben hat, werden alle Karten dieser Seltenheit angezeigt
    englische_seltenheit = seltenheiten[gesucht]# nimmt die englische Seltenheit aus dem Dictionary
    print(f"\n Alle Karten mit Seltenheit '{gesucht}':")# gibt alle Karten mit der gesuchten Seltenheit aus

    for card in cards: # Durchläuft alle Karten
      if card.get("rarity") == englische_seltenheit:# Wenn die Seltenheit der Karte mit der gesuchten Seltenheit übereinstimmt, wird die Karte angezeigt
        print(f"- {card['name']}")

    # Danach nochmal nach dem genauen Namen fragen
    gesucht = input("\n Welche Karte davon möchtest du genauer sehen?: ").lower()
  elif gesucht == "8er": # Wenn der User 8er eingibt, wird ein zufälliges 8er-Deck generiert
    print("\n--- Zufälliges 8er-Deck ---")
    deck = random.sample(cards, 8) # 8 zufällige Karten aus der Liste auswählen
    print(deck)

    for card in deck:
      print(f"- {card['name']} (Seltenheit: {card['rarity']}, Elixier-Kosten: {card['elixir']})")
    exit() # Programm beenden, da das Deck bereits angezeigt wurde


  # 3. Karte nach Namen suchen (läuft immer – egal ob direkt gesucht oder nach der Liste)
  gefundene_karte = None
  for card in cards:
    if gesucht in card["name"].lower():
      gefundene_karte = card
      break

  # 4. Ausgabe der Infos
  if gefundene_karte:# Wenn eine Karte gefunden wurde, werden die Infos ausgegeben(True)
    print(f"\n--- Infos zu {gefundene_karte['name']} ---")
    print(f"Typ: {gefundene_karte.get('type')}")
    print(f"Seltenheit: {gefundene_karte.get('rarity')}")
    print(f"Elixier-Kosten: {gefundene_karte.get('elixir')}")
    print(f"Beschreibung: {gefundene_karte.get('description')}")
    
  else:
    print("Falsche eingabe!")

except Exception:# Wenn ein Fehler auftritt, wird eine Fehlermeldung ausgegeben
  print("Fehler beim Anzeigen der Karteninfos.")