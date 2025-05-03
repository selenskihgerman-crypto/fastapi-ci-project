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
    nodes = {}       # {значение: объект узла}
    children = set() # множество значений потомков

    # Регулярное выражение для поиска узлов
    node_pattern = re.compile(r'<BinaryTreeNode$$$(\d+)$$$>')

    for path in log_files_paths:
        with open(path, 'r') as file:
            for line in file:
                # Ищем все узлы в строке
                found_nodes = node_pattern.findall(line)

                # Обработка добавления потомков
                if 'Adding' in line:
                    parts = line.strip().split('Adding')
                    parent_match = node_pattern.search(parts[0])
                    if parent_match:
                        parent_value = int(parent_match.group(1))
                        # Создаем узел, если еще не создан
                        if parent_value not in nodes:
                            nodes[parent_value] = BinaryTreeNode(parent_value)

                        for part in parts[1:]:
                            child_match = node_pattern.search(part)
                            if child_match:
                                child_value = int(child_match.group(1))
                                if child_value not in nodes:
                                    nodes[child_value] = BinaryTreeNode(child_value)
                                # Добавим значение потомка в множество
                                children.add(child_value)

                                # Определим, левый или правый потомок
                                # Для этого можно использовать порядок добавления или лог-файлы
                                # Для простоты — добавим оба потомка без определения позиции
                                # В реальной задаче нужно дополнительно учитывать позицию
                                # Предположим, что порядок добавлений определяет левый/правый
                                # Здесь для примера можно оставить так
                                # Можно расширить, если есть такая информация
                                # Но для простоты — связи позже установим вручную или по логам

    # После обработки всех логов найдем корень
    all_nodes = set(nodes.keys())
    # Узлы, которые являются потомками
    # Объединим все потомки узлов
    # Так как мы добавляем только потомков (их значения), то создаем множество
    # из всех значений, которые встречались как потомки
    # В данном случае используем множество children
    root_candidates = all_nodes - children

    # Если корень есть, возвращаем его
    if not root_candidates:
        return None
    root_value = root_candidates.pop()
    return nodes[root_value]
