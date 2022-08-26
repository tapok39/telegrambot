import operator
d = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
result = dict(sorted(d.items(), key=operator.itemgetter(1)))
result2 = dict(sorted(d.items(), key=operator.itemgetter(1), reverse=True))
print(result, result2)

