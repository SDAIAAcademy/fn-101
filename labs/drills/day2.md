# Drill 2: lists and dictionaries that share

Ten minutes, on paper, without a computer and without an assistant. Write what each snippet prints.

**1.**

```python
d = {"a": 1}
e = d
e["b"] = 2
print(len(d))
```

**2.**

```python
rows = [{"m": 1}] * 2
rows[0]["m"] = 7
print(rows)
```

**3.**

```python
counts = {}
for word in ["a", "b", "a"]:
    counts[word] = counts.get(word, 0) + 1
print(counts)
```

**4.**

```python
a = [3, 1, 2]
b = sorted(a)
a.sort(reverse=True)
print(a, b)
```

**5.**

```python
t = (1, [2])
t[1].append(3)
print(t)
```
