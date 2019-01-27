from app import verify_program
import unittest


class TestVerifyCompile(unittest.TestCase):
    def setUp(self):
        f = open("compile.py", "r")
        self.compile = f.read()
        f.close()

        f = open("compile2.py", "r")
        self.compile2 = f.read()
        f.close()

        f = open("no_compile.py", "r")
        self.no_compile = f.read()
        f.close()

        f = open("no_compile2.py", "r")
        self.no_compile2 = f.read()
        f.close()

    def test_verify_no_compile(self):
        self.assertEqual(verify_program(self.no_compile), (False, "-", None))

    def test_verify_no_compile2(self):
        self.assertEqual(verify_program(self.no_compile2), (False, "-", None))

    def test_verify_compile(self):
        self.assertEqual(verify_program(self.compile), (True, None, None))

    def test_verify_compile2(self):
        self.assertEqual(verify_program(self.compile2), (True, 4, None))
