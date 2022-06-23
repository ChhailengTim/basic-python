testSet = {1, 2, 3}
print(testSet, 'length is', len(testSet))

# Empty Set
testSet = set()
print(testSet, 'length is', len(testSet))

testDict = {1: 'one', 2: 'two'}
print(testDict, 'length is', len(testDict))

testDict = {}
print(testDict, 'length is', len(testDict))

testSet = {1, 2}
# frozenSet
frozenTestSet = frozenset(testSet)
print(frozenTestSet, 'length is', len(frozenTestSet))