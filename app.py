from flask import Flask, render_template, request, jsonify, \
                        make_response, redirect, url_for
import json
import py_compile       # kompilacja programu
import subprocess       # uruchomienie programu

app = Flask(__name__)
client_list = []


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


def verify_program(file_to_compile):
    # print("File to compile: ", len(file_to_compile), ", ", file_to_compile)
    f = open("zapis.py", "w")
    f.write(file_to_compile)
    f.close()

    is_compiled = False
    try:
        # proba kompilacji
        file_to_run = py_compile.compile('zapis.py', cfile=None, dfile=None, doraise=True, optimize=-1)
        is_compiled = True

    except py_compile.PyCompileError:
        # program sie nie kompiluje
        # print("Nie kompiluje sie, nie dobrze !!!")

    except:
        # print("Blad nieznajomego pochodzenia")

    if is_compiled:
        # uruchomienie skompilowanego programu
        proc = subprocess.Popen(file_to_run, stdout=subprocess.PIPE, shell=True)
        (output, error) = proc.communicate()
        print("Output: ", output)

        return is_compiled, output.decode('utf-8'), error

    return is_compiled, "-", None


# obslugiwanie bledow
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/server')
def send_data():
    return render_template('server.html')


@app.route('/client')
def show_blank_client_view():
    msg         = Message()
    client_id   = Message.unique_id

    client_list.append(msg)
    Message.unique_id += 1

    return render_template('client.html',
                           output=" - ",
                           is_compiled=" - ",
                           client_id=client_id)


@app.route('/uploader', methods=['POST'])
def upload_file():
    # print("Reload uploader")
    source_to_compile               = request.files['file']
    client_id                       = request.form.get('client_id', type=int)
    client_list[client_id].source   = source_to_compile.read().decode('utf-8')

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


def obj_dict(obj):
    return obj.__dict__


# API udostepnione dla widoku serwera
@app.route('/conectedClients')
def conectedClients():
    for client in client_list:
        if (client.source is not None) and (client.is_check_by_server is False):
            client_id                                       = client.client_id
            client_list[client_id].is_check_by_server       = True
            source_to_compile                               = client.source
            is_compiled, output, error                      = verify_program(source_to_compile)
            client_list[client_id].program_output           = output
            client_list[client_id].is_compiled              = is_compiled
            client_list[client_id].is_server_has_program    = True

    return make_response(json.dumps(client_list, default=obj_dict))


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='localhost', port=5000)
