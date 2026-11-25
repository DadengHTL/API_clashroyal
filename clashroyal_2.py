import random  # Modul für Zufallsauswahl (z. B. zufälliges 8er-Deck)
import tkinter as tk  # Modul für die grafische Benutzeroberfläche (GUI)
import requests  # Modul zum Herunterladen von Daten aus dem Internet (API)

# 1. Daten von RoyaleAPI laden
url = "https://royaleapi.github.io/cr-api-data/json/cards.json"  # JSON-Quelle mit allen Clash-Royale-Karten
response = requests.get(
    url, timeout=10
)  # Anfrage senden (bricht nach 10 Sek. ab, falls keine Antwort kommt)
response.raise_for_status()  # Löst bei HTTP-Fehlern (z. B. 404 oder 500) eine Ausnahme aus
cards = (
    response.json()
)  # Wandelt die JSON-Antwort in eine Python-Liste mit Karten-Dictionaries um
# hallo
seltenheiten = {  # Übersetzt deutsche und englische Seltenheitsnamen in die englischen API-Werte
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

fenster = tk.Tk()  # Hauptfenster der GUI erstellen
fenster.title(
    "Clash Royale Suche & Deck-Generator"
)  # Titel oben in der Fensterleiste
fenster.geometry("520x540")  # Fenstergröße (Breite x Höhe in Pixeln)
fenster.config(bg="#0f2547")  # Dunkelblaue Hintergrundfarbe des Fensters

tk.Label(  # Überschrift im Fenster anzeigen
    fenster,
    text="CLASH ROYALE SUCHE",
    font=("Arial", 16, "bold"),
    bg="#0f2547",
    fg="#ffcc00",
).pack(
    pady=10
)  # Mit 10 Pixeln vertikalem Abstand platzieren

tk.Label(  # Hinweistext für die Eingabe anzeigen
    fenster,
    text="Name (z. B. Pekka), Seltenheit (z. B. Selten, Episch) oder '8er':",
    bg="#0f2547",
    fg="white",
).pack()

eingabe = tk.Entry(
    fenster, width=36, font=("Arial", 12), justify="center"
)  # Einzeiliges Eingabefeld für den Nutzer
eingabe.pack(pady=8)


def zeige_karten_info(karte):  # Gibt alle wichtigen Details einer Karte im Textfeld aus
  ausgabe.insert(tk.END, f"--- Infos zu {karte['name']} ---\n")
  ausgabe.insert(tk.END, f"Typ: {karte.get('type')}\n")
  ausgabe.insert(tk.END, f"Seltenheit: {karte.get('rarity')}\n")
  ausgabe.insert(tk.END, f"Elixier-Kosten: {karte.get('elixir')}\n")
  ausgabe.insert(tk.END, f"Beschreibung: {karte.get('description')}\n")


def generiere_8er_deck():  # Erstellt ein zufälliges Deck aus 8 verschiedenen Karten und berechnet den Schnitt
  ausgabe.delete("1.0", tk.END)  # Vorherigen Text im Ausgabefeld löschen
  ausgabe.insert(tk.END, "--- Zufälliges 8er-Deck ---\n\n")

  deck = random.sample(cards, 8)  # Zieht 8 zufällige Karten ohne Wiederholung
  gesamt_elixier = 0  # Zähler für die Summe aller Elixierkosten

  for card in deck:  # Jede der 8 gezogenen Karten durchgehen
    elixier = card.get(
        "elixir", 0
    )  # Elixierwert holen (Standard 0, falls Schlüssel fehlt)
    gesamt_elixier += elixier  # Elixierkosten zur Gesamtsumme addieren
    ausgabe.insert(  # Karte mit Seltenheit und Elixier ins Textfeld schreiben
        tk.END,
        f"- {card['name']} (Seltenheit: {card.get('rarity')}, "
        f"Elixier-Kosten: {elixier})\n",
    )

  schnitt = (
      gesamt_elixier / len(deck)
  )  # Durchschnittliches Elixier des Decks berechnen
  ausgabe.insert(
      tk.END, f"\nDurchschnitts-Elixier: {schnitt:.2f}"
  )  # Auf 2 Nachkommastellen gerundet ausgeben


def suchen(
    event=None,
):  # Haupt-Suchfunktion (event=None erlaubt Aufruf per Klick und per Enter-Taste)
  ausgabe.delete("1.0", tk.END)  # Bisherige Ausgabe leeren
  gesucht = (
      eingabe.get().strip().lower()
  )  # Eingabe lesen, Leerzeichen entfernen und in Kleinbuchstaben wandeln

  if not gesucht:  # Prüfen, ob das Eingabefeld leer ist
    ausgabe.insert(
        tk.END,
        "Bitte gib einen Kartennamen, eine Seltenheit oder '8er' ein.",
    )
    return  # Funktion hier vorzeitig beenden

  if gesucht == "8er":  # Sonderbefehl für zufälliges 8er-Deck
    generiere_8er_deck()
    return

  if (
      gesucht in seltenheiten
  ):  # Prüfen, ob nach einer Seltenheit gesucht wurde
    englische_seltenheit = seltenheiten[
        gesucht
    ]  # Passenden englischen Seltenheitswert nachschlagen
    ausgabe.insert(tk.END, f"Alle Karten mit Seltenheit '{gesucht}':\n\n")

    treffer = [  # Liste aller Karten mit der gewählten Seltenheit erstellen
        card for card in cards if card.get("rarity") == englische_seltenheit
    ]
    for card in treffer:  # Jeden Treffer zeilenweise ausgeben
      ausgabe.insert(tk.END, f"- {card['name']}\n")

    ausgabe.insert(  # Hinweis für den nächsten Schritt anzeigen
        tk.END,
        "\nWelche Karte davon möchtest du genauer sehen? (Oben eingeben)",
    )
  else:  # Sonst nach einem Kartennamen suchen
    gefundene_karte = None  # Speichert den ersten passenden Kartentreffer
    for card in cards:  # Alle Karten durchsuchen
      if (
          gesucht in card["name"].lower()
      ):  # Teilstring-Suche ohne Groß-/Kleinschreibung
        gefundene_karte = card
        break  # Suche abbrechen, sobald ein Treffer gefunden wurde

    if gefundene_karte:  # Falls eine Karte gefunden wurde, Details anzeigen
      zeige_karten_info(gefundene_karte)
    else:  # Falls keine passende Karte gefunden wurde
      ausgabe.insert(tk.END, "Karte wurde nicht gefunden!")


eingabe.bind(
    "<Return>", suchen
)  # Drücken der Enter-Taste im Eingabefeld löst suchen() aus

button_rahmen = tk.Frame(
    fenster, bg="#0f2547"
)  # Container, um Buttons nebeneinander anzuordnen
button_rahmen.pack(pady=5)

tk.Button(  # Button zum Starten der Suche
    button_rahmen,
    text="Suchen",
    command=suchen,
    font=("Arial", 11, "bold"),
    bg="#ffcc00",
    fg="black",
    padx=12,
).pack(side=tk.LEFT, padx=6)

tk.Button(  # Button zum direkten Erstellen eines zufälligen 8er-Decks
    button_rahmen,
    text="Zufälliges 8er-Deck",
    command=generiere_8er_deck,
    font=("Arial", 11, "bold"),
    bg="#38bdf8",
    fg="black",
    padx=12,
).pack(side=tk.LEFT, padx=6)

ausgabe = tk.Text(  # Mehrzeiliges Textfeld für Ergebnisse, Listen und Decks
    fenster,
    width=54,
    height=19,
    font=("Arial", 10),
    bg="#16325c",
    fg="white",
    wrap="word",  # Umbricht lange Zeilen an Wortgrenzen statt mitten im Wort
)
ausgabe.pack(pady=10, padx=15)

fenster.mainloop()  # Startet die Ereignisschleife, damit das Fenster offen bleibt und auf Klicks/Eingaben reagiert