a = ["apple", "banana", "republic"]

for i in range(len(a)):
    for j in range(i+1):
        # i=0 -> j=0
        # i=1 -> j=0, 1
        # i=2 -> j=0, 1, 2
        print(a[i])