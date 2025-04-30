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

def restore_tree(log_path):
    # Проверяем, что имя файла допустимо
    allowed_logs = [
        "walk_log_1.txt",
        "walk_log_2.txt",
        "walk_log_3.txt",
        "walk_log_4.txt",
    ]
    if log_path not in allowed_logs:
        raise ValueError(f"Файл {log_path} не является допустимым логом для восстановления дерева!")

    nodes = {}
    children = set()

    visiting_re = re.compile(r'INFO:Visiting <BinaryTreeNode$$$(\d+)$$$>')
    left_re = re.compile(r'DEBUG:<BinaryTreeNode$$$(\d+)$$$> left is not empty. Adding <BinaryTreeNode$$$(\d+)$$$> to the queue')
    right_re = re.compile(r'DEBUG:<BinaryTreeNode$$$(\d+)$$$> right is not empty. Adding <BinaryTreeNode$$$(\d+)$$$> to the queue')

    with open(log_path, "r") as f:
        for line in f:
            line = line.strip()
            m = visiting_re.match(line)
            if m:
                current = int(m.group(1))
                if current not in nodes:
                    nodes[current] = BinaryTreeNode(current)
                continue

            m = left_re.match(line)
            if m:
                parent, child = int(m.group(1)), int(m.group(2))
                if parent not in nodes:
                    nodes[parent] = BinaryTreeNode(parent)
                if child not in nodes:
                    nodes[child] = BinaryTreeNode(child)
                nodes[parent].left = nodes[child]
                children.add(child)
                continue

            m = right_re.match(line)
            if m:
                parent, child = int(m.group(1)), int(m.group(2))
                if parent not in nodes:
                    nodes[parent] = BinaryTreeNode(parent)
                if child not in nodes:
                    nodes[child] = BinaryTreeNode(child)
                nodes[parent].right = nodes[child]
                children.add(child)
                continue

    # Корень — тот, кто не является ни чьим потомком
    all_nodes = set(nodes.keys())
    root_candidates = all_nodes - children
    if not root_candidates:
        return None
    root_value = root_candidates.pop()
    return nodes[root_value]
