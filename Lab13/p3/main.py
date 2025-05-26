from functools import reduce

data = [1, 21, 75, 39, 7, 2, 35, 3, 31, 7, 8]

filtered = list(filter(lambda x: x >= 5, data))

pairs = list(zip(filtered[0::2], filtered[1::2]))

products = list(map(lambda p: p[0] * p[1], pairs))

total = reduce(lambda a, b: a + b, products, 0)

print("Filtered (>=5):", filtered)
print("Pairs:", pairs)
print("Products:", products)
print("Sum of products:", total)
