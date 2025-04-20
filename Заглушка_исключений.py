class BlockErrors:
    def __init__(self, err_types):
        self.err_types = tuple(err_types)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False
        # isinstance(exc_val, self.err_types) не работает с дочерними классами
        return issubclass(exc_type, self.err_types)
