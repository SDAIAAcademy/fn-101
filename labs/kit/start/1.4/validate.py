# These lines are one working function, scrambled, with three lines that do not belong.
# Put them in order, indent them, delete the three distractors. Add nothing.
#
# validate_reading(row, known) returns "" for a good row, or the reason it is rejected:
# "MISSING_VALUE" for an empty consumption, "NOT_A_NUMBER" for text that is not a number,
# "OUT_OF_RANGE" below 0 or above 200, "UNKNOWN_METER" when the meter is not in known.
# The checks are made in that order.

return "OUT_OF_RANGE"
except ValueError:
if row["meter_id"] not in known:
value = float(row)
return ""
text = row["consumption_m3"].strip()
if value < 0 and value > 200:
return "NOT_A_NUMBER"
def validate_reading(row, known):
try:
if text == "":
except TypeError:
return "UNKNOWN_METER"
value = float(text)
if value < 0 or value > 200:
return "MISSING_VALUE"
