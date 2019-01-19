from flask import Flask, render_template, request, jsonify, make_response
import json
import py_compile
import subprocess

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
        self.client_id = self.unique_id
        self.source = "empty"
        self.is_compiled = "no determine"
        self.program_output = "empty"

    def __str__(self):
        return "Id: " + str(self.client_id) + ", source: " + str(self.source) + \
               ", is_compiled: " + str(self.is_compiled) + ", program_output: " + str(self.program_output)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/change')
def hello_worldert():
    return "Test Ajax"


def verify_program(file_to_compile):
    is_compiled = False
    msg = request.files.get('file')

    print("Code: ", msg)
    file_to_compile.save('zapis.py')

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
        # print("program output:", output, ", ", error)
        return is_compiled, output, error

    return is_compiled, None, None

# obslugiwanie bledow
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/server')
def send_data():
    print("Reload server")
    output = "testprzesylu"
    is_compiled = False
    is_sent = False
    is_received_code = False
    sent_program = []

    return render_template('server.html',
                           output=output,
                           is_compiled=is_compiled,
                           sent_program=sent_program,
                           is_sent=is_sent,
                           is_received_code=is_received_code)


@app.route('/client')
def show_blank_client_view():
    msg = Message()
    client_list.append(msg)
    Message.unique_id += 1

    print("Client list size: ", len(client_list))
    for client in client_list:
        print(client)

    return render_template('client.html',
                           output="output",
                           is_compile=False,
                           client_id=(Message.unique_id-1))


@app.route('/uploader', methods=['POST'])
def upload_file():
    file_to_compile = request.files['file']
    client_id = request.form.get('client_id', type=int)

    is_compiled, output, error = verify_program(file_to_compile)
    print("Compile: ", is_compiled,
          "output: ", output,
          "error: ", error,
          "client_id: ", client_id)

    # send data to server
    # url = 'http://localhost:5000/server'
    # data = requests.get(url).json()
    # print("Client: ", data)


    return render_template('client.html',
                           output="Waiting for data from server",
                           is_compile="Waiting for data from server",
                           client_id=client_id)


if __name__ == '__main__':
    app.run(debug=True)

