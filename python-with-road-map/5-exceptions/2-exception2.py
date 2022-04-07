import sys

randomList = ['a', 0, 2]

for entry in randomList:
    try:
        print("the entry is", entry)
        r = 1 / int(entry)
        break
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        print("Next entry")
        print()
print("the reciprocal of ", entry, "is", r)
