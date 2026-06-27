import pandas as pd
import json

def excel_to_javascript(excel_file, js_output_file):
    # 1. Excel-Datei einlesen (wir überspringen die ersten Zeilen bis zur echten Kopfzeile)
    df = pd.read_excel(excel_file, skiprows=1) 
    
    # Spaltennamen von Leerzeichen befreien
    df.columns = [str(c).strip() for c in df.columns]
    
    # Nur Zeilen behalten, die einen Titel haben
    df = df.dropna(subset=['Titel'])
    
    ergebnis = []
    
    # Festlegen, welches die Info-Spalten sind
    info_spalten = ['Titel', 'Link', 'Beschreibung']
    
    # Alle anderen Spalten danach sind potenzielle Kategorien
    alle_spalten = list(df.columns)
    kategorie_spalten = [c for c in alle_spalten if c not in info_spalten and not c.startswith('Unnamed')]

    for _, row in df.iterrows():
        titel = row.get('Titel', '')
        link = row.get('Link', '')
        beschreibung = row.get('Beschreibung', '')
        
        if pd.isna(link): link = ''
        if pd.isna(beschreibung): beschreibung = ''
        
        # Prüfen, in welchen Kategorie-Spalten ein "Ja" steht
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
        
    # 3. Als JavaScript-Datei mit einer globalen Variable speichern
    with open(js_output_file, "w", encoding="utf-8") as f:
        f.write("const firmaData = ")
        json.dump(ergebnis, f, ensure_ascii=False, indent=2)
        f.write(";")
        
    print(f"Erfolgreich {len(ergebnis)} Einträge in '{js_output_file}' konvertiert!")

# Skript ausführen
if __name__ == "__main__":
    # HIER ist die Anpassung: Wir übergeben jetzt "daten.js" als Zieldatei
    excel_to_javascript("Linkliste.xlsx", "linkliste.js")