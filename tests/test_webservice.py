from server.server_controller import verify_program, parse_message_from_client, update_client_data
from model.model import Message
import unittest


# --------------------------------------
# Testy jednostkowe dla servera
# --------------------------------------
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


class TestParseMessageFromClient(unittest.TestCase):
    def setUp(self):
        self.json = "{\"client_id\": 0, \"source\": \"2+2\", \"is_compiled\": true, \"program_output\": 4, \"is_check_by_server\": true, \"is_reload\": 0, \"is_server_has_program\": true}"

        self.msg = Message()
        self.msg.client_id               = 0
        self.msg.source                  = "2+2"
        self.msg.is_compiled             = True
        self.msg.program_output          = 4
        self.msg.is_check_by_server      = True
        self.msg.is_reload               = 0
        self.msg.is_server_has_program   = True

    def test_parse_message_from_client(self):
        self.assertEqual(parse_message_from_client(self.json), self.msg)


# test zawierajacy w sobie inna funkcje wiec to jest takze tekst integracyjny,
# przynajmniej tak mi sie wydaje
class TestUpdateClientData(unittest.TestCase):
    def setUp(self):
        self.basic_msg = Message()
        self.basic_msg.client_id = 0
        self.basic_msg.source = "2+2"
        self.basic_msg.is_compiled = False
        self.basic_msg.program_output = "-"
        self.basic_msg.is_check_by_server = False
        self.basic_msg.is_reload = 0
        self.basic_msg.is_server_has_program = False

        self.update_msg = Message()
        self.update_msg.client_id = 0
        self.update_msg.source = "2+2"
        self.update_msg.is_compiled = True
        self.update_msg.program_output = 4
        self.update_msg.is_check_by_server = True
        self.update_msg.is_reload = 0
        self.update_msg.is_server_has_program = True

    def test_update_client_data(self):
        self.assertEqual(update_client_data(self.basic_msg), self.update_msg)


# --------------------------------------
# Testy jednostkowe dla clienta
# --------------------------------------








