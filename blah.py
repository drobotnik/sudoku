from collections import Counter
a = [1, 1, 2, 2]
a = Counter(a)
av = 0
for x, y in a.items():
    av += x * y
av = av / sum(a.values())

print(av)