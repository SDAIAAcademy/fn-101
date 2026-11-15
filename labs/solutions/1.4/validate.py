# The three distractors, and why each is wrong:
#   "if value < 0 and value > 200:"  no number is below 0 and above 200 at once: never true
#   "except TypeError:"              float("N/A") raises ValueError, so this catches nothing
#   "value = float(row)"             row is the whole dictionary, not the text of one cell

def validate_reading(row, known):
    text = row["consumption_m3"].strip()
    if text == "":
        return "MISSING_VALUE"
    try:
        value = float(text)
    except ValueError:
        return "NOT_A_NUMBER"
    if value < 0 or value > 200:
        return "OUT_OF_RANGE"
    if row["meter_id"] not in known:
        return "UNKNOWN_METER"
    return ""
