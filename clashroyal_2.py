import random  # Modul für Zufallsauswahl (z. B. zufälliges 8er-Deck)
import tkinter as tk  # Modul für die grafische Benutzeroberfläche (GUI)
import requests  # Modul zum Herunterladen von Daten aus dem Internet (API)

# 1. Kartendaten von RoyaleAPI laden
URL = "https://royaleapi.github.io/cr-api-data/json/cards.json"  # JSON-Quelle mit allen Karten
response = requests.get(URL, timeout=10)  # HTTP-Anfrage mit 10 Sek. Timeout senden
response.raise_for_status()  # Bei HTTP-Fehlern (z. B. 404/500) direkt abbrechen
cards = response.json()  # Wandelt JSON in eine Liste aus Karten-Dictionaries um

# Übersetzungstabelle für deutsche/englische Seltenheiten auf den API-Wert
SELTENHEITEN = {
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


def zeige_karten_info(karte):# es gibt eine Funktion, die alle wichtigen Details einer einzelnen Karte im Ausgabefeld ausgibt
  """Gibt alle wichtigen Details einer einzelnen Karte im Ausgabefeld aus."""
  ausgabe.insert(tk.END, f"--- Infos zu {karte['name']} ---\n")
  ausgabe.insert(tk.END, f"Typ: {karte.get('type')}\n")
  ausgabe.insert(tk.END, f"Seltenheit: {karte.get('rarity')}\n")
  ausgabe.insert(tk.END, f"Elixier-Kosten: {karte.get('elixir')}\n")
  ausgabe.insert(tk.END, f"Beschreibung: {karte.get('description')}\n")


def generiere_8er_deck():
  """Zieht 8 zufällige Karten ohne Dopplungen und berechnet das Durchschnitts-Elixier."""
  ausgabe.delete("1.0", tk.END)  # Bisherigen Text im Ausgabefeld löschen
  ausgabe.insert(tk.END, "--- Zufälliges 8er-Deck ---\n\n")

  deck = random.sample(cards, 8)  # 8 verschiedene Karten zufällig auswählen

  # Jede Karte ausgeben und ihre Elixierkosten in einer einzigen Schleife aufsummieren
  gesamt_elixier = 0
  for card in deck:
    elixier = card.get("elixir") or 0  # Falls kein Elixier vorhanden ist (z. B. None/0), 0 nutzen
    gesamt_elixier += elixier
    ausgabe.insert( # Karte in das Ausgabefeld einfügen
        tk.END,
        f"- {card['name']} (Seltenheit: {card.get('rarity')}, "
        f"Elixier-Kosten: {elixier})\n",
    )

  schnitt = gesamt_elixier / len(deck)  # Durchschnittliches Elixier des 8er-Decks berechnen
  ausgabe.insert(tk.END, f"\nDurchschnitts-Elixier: {schnitt:.2f}")  # Auf 2 Nachkommastellen runden


def finde_karte_nach_name(suchtext):
  """Sucht die erste Karte, deren Name den Suchtext (ohne Groß-/Kleinschreibung) enthält."""
  for card in cards:  # Alle Karten nacheinander durchsuchen
    if suchtext in card.get("name", "").lower():  # Prüfen, ob Suchtext im Namen steckt
      return card  # Erste passende Karte direkt zurückgeben
  return None  # Falls keine Karte passt, None zurückgeben


def suchen(event=None):
  """Verarbeitet die Nutzereingabe (8er-Deck, Seltenheitsliste oder Kartensuche)."""
  ausgabe.delete("1.0", tk.END)  # Vorherige Ausgabe entfernen
  gesucht = eingabe.get().strip().lower()  # Eingabe bereinigen und in Kleinbuchstaben wandeln

  if not gesucht:  # Leere Eingabe abfangen
    ausgabe.insert(
        tk.END, "Bitte gib einen Kartennamen, eine Seltenheit oder '8er' ein."
    )
    return

  if gesucht == "8er":  # Direkter Befehl für ein zufälliges Deck
    generiere_8er_deck()
    return

  if gesucht in SELTENHEITEN:  # Eingabe ist eine bekannte Seltenheit
    englische_seltenheit = SELTENHEITEN[gesucht]
    ausgabe.insert(tk.END, f"Alle Karten mit Seltenheit '{gesucht}':\n\n")

    # Normale Schleife: Geht alle Karten durch und gibt nur passende Seltenheiten aus
    for card in cards:
      if card.get("rarity") == englische_seltenheit:
        ausgabe.insert(tk.END, f"- {card['name']}\n")

    ausgabe.insert(
        tk.END, "\nWelche Karte davon möchtest du genauer sehen? (Oben eingeben)"
    )
    return

  # Standardfall: Nach einem Kartennamen suchen und Details anzeigen
  karte = finde_karte_nach_name(gesucht)
  if karte:
    zeige_karten_info(karte)
  else:
    ausgabe.insert(tk.END, "Karte wurde nicht gefunden!")


# --- Aufbau der grafischen Benutzeroberfläche (GUI) ---
fenster = tk.Tk()  # Hauptfenster erstellen
fenster.title("Clash Royale Suche & Deck-Generator")  # Fenstertitel setzen
fenster.geometry("520x540")  # Fenstergröße festlegen
fenster.config(bg="#0f2547")  # Dunkelblauer Hintergrund

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
eingabe.bind("<Return>", suchen)  # Enter-Taste im Eingabefeld startet ebenfalls die Suche

button_rahmen = tk.Frame(fenster, bg="#0f2547")  # Rahmen für nebeneinander liegende Buttons
button_rahmen.pack(pady=5)

tk.Button(  # knopf für die Suche nach Kartenname/Seltenheit
    button_rahmen,
    text="Suchen",
    command=suchen,
    font=("Arial", 11, "bold"),
    bg="#ffcc00",
    fg="black",
    padx=12,
).pack(side=tk.LEFT, padx=6)

tk.Button( # knopf für die Generierung eines zufälligen 8er-Decks
    button_rahmen,
    text="Zufälliges 8er-Deck",
    command=generiere_8er_deck,
    font=("Arial", 11, "bold"),
    bg="#38bdf8",
    fg="black",
    padx=12,
).pack(side=tk.LEFT, padx=6)

ausgabe = tk.Text( # knopf für die Ausgabe der Karteninfos und des 8er-Decks
    fenster,
    width=54,
    height=19,
    font=("Arial", 10),
    bg="#16325c",
    fg="white",
    wrap="word",  # Zeilenumbrüche an Wortgrenzen
)
ausgabe.pack(pady=10, padx=15)

fenster.mainloop()  # Startet die GUI-Schleife und wartet auf Nutzeraktionen