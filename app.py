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


@app.route('/')
def hello_world():
    print("Hello")
    return render_template('index.html')


@app.route('/change')
def hello_worldert():
    return "Test Ajax"


def verify_program():


    return "Ciekawe"


@app.route('/uploader', methods=['POST'])
def upload_file():

    # pobranie pliku
    file_to_compile = request.files['file']

    isCompiled = False
    msg = request.files.get('file')

    print("Code: ", msg)
    file_to_compile.save('zapis.py')

    try:
        # proba kompilacji
        file_to_run = py_compile.compile('zapis.py', cfile=None, dfile=None, doraise=True, optimize=-1)
        isCompiled = True

        # uruchomienie skompilowanego programu
        proc = subprocess.Popen(file_to_run, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        print("program output:", out, ", ", err)

    except py_compile.PyCompileError:
        # program sie nie kompiluje
        print("Nie kompiluje sie, nie dobrze !!!")

    except:
        print("Blad nieznajomego pochodzenia")

    if isCompiled:
        return "Kompiluje sie"

    return "Nie kompiluje sie :/ "


# obslugiwanie bledow
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/server')
def send_data():
    print("Start server")
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
def recive_data():
    # url = 'http://localhost:5000/server'
    # data = requests.get(url).json()
    # print("Client: ", data)

    output = "output"
    is_compile = False

    # print("Client list size: ", len(client_list))
    # for client in client_list:
    #     print(client)


    return render_template('client.html',
                           output=output,
                           is_compile=is_compile)


if __name__ == '__main__':
    app.run(debug=True)

