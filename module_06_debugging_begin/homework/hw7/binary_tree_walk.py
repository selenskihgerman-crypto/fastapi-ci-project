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
import re


class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def restore_tree_from_logs(log_files_paths):
    nodes = {}  # {значение: объект узла}
    children = set()  # множество значений потомков

    node_pattern = re.compile(r'<BinaryTreeNode$$$(\d+)$$$>')

    for path in log_files_paths:
        with open(path, 'r') as file:
            for line in file:
                if 'Adding' in line:
                    matches = node_pattern.findall(line)
                    if len(matches) == 2:
                        parent_val = int(matches[0])
                        child_val = int(matches[1])

                        # Создаём узлы если их нет
                        if parent_val not in nodes:
                            nodes[parent_val] = BinaryTreeNode(parent_val)
                        if child_val not in nodes:
                            nodes[child_val] = BinaryTreeNode(child_val)
                        children.add(child_val)

                        # Определяем, левый или правый потомок
                        if 'left is not empty' in line:
                            nodes[parent_val].left = nodes[child_val]
                        elif 'right is not empty' in line:
                            nodes[parent_val].right = nodes[child_val]
                        # Если вдруг что-то ещё, просто пропускаем (у нас только left/right)

    # Находим корень
    all_nodes = set(nodes.keys())
    root_candidates = all_nodes - children
    if not root_candidates:
        return None
    root_value = root_candidates.pop()
    return nodes[root_value]

def print_tree_by_levels(root):
    if not root:
        print("Дерево пустое")
        return
    queue = [root]
    while queue:
        node = queue.pop(0)
        print(f"Узел: {node.value}")
        if node.left:
            print(f"  Левый потомок: {node.left.value}")
            queue.append(node.left)
        if node.right:
            print(f"  Правый потомок: {node.right.value}")
            queue.append(node.right)


log_files_paths = ["./walk_log_1.txt"]
root = restore_tree_from_logs(log_files_paths)
print_tree_by_levels(root)
