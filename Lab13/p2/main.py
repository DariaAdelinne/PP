from more_itertools import map_reduce
import string

text = """
Functional programming in Python este un stil de codare care pune accent
pe folosirea functiilor pure, immutable data si expresii lambda. Astfel,
codul devine mai concis si mai usor de testat.
"""

words = [
    w.strip(string.punctuation).lower()
    for w in text.split()
    if w.strip(string.punctuation)
]

groups = map_reduce(
    words,
    lambda w: w[0]
)

print("Grupuri simple:")
for letter, group in sorted(groups.items()):
    print(f"{letter} → {group}")

groups_counts = map_reduce(
    words,
    lambda w: w[0],
    lambda w: 1,
    sum
)

print("\nNumar aparitii per litera:")
for letter, count in sorted(groups_counts.items()):
    print(f"{letter} → {count}")
