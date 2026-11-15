# Pre-work: answers

Every output below was produced by running the snippet. Check your sheet only after you have written all your answers.

## Pre-work 1: Values, names and arithmetic

**1.** `1.5`. / always gives a number with a decimal point.

**2.** `4 2`. // is whole division, % is the remainder.

**3.** `meter-42 / 5`. + joins two strings; len counts characters.

**4.** `0.7420.742`. The quotes make it text. Text times 2 is the text twice.

**5.** `1.484`. float turns the text into a number first.

**6.** `6`. A name can be bound again; += is short for the line above it.

**7.** `error: TypeError: can only concatenate str (not "int") to str`. Text and a number cannot be joined with +. Write str(price), or an f-string.

## Pre-work 2: Conditions

**1.** `normal`. 0.9 is not above 1, so the else branch runs.

**2.** `reject`. The first true condition wins; the others are not looked at.

**3.** `False / True`. Comparison of text is exact: capital letters count.

**4.** `True / False / False`. and needs both sides; not turns True into False.

**5.** `empty`. An empty string counts as false in a condition.

**6.** `error: SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?`. = binds a name, == compares. A condition needs ==.

## Pre-work 3: Loops and lists

**1.** `10 / 20 / 30`. The body runs once for each item.

**2.** `4.0`. The print is outside the loop, so it runs once, at the end.

**3.** `2`. A condition inside a loop: two values are above 200.

**4.** `0 / 1 / 2`. range(3) gives 0, 1 and 2: three numbers, starting at zero.

**5.** `4 6 3`. Positions start at 0; -1 is the last item.

**6.** `3 / 2 / 1 / done`. A while loop runs as long as its condition is true.

**7.** `error: IndentationError: expected an indented block after 'for' statement on line 1`. The body of a loop must be indented.

## Entry quiz

**1.** B. Whole division gives 3, the remainder is 1.

**2.** C. The right side is computed first, then the name is bound to the result.

**3.** C. Both are text, so + joins them.

**4.** B. == compares; = binds a name.

**5.** A. range(4) gives 0, 1, 2, 3.

**6.** D. Positions start at 0.

**7.** C. >= includes the boundary.

**8.** D. Text that is not a number cannot be converted: Python raises a ValueError.

**9.** C. Only the indented line belongs to the if.

**10.** A. The print is after the loop and runs once.
