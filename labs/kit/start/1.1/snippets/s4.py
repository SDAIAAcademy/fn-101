def add_reading(log, value):
    log.append(value)
    log = []
    log.append(-1)


day = [1.2]
add_reading(day, 0.8)
print(day)
