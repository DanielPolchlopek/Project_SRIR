from flask import Flask, render_template, request, jsonify, \
                        make_response, redirect, url_for
import json
import py_compile
import subprocess
from werkzeug.datastructures import FileStorage

app = Flask(__name__)


# message = {}
# message['id'] = 2
# json_data = json.dumps(message)
#
#
# message_to_sever = {}
#
#
# message_to_client = {}

client_list = []


class Message(object):
    unique_id = 0

    def __init__(self):
        self.client_id          = self.unique_id
        self.source             = None
        self.is_compiled        = "no determine"
        self.program_output     = "empty"
        self.is_check_by_server = False
        self.is_reload          = 0

    def get_is_compiled(self):
        return self.is_compiled



    def __str__(self):
        return "Id: " + str(self.client_id) + ", source: " + str(self.source) + \
               ", is_compiled: " + str(self.is_compiled) + ", program_output: " + str(self.program_output) + \
                ", is_check_by_server: " + str(self.is_check_by_server)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/change')
def hello_worldert():
    return "Test Ajax"


def verify_program(file_to_compile):
    is_compiled = False
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@: ", file_to_compile)


    # # proba przepisania pliku do innego
    # with open(file_to_compile) as send_file:
    #     print("UDalo sie: ")

    # file = None
    # with open('document-test/test.pdf', 'rb') as fp:
    #     file = FileStorage(fp)
    # file.save('document-test/test_new.pdf')
    #
    # f = open(file_to_compile, 'r')
    # file_to_compile.save('zapis.py')


    try:
        # proba kompilacji
        file_to_run = py_compile.compile('zapis.py', cfile=None, dfile=None, doraise=True, optimize=-1)
        is_compiled = True

    except py_compile.PyCompileError:
        # program sie nie kompiluje
        print("Nie kompiluje sie, nie dobrze !!!")

    except:
        print("Blad nieznajomego pochodzenia")

    if is_compiled:
        # uruchomienie skompilowanego programu
        proc = subprocess.Popen(file_to_run, stdout=subprocess.PIPE, shell=True)
        (output, error) = proc.communicate()
        return is_compiled, output, error

    return is_compiled, None, None

# obslugiwanie bledow
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/server')
def send_data():
    print("Reload server")

    for client in client_list:
        if (client.source is not None) and (client.is_check_by_server is False):
            client_id                                   = client.client_id
            client_list[client_id].is_check_by_server   = True
            source_to_compile                           = client.source
            print("[SERVER] Source: ", source_to_compile)
            is_compiled, output, error                  = verify_program(source_to_compile)
            client_list[client_id].program_output       = output
            client_list[client_id].is_compiled          = is_compiled

            # print("[SERVER] CLIENT_ID: ", client)
            # # client_list[cli]

    return render_template('server.html',
                           client_list=client_list)


@app.route('/client')
def show_blank_client_view():

    print("Reload client")

    msg = Message()
    client_list.append(msg)
    client_id = Message.unique_id
    Message.unique_id += 1

    # print("Client list size: ", len(client_list))
    # for client in client_list:
    #     print(client)

    return render_template('client.html',
                           output=" - ",
                           is_compiled=" - ",
                           client_id=client_id)


# send data to server
# url = 'http://localhost:5000/server'
# data = requests.get(url).json()
# print("Client: ", data)


@app.route('/uploader', methods=['POST'])
def upload_file():

    print("Reload uploader")

    source_to_compile = request.files['file']
    client_id = request.form.get('client_id', type=int)
    client_list[client_id].source = source_to_compile
    source_to_compile.save('zapis.py')
    print("Udalo sie zapisac plik !!!!!!!")

    return redirect(url_for('show_update_client_view', client_id=client_id))


@app.route('/updateClientData')
def show_update_client_view():
    client_id                           = int(request.args['client_id'])
    client_list[client_id].is_reload    = 1

    return render_template('client.html',
                            client_id=client_id,
                            is_reload=client_list[client_id].is_reload,
                            is_compiled=client_list[client_id].is_compiled,
                            output=client_list[client_id].program_output)



@app.route('/actualClientData')
def ssssss():
    print("Ajax wyslal zapytanie !!!!!!!!!!!!!!")
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='localhost', port=5000)

