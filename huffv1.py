import Queue
from collections import Counter
from copy import deepcopy

from tree import *

currentfile = "hamlet.txt"
outfile = "out.txt"
length = 0


def countstuff():
    """
    :return: a dictionary, v=frequency
    """
    with open(currentfile) as myfile:
        data = myfile.read()
    freq = Counter(data)
    return freq


def setfile(fn):
    """
    Better set the file before running anything else
    Default file is hamlet.txt
    """
    global currentfile
    currentfile = fn


# using built-in Priority Queue
def makeTree(mdict):
    q1 = Queue.PriorityQueue()
    for k, v in mdict.items():
        # print Node((v,k,""))
        q1.put((v, Node((v, k, ""))))
    # while(q1.not_empty ):
    #    print q1.get()[1]
    while q1.qsize() != 1:
        i1 = q1.get()[1]
        i2 = q1.get()[1]
        newv = i1.data[0] + i2.data[0]
        # print i1, i2
        i3 = Node((newv, 'i' + str(newv), ""))
        i3.left = i1
        i3.right = i2
        # print i3
        q1.put((newv, i3))
    root = q1.get()
    return root


def markTree(node):
    """add binary codes to the tree """
    # print "FUCKFUCK:", node
    if node.left is None and node.right is None:
        # print node.data[1], node.data[2]

        pass
    elif node.left is not None and node.right is not None:
        # print "markTree:", node
        # print node.right.adddigit('1')
        node.right = node.right.adddigit('1')
        node.left = node.left.adddigit('0')
        markTree(node.right)
        markTree(node.left)


def encode(tree):
    """given an input and a tree, output an encoded string"""
    output = ""
    with open(currentfile) as myfile:
        data = myfile.read()
    for x in data:
        bs = search(tree, x, False).data[2]
        # print bs
        if bs is None:
            print "encode: letter not found. problem."
        else:
            output += bs
    n1 = currentfile.split('.')[0]
    with open(n1 + ".huff.txt", 'w') as wf:
        wf.write(output)
    return output


def decode(instr, tree):
    """given an input and a tree, output a decoded string"""
    node = deepcopy(tree)
    global length
    counter = 0
    output = ""
    levels = [(x + 1) * 5 / 100.0 for x in range(20)]
    clevels = map(lambda x: int(length * x), levels)
    for x in instr:
        # print len(output)
        if node.left is None:
            # print node.data[1]
            output = output.join(node.data[1])
            node = deepcopy(tree)
            counter += 1
            if counter in clevels:
                print counter / (length * 1.0)
        elif x == '0':
            node = node.left
        else:
            node = node.right
            # leaf node must have both children as None


def main():
    # instr = "This is a sample input!?."
    # print len(input)
    root = makeTree(countstuff())
    # print "main:", root[1].left
    # root[1].printNodes()
    markTree(root[1])
    global length
    length = root[0]
    s1 = encode(root[1])
    print s1
    decode(s1, root[1])


if __name__ == "__main__":
    main()
