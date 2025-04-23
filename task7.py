class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def restore_tree(logs):
    node_dict = {}
    for log in logs:
        value = log['value']
        node_dict[value] = BinaryTreeNode(value)

    for log in logs:
        value = log['value']
        if log['left'] is not None:
            node_dict[value].left = node_dict[log['left']]
        if log['right'] is not None:
            node_dict[value].right = node_dict[log['right']]

    return node_dict[logs[0]['value']]  # корень

# Пример использования
# logs = [{'value': 1, 'left': 2, 'right': 3}, ...]
# root = restore_tree(logs)
