import json


class Message(object):
    unique_id = 0

    def __init__(self):
        self.client_id              = self.unique_id
        self.source                 = None
        self.is_compiled            = "no determine"
        self.program_output         = "empty"
        self.is_check_by_server     = False
        self.is_reload              = 0
        self.is_server_has_program  = False

    def get_is_compiled(self):
        return self.is_compiled

    def __str__(self):
        return "Id: " + str(self.client_id) + ", source: " + str(self.source) + \
               ", is_compiled: " + str(self.is_compiled) + ", program_output: " + str(self.program_output) + \
                ", is_check_by_server: " + str(self.is_check_by_server)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

