# Задача 6. Дерево логгеров с logging_tree

import logging_tree
with open('logging_tree.txt', 'w', encoding='utf-8') as f:
    f.write(logging_tree.format.build_description())

