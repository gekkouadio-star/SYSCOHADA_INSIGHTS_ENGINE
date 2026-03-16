def compute_ratios(data):
    ca = data["CA"]
    rn = data["RN"]
    equity = data.get("Equity", 0)
    debt = data.get("Debt", 0)
    ratios = {}
    ratios["marge_nette"] = (rn/ca)*100 if ca else 0
    ratios["roe"] = (rn/equity)*100 if equity else 0
    ratios["gearing"] = (debt/equity) if equity else 0
    return ratios