class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def restore_tree(path):
    nodes = {}
    children = set()
    with open(path) as f:
        for line in f:
            # Пример строки: "INFO 12:00:00 Visited node 1: left=2, right=3"
            m = re.search(r"node (\d+): left=(\d+|None), right=(\d+|None)", line)
            if m:
                v, l, r = m.groups()
                v = int(v)
                if v not in nodes:
                    nodes[v] = BinaryTreeNode(v)
                node = nodes[v]
                if l != "None":
                    l = int(l)
                    if l not in nodes:
                        nodes[l] = BinaryTreeNode(l)
                    node.left = nodes[l]
                    children.add(l)
                if r != "None":
                    r = int(r)
                    if r not in nodes:
                        nodes[r] = BinaryTreeNode(r)
                    node.right = nodes[r]
                    children.add(r)
    # Root is the node that is not a child
    root_val = (set(nodes.keys()) - children).pop()
    return nodes[root_val]
