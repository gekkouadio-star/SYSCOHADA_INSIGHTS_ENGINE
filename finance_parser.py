import re

def extract_finance_syscohada(text):
    def parse_metric(pattern):
        matches = re.findall(pattern + r".*?([\d\s\.,\(\)-]+)", text, re.IGNORECASE)
        for m in matches:
            digits = re.sub(r"\D", "", m)
            if digits == "":
                continue
            value = int(digits)
            if value > 100000:
                return value
        return 0

    ca = parse_metric("Chiffre d.?Affaires")
    rn = parse_metric("Résultat net")
    stocks = parse_metric("Stocks")
    creances = parse_metric("Créances")
    passif = parse_metric("Passif circulant")
    caf = parse_metric("Capacité d.?autofinancement")

    bfr = stocks + creances - passif
    dso = (creances / ca) * 360 if ca else 0

    return {
        "CA": ca,
        "RN": rn,
        "Stocks": stocks,
        "Creances": creances,
        "Passif circulant": passif,
        "CAF": caf,
        "BFR": bfr,
        "DSO": dso
    }