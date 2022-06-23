class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __int__(self):
        self.head = None


LL = LinkedList()
LL.head = Node(3)
print(LL.head.data)
