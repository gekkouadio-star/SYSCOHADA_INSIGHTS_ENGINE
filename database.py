import sqlite3
import pandas as pd

DB_FILE = "brvm_data.db"

def initialize_db():
    """Créer la table financials si elle n'existe pas."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financials (
            CA REAL,
            RN REAL,
            Stocks REAL,
            Creances REAL,
            Passif REAL,
            CAF REAL,
            BFR REAL,
            DSO REAL,
            company TEXT,
            year INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_financials(data, company_name, year):
    """Enregistre les données financières dans SQLite."""
    conn = sqlite3.connect(DB_FILE)
    df = pd.DataFrame([{
        "CA": data.get("CA",0),
        "RN": data.get("RN",0),
        "Stocks": data.get("Stocks",0),
        "Creances": data.get("Creances",0),
        "Passif": data.get("Passif circulant",0),
        "CAF": data.get("CAF",0),
        "BFR": data.get("BFR",0),
        "DSO": data.get("DSO",0),
        "company": company_name,
        "year": year
    }])
    df.to_sql("financials", conn, if_exists="append", index=False)
    conn.close()