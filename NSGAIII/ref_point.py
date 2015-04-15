
def get_ref_points(root):
    ref_points = []
    assert(root.data == -1 and root.level == 0), "Supplied node is not root"
    visited, stack = set(), [root]
    count = 0
    while len(stack) != 0:
        vertex = stack.pop()
        if vertex not in visited:
            if len(vertex.children) == 0:
                temp = vertex
                points = []
                while temp is not None:
                    points = [round(temp.data, 2)] + points
                    temp = temp.parent
                ref_points.append(points)
            stack.extend(vertex.children)
            visited.add(vertex)
    return ref_points

class Node(object):
    def __init__(self, data=-1, level=0, parent = None):
        self.data = data
        self.level = level
        self.children = []
        self.parent = parent

    def add_child(self, obj):
        self.children.append(obj)

def tree(node, n, p, level = 0):
    if level == 0:
        from numpy import arange
        for i in [j for j in arange(0, 1 + 10e-10, 1/p)]:
            node.add_child(Node(i, level + 1))
        for child in node.children:
            tree(child, n, p, level + 1)
    elif level < (n - 1):
        other_beta = 0

        # Traversing up the tree to get other values of beta
        temp = node
        while temp is not None:
            other_beta += temp.data
            temp = temp.parent

        k = (1 - other_beta)/(1/p)
        from numpy import arange
        for i in [j for j in arange(0, k * (1/p) + 10e-10, (1/p))]:
            node.add_child(Node(i, level + 1, node))
        for child in node.children:
            tree(child, n, p, level + 1)
    elif level == (n -1):
        other_beta = 0
        # Traversing up the tree to get other values of beta
        temp = node
        while temp is not None:
            other_beta += temp.data
            temp = temp.parent
        node.add_child(Node(1-other_beta, level + 1, node))

    else:
        return

def cover(n, p):
    from scipy.misc import comb
    combination = comb(n + p - 1, p)
    root = Node(-1)
    tree(root, n, p)
    lst = get_ref_points(root)
    assert(len(lst) == combination), "Length of the lst should be equal to combination"
    for l in lst:
        assert(round(sum(l), 1) == 1), "sum of l should be 1"
    return lst

# -------------------------- Testing -------------------------- #

def _get_ref_points():
    for x in xrange(100):
        print ".",
        import random
        a = random.randint(3, 7)
        b = random.randint(a, 10)
        cover(a, b)


if __name__ == "__main__":
     _get_ref_points()