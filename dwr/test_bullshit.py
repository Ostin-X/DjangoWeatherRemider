def increment(x):
    return x + 1


x = [1, 2, 3]
y = map(increment, x)
y1 = map(lambda b: b + 1, x)

print(increment(1))
print(y)
print(y1)
print(y == y1)
print(list(y))
print(list(y1))
