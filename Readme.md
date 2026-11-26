# Clash Royale Karten-Suche & Deck-Generator

Ein kleines Python-Programm, mit dem du Clash-Royale-Karten suchen, nach Seltenheit filtern oder ein zufälliges 8er-Deck erstellen kannst. Die Kartendaten kommen live von RoyaleAPI.

## Funktionen

- **Nach Name suchen:** Gib einen Kartennamen (z. B. `Knight` oder `Pekka`) ein, um Typ, Seltenheit, Elixier-Kosten und Beschreibung anzuzeigen.
- **Nach Seltenheit filtern:** Gib z. B. `Selten`, `Episch`, `Legendär` oder `Champion` ein, um alle passenden Karten zu sehen und danach eine davon genauer auszuwählen.
- **Zufälliges 8er-Deck (`8er`):** Erstellt 8 zufällige Karten mit Elixier-Kosten und berechnet das Durchschnitts-Elixier.

## Voraussetzungen & Start

1. `requests` installieren:
   ```bash
   pip install requests