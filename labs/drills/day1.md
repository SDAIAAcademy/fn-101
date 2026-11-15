# Drill 1: predict the output

Ten minutes, on paper, without a computer and without an assistant. Write what each snippet prints.

**1.**

```python
a = [1, 2]
b = a
b = b + [3]
print(a, b)
```

**2.**

```python
s = "meter"
t = s
t = t.upper()
print(s, t)
```

**3.**

```python
x = [1, 2, 3]
y = x
y[0] = 99
x = [0]
print(x, y)
```

**4.**

```python
def reset(values):
    values = []
    return values


data = [5]
reset(data)
print(data)
```

**5.**

```python
def clear(values):
    values.clear()


data = [5]
clear(data)
print(data)
```
