import re

class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def restore_tree(log_files):
    nodes = {}  # {value: node}
    children = set()
    root_value = None

    visit_pattern = re.compile(r'Visiting <BinaryTreeNode\[(\d+)\]>')
    left_pattern = re.compile(r'<BinaryTreeNode\[(\d+)\]> left is not empty')
    right_pattern = re.compile(r'<BinaryTreeNode\[(\d+)\]> right is not empty')
    
    for log_file in log_files:
        with open(log_file, 'r') as f:
            for line in f:
                line = line.strip()
                if "Visiting" in line:
                    # Получаем value текущего узла
                    match_visit = visit_pattern.search(line)
                    if match_visit:
                        value = int(match_visit.group(1))
                        if value not in nodes:
                            nodes[value] = BinaryTreeNode(value)
                        # Первым посещенным — предполагаемый корень
                        if root_value is None:
                            root_value = value
                elif "left is not empty" in line:
                    match_left = left_pattern.search(line)
                    if match_left:
                        parent_value = int(re.findall(r'\[(\d+)\]', line)[0])
                        child_value = int(match_left.group(1))
                        # Создаем узлы при необходимости
                        if parent_value not in nodes:
                            nodes[parent_value] = BinaryTreeNode(parent_value)
                        if child_value not in nodes:
                            nodes[child_value] = BinaryTreeNode(child_value)
                        # Связываем
                        nodes[parent_value].left = nodes[child_value]
                        children.add(child_value)
                elif "right is not empty" in line:
                    match_right = right_pattern.search(line)
                    if match_right:
                        parent_value = int(re.findall(r'\[(\d+)\]', line)[0])
                        child_value = int(match_right.group(1))
                        if parent_value not in nodes:
                            nodes[parent_value] = BinaryTreeNode(parent_value)
                        if child_value not in nodes:
                            nodes[child_value] = BinaryTreeNode(child_value)
                        nodes[parent_value].right = nodes[child_value]
                        children.add(child_value)

    # Корень — это узел, не являющийся потомком
    root_value = (set(nodes.keys()) - children).pop()
    return nodes[root_value]

tree_root = restore_tree(['walk_log_1.txt', 'walk_log_2.txt', 'walk_log_3.txt', 'walk_log_4.txt'])
print(tree_root.value if tree_root else "Нет корня")
