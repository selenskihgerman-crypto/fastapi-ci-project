"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""
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
