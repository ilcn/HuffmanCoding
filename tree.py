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

    def printNodes(self):
        if self.left is not None or self.right is not None:
            self.left.printNodes()
            # print self
            self.right.printNodes()
        elif self.left is None and self.right is None:
            print "PrintNodes:", self


def search(node, data, searchforbitstring):
    if searchforbitstring:
        mycompare = 2
    else:
        mycompare = mycompare1
    """
    :param node: Node object
    :param data: data to be searched for
    :param searchforbitstring: boolean
    :return:
    """
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

            # apparently I don't need delete for now


def printTree(node, depth=0):
    ret = ""

    # Print right branch
    if node.right != None:
        ret += printTree(node.right, depth + 1)

    # Print own value
    ret += "\n" + ("    " * depth) + str(node.data)

    # Print left branch
    if node.left != None:
        ret += printTree(node.left, depth + 1)

    return ret


def mycompare1(d1, d2):
    # print "compare:",d1,d2, d1==d2[1]
    return d1 == d2[1]


def mycompare2(d1, d2):
    return d1 == d2[2]
