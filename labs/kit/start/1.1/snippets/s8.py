def tag(reading, tags=[]):
    tags.append(reading)
    return tags


first = tag("high")
second = tag("low")
print(first, second, first is second)
