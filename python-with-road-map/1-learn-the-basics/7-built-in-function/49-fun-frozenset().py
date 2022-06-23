# Frozensets
# initialize A and B
A = frozenset([1, 2, 3, 4])
B = frozenset([3, 4, 5, 6])

# copying a frozenset
C = A.copy()  # Output: frozenset({1, 2, 3, 4.txt})
print(C)

# union
print(A.union(B))  # Output: frozenset({1, 2, 3, 4.txt, 5, 6})

# intersection
print(A.intersection(B))  # Output: frozenset({3, 4.txt})

# difference
print(A.difference(B))  # Output: frozenset({1, 2})

# symmetric_difference
print(A.symmetric_difference(B))  # Output: frozenset({1, 2, 5, 6})