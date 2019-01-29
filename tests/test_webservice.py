from server.server_controller import verify_program
import unittest


class TestVerifyCompile(unittest.TestCase):
    def setUp(self):
        f = open("..\\example_program\\compile.py", "r")
        self.compile = f.read()
        f.close()

        f = open("..\\example_program\\compile2.py", "r")
        self.compile2 = f.read()
        f.close()

        f = open("..\\example_program\\no_compile.py", "r")
        self.no_compile = f.read()
        f.close()

        f = open("..\\example_program\\no_compile2.py", "r")
        self.no_compile2 = f.read()
        f.close()

    def test_verify_no_compile(self):
        self.assertEqual(verify_program(self.no_compile), (False, "-"))

    def test_verify_no_compile2(self):
        self.assertEqual(verify_program(self.no_compile2), (False, "-"))

    def test_verify_compile(self):
        self.assertEqual(verify_program(self.compile), (True, "-"))

    def test_verify_compile2(self):
        self.assertEqual(verify_program(self.compile2), (True, 4))
