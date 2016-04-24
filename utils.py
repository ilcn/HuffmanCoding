from Queue import Queue


class Node(object):
    def __init__(self, value, left=None, right=None):
        self.left = left
        self.right = right
        self.data = value

    def __str__(self):
        return "Node: data=" + str(self.data)

    def adddigit(self, digit):
        # print "adddigit:", self.data
        tlist = list(self.data)
        # print tlist
        tlist[2] += digit
        self.data = tuple(tlist)
        if self.left is not None:
            self.left = self.left.adddigit(digit)
            self.right = self.right.adddigit(digit)
        return self

    def print_tree(self):
        if self.left is not None or self.right is not None:
            self.left.print_tree()
            # print self
            self.right.print_tree()
        elif self.left is None and self.right is None:
            print "print_tree:", self

    def get_items(self):
        l1 = []
        if self.left is not None or self.right is not None:
            l1 += self.left.get_items()
            l1 += self.right.get_items()
        elif self.left is None and self.right is None:
            l1.append([self.data[1], self.data[2]])
        return l1


def bfs(node, data, searchforbitstring):
    mycompare = mycompare2 if searchforbitstring else mycompare1
    queue = Queue()
    queue.put(node)
    while queue.not_empty:
        current = queue.get()
        if mycompare(data, current.data) != 0:
            return current
        elif current.left is None:
            continue
        else:
            queue.put(current.left)
            queue.put(current.right)





def search(node, data, searchforbitstring):
    """
        :param node: Node object
        :param data: data to be searched for
        :param searchforbitstring: boolean
        :return:
        """
    mycompare = mycompare2 if searchforbitstring else mycompare1

    # print "searchenter", False==0
    if node is None:
        # print "didn't get anything"
        pass
    elif mycompare(data, node.data) != 0:
        return node
    else:
        l = search(node.left, data, searchforbitstring)
        r = search(node.right, data, searchforbitstring)
        if l is None:
            return r
        else:
            return l


def mycompare1(d1, d2):
    # print "compare:",d1,d2, d1==d2[1]
    return d1 == d2[1]


def mycompare2(d1, d2):
    return d1 == d2[2]
