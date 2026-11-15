# What the notebook hid

## 1. What a fresh run could not find
After "Restart and run all" the cleaning cell stops with NameError: name 'known' is not defined. The cell that set known was run once (the saved counts jump from 1 to 3) and then deleted; the name lived on in the kernel's memory, so the notebook kept working for Salma and for nobody else. I added a cell with known = set(district_of) before the cleaning cell.

## 2. The number that the code on screen does not produce
The saved output says 27 anomalies, under a cell that sets factor = 3.0. The what-if cell at the bottom set factor = 2.0 and was run (count 7) before the anomaly cell was run again (count 8), so the 27 belongs to a factor of 2.0. On a clean run from top to bottom the count is 18. I gave the stricter question its own name, strict_factor, so that factor is set in one cell only.
