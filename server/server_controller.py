from flask import Flask, render_template, jsonify, make_response, request
import json
from client.client_controller import routes
from model.model import Message

app = Flask(__name__)
app.register_blueprint(routes, template_folder='templates')

client_list = []  # lista przechowujaca wszytskich klientow


def verify_program(file_to_compile):
    is_compiled = False

    try:
        result = eval(compile(file_to_compile, '<string>', 'eval'))
        if result is None:
            result = "-"

        print("Result try: ", result)
        is_compiled = True

    except Exception:
        result = "-"

    return is_compiled, result


def parse_message_from_client(input_json):
    client_json = json.loads(input_json)
    client_data = Message()

    client_data.client_id               = client_json['client_id']
    client_data.source                  = client_json['source']
    client_data.is_compiled             = client_json['is_compiled']
    client_data.program_output          = client_json['program_output']
    client_data.is_check_by_server      = client_json['is_check_by_server']
    client_data.is_reload               = client_json['is_reload']
    client_data.is_server_has_program   = client_json['is_server_has_program']

    return client_data


def update_client_data(client_data):
    source_to_compile                 = client_data.source
    is_compiled, output               = verify_program(source_to_compile)
    client_data.is_check_by_server    = True
    client_data.program_output        = output
    client_data.is_compiled           = is_compiled
    client_data.is_server_has_program = True
    return client_data


# obslugiwanie bledow
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/server')
def show_server_view():
    return render_template('server.html')


# ustawia parsowanie danych z jsona na struktura danych slownik (dictionary)
# funkcja podawana jako argument do innej funkcji
def obj_dict(obj):
    return obj.__dict__


# API udostepnione dla widoku serwera
@app.route('/conectedClients')
def conectedClients():
    return make_response(json.dumps(client_list, default=obj_dict))


# API udostepnione dla clienta - pobieranie id clienta
@app.route('/getClientId')
def getNextClientId():
    client_id         = Message.unique_id
    Message.unique_id = Message.unique_id + 1
    return make_response(json.dumps(client_id, default=obj_dict))


# API udostepnione dla clienta - zwraca zupdatowane dane o kliencie
@app.route('/getDatafromClient', methods=['POST'])
def getDataFromClient():
    input_json      = request.get_json(force=True)
    new_client      = parse_message_from_client(input_json)
    updated_client  = update_client_data(new_client)
    client_list.append(updated_client)

    server_response = {'data_to_client': updated_client.toJSON()}
    return jsonify(server_response)


if __name__ == '__main__':
    app.run(debug=True)
