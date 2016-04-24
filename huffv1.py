import getopt
import os
import struct
import sys
import time
from Queue import PriorityQueue
from copy import deepcopy

from utils import *

read_file = ".\\texts\\hamlet.txt"
out_file = ""
huff_file = ""
report_file = ""
length_counter = 0
BYTE_LENGTH = 8
table_length = 0
nl = 0


def count_multiple(symbol_length):
    """
    Count pairs of symbols.
    :return: a dictionary, v=frequency
    """
    counts = dict()
    with open(read_file) as mf:
        while True:
            c = mf.read(symbol_length)
            counts[c] = counts.get(c, 0) + 1
            if not c:
                break
    return counts


def set_file(v1, my_file=None):
    """
    :param my_file: file name without extension
    :param v1: True if using v1
    """
    table_length = 0
    global read_file, out_file, huff_file, report_file
    if my_file is None or not os.path.isfile(".\\texts\\" + my_file + ".txt"):
        print "set_file: You have not set custom files, or my_file does not exist. Using hamlet"
        if v1:
            out_file = ".\\output\\v1\\hamlet.out.txt"
            huff_file = ".\\output\\v1\\hamlet.huff.txt"
            report_file = ".\\output\\v1\\hamlet.report.txt"
        else:
            out_file = ".\\output\\v2\\hamlet.out.txt"
            huff_file = ".\\output\\v2\\hamlet.huff.txt"
            report_file = ".\\output\\v2\\hamlet.report.txt"
    else:
        read_file = ".\\texts\\" + my_file + ".txt"
        if v1:
            out_file = ".\\output\\v1\\" + my_file + ".out.txt"
            huff_file = ".\\output\\v1\\" + my_file + ".huff.txt"
            report_file = ".\\output\\v1\\" + my_file + ".report.txt"
        else:
            out_file = ".\\output\\v2\\" + my_file + ".out.txt"
            huff_file = ".\\output\\v2\\" + my_file + ".huff.txt"
            report_file = ".\\output\\v2\\" + my_file + ".report.txt"


# using built-in Priority Queue
def make_tree(mdict):
    q1 = PriorityQueue()
    for k, v in mdict.items():
        # print Node((v,k,""))
        q1.put((v, Node((v, k, ""))))
    # while(q1.not_empty ):
    #    print q1.get()[1]
    while q1.qsize() != 1:
        i1 = q1.get()[1]
        i2 = q1.get()[1]
        new_value = i1.data[0] + i2.data[0]
        # print i1, i2
        i3 = Node((new_value, 'i' + str(new_value), ""))
        i3.left = i1
        i3.right = i2
        # print i3
        q1.put((new_value, i3))
    root = q1.get()
    return root


def mark_tree(node):

    """add binary codes to the tree """
    if node.left is None and node.right is None:
        # print node.data[1], node.data[2]

        pass
    elif node.left is not None and node.right is not None:
        # print "mark_tree:", node
        # print node.right.adddigit('1')
        node.right = node.right.adddigit('1')
        node.left = node.left.adddigit('0')
        mark_tree(node.right)
        mark_tree(node.left)


def write_table(l1):
    global nl

    with open(huff_file, 'wb') as wf:
        for [k, v] in l1:
            if '\n' in k: nl += 1
            wf.write(k)
            wf.write(v)
        wf.write('\n')
    global table_length
    table_length = os.stat(huff_file).st_size


def encode(tree, symbol_length):
    """given an input and a tree, output an encoded string"""
    global BYTE_LENGTH, read_file, out_file, huff_file
    print "encode: start encoding"
    counter = 0
    # write table
    l1 = tree.get_items()
    write_table(l1)
    with open(read_file) as mf, open(huff_file, 'ab') as wf:
        bs = ""
        while True:
            x = mf.read(symbol_length)
            if not x:
                break
            bs += bfs(tree, x, False).data[2]
            if bs is None:
                print "encode: letter not found. problem."
            else:
                for i in range(len(bs) / (BYTE_LENGTH + 1) + 1):
                    if len(bs) >= BYTE_LENGTH:
                        buff = bs[:BYTE_LENGTH]
                        bs = bs[BYTE_LENGTH:]
                        wf.write(struct.pack('B', int(buff, 2)))
                        counter += 1
                    elif 0 < len(bs) < BYTE_LENGTH:
                        pass
                    else:
                        print "encode: shouldn't have 0 or less length"
                        # print buffer, sys.getsizeof(buffer)
    print "encode: result written to file", out_file


def decode(tree, symbol_length):
    """given an input and a tree, output a decoded string"""
    print "decode: start decoding"
    node = deepcopy(tree)

    with open(huff_file, "rb")as rf, open(out_file, "w") as wf:
        for i in range(nl + 2):
            rf.readline()
        byte = rf.read(1)
        while byte != "":
            bs = struct.unpack('B', byte)[0]
            for i in range(7, -1, -1):
                if node.left is None:
                    # print  node.data[1]
                    wf.write(node.data[1])
                    node = deepcopy(tree)
                if check_bit(int(bs), i):  # a zero
                    node = node.right
                else:
                    node = node.left
            byte = rf.read(1)


def set_total_length(i):
    global length_counter
    length_counter = i


def check_bit(byte_val, idx):
    return (byte_val & (1 << idx)) != 0


def report(ts):
    print "------------------REPORT------------------"
    with open(report_file, 'w') as mf:
        mf.write("File name: %s\nSize: %d bytes\nAfter Huffman encoding: %d bytes\n"
                 % (read_file, os.stat(read_file).st_size, os.stat(huff_file).st_size))
        mf.write("Table(s) length: %d bytes\n" % table_length)
        cr = float(os.path.getsize(huff_file)) / float(os.path.getsize(read_file))
        mf.write("Compression ratio: %f\n" % cr)
        mf.write("Making and marking tree took time: %ds\nEncoding took time: %ds\nDecoding took time: %ds\n"
                 % (ts[1] - ts[0], ts[2] - ts[1], ts[3] - ts[2]))
    with open(report_file, 'r') as mf:
        print (mf.read())


def get_read():
    return read_file


def main(argv, variant):
    # this deals with command line input
    try:
        opts, args = getopt.getopt(argv, "hi:v:")
    except getopt.GetoptError:
        print 'exception: do huffv%d.py -i <input_file> -v <version>' % variant
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'help:\nhuffv%d.py -i <input_file(no extension) -v <version>>' % variant
            sys.exit()
        elif opt in ("-i"):
            set_file(True, arg)
        elif opt in ("-v"):
            variant = int(arg)

    set_file(variant == 2, "a_book_on_biology")
    ts = [time.clock()]
    root = make_tree(count_multiple(variant))
    # root[1].print_tree()
    mark_tree(root[1])
    set_total_length(root[0])
    ts.append(time.clock())
    encode(root[1], variant)
    ts.append(time.clock())
    print table_length
    # print s1
    decode(root[1], variant)
    ts.append(time.clock())
    report(ts)


if __name__ == "__main__":
    main(sys.argv[1:], 1)
