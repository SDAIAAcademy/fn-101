meter = {"id": "M-0042", "readings": [0.6]}
backup = dict(meter)
backup["id"] = "M-0043"
backup["readings"].append(0.7)
print(meter["id"], meter["readings"])
