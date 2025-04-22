class BlockErrors:
    def __init__(self, err_types):
        self.err_types = tuple(err_types)

    def __enter__(self):
        return selfaimport unittest

class TestBlockErrors(unittest.TestCase):
    def test_ignore_error(self):
        try:
            with BlockErrors({ZeroDivisionError}):
                1 / 0
        except Exception:
            self.fail("ZeroDivisionError не был заглушён")

    def test_propagate_error(self):
        with self.assertRaises(TypeError):
            with BlockErrors({ZeroDivisionError}):
                1 / '0'

    def test_nested(self):
        try:
            with BlockErrors({TypeError}):
                with BlockErrors({ZeroDivisionError}):
                    1 / '0'
        except TypeError:
            pass
        except Exception:
            self.fail("Ошибка не TypeError не была ожидаема")

    def test_subclass(self):
        class MyError(Exception): pass
        try:
            with BlockErrors({Exception}):
                raise MyError()
        except Exception:
            self.fail("Дочерний класс Exception не был заглушён")

if __name__ == '__main__':
    unittest.main()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False
        # isinstance(exc_val, self.err_types) не работает с дочерними классами
        return issubclass(exc_type, self.err_types)
