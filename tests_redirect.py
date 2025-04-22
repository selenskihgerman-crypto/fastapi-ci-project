import unittest
import io
import sys

class TestRedirect(unittest.TestCase):
    def test_stdout(self):
        fake_out = io.StringIO()
        with Redirect(stdout=fake_out):
            print("hello")
        self.assertIn("hello", fake_out.getvalue())

    def test_stderr(self):
        fake_err = io.StringIO()
        with Redirect(stderr=fake_err):
            print("err", file=sys.stderr)
        self.assertIn("err", fake_err.getvalue())

    def test_both(self):
        fake_out = io.StringIO()
        fake_err = io.StringIO()
        with Redirect(stdout=fake_out, stderr=fake_err):
            print("stdout!")
            print("stderr!", file=sys.stderr)
        self.assertIn("stdout!", fake_out.getvalue())
        self.assertIn("stderr!", fake_err.getvalue())

    def test_no_args(self):
        with Redirect():
            print("should go to normal stdout")

if __name__ == '__main__':
    unittest.main()
