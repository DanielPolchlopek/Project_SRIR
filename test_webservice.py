from app import verify_program
import unittest


class TestVerifyCompile(unittest.TestCase):
    def setUp(self):
        f = open("compile.py", "r")
        self.compile = f.read()
        f.close()

        f = open("no_compile.py", "r")
        self.no_compile = f.read()
        f.close()

    def test_verify_no_compile(self):
        self.assertEqual(verify_program(self.no_compile), (False, "-", None))

    def test_verify_compile(self):
        self.assertEqual(verify_program(self.compile), (True, "Test-kompilacji\r\n", None))
