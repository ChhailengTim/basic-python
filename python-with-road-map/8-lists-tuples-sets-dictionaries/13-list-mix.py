list1 = [1, 5, 3, 9, "apple"]
print(list1.index(9))
list2 = [2, 7, 8, 7]
print(list2.index(7))
print(list2.index(7, 2))

tuple1 = (1, 3, 6, 7, 9, 10)
print(tuple1.index(6))
print(tuple1.index(9))

set1 = {1, 5, 6, 3, 9}
# set1.index Error

dict1 = {"key": "value1", "key2": "value2"}
# dict1.index("key1")
print(dict1.get("key1"))
