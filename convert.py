import pandas as pd
import json
import math

def excel_to_json(excel_file, json_output_file):
    # 1. Excel-Datei einlesen (wir überspringen die ersten Zeilen bis zur echten Kopfzeile)
    # Da "Titel" in Zeile 10 oder ähnlich steht, sucht pandas automatisch nach der Zeile.
    df = pd.read_excel(excel_file, skiprows=1) # Eventuell anpassen, falls nötig
    
    # Spaltennamen bereinigen
    df.columns = [str(c).strip() for c in df.columns]
    
    # Nur Zeilen behalten, die einen Titel haben
    df = df.dropna(subset=['Titel'])
    
    ergebnis = []
    
    # 2. Festlegen, welches die Info-Spalten sind
    info_spalten = ['Titel', 'Link', 'Beschreibung']
    
    # Alle anderen Spalten danach sind potenzielle Kategorien
    alle_spalten = list(df.columns)
    kategorie_spalten = [c for c in alle_spalten if c not in info_spalten and not c.startswith('Unnamed')]

    for _, row in df.iterrows():
        # Basis-Daten extrahieren
        titel = row.get('Titel', '')
        link = row.get('Link', '')
        beschreibung = row.get('Beschreibung', '')
        
        # Wenn Link oder Beschreibung NaN (leer) sind, zu Leerstring machen
        if pd.isna(link): link = ''
        if pd.isna(beschreibung): beschreibung = ''
        
        # Jetzt prüfen, in welchen Kategorie-Spalten ein "Ja" steht
        aktive_kategorien = []
        for kat in kategorie_spalten:
            wert = str(row.get(kat, '')).strip().lower()
            if wert == 'ja':
                aktive_kategorien.append(kat)
        
        # Objekt für diese Firma bauen
        firma = {
            "titel": str(titel).strip(),
            "link": str(link).strip(),
            "beschreibung": str(beschreibung).strip(),
            "kategorien": aktive_kategorien
        }
        ergebnis.append(firma)
        
    # 3. Als JSON-Datei speichern
    with open(json_output_file, 'w', encoding='utf-8') as f:
        json.dump(ergebnis, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully converted {len(ergebnis)} entries to {json_output_file}!")

# Skript ausführen
if __name__ == "__main__":
    # Name deiner Excel-Datei hier eintragen!
    excel_to_json("Linkliste.xlsx", "Linkliste.json")