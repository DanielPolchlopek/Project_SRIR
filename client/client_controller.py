from flask import render_template, request, redirect, url_for
import json
import requests
from model.model import Message

from flask import Blueprint
routes = Blueprint('routes', __name__, template_folder='templates')


# funkcja pobierajaca od serwera wolne nastepne dostepne id klienta
def getClientId():
    url = "http://localhost:5000/getClientId"
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"

    Jresponse = uResponse.text
    client_id = json.loads(Jresponse)
    return client_id


# funkcja pobierajaca od serwera zupdateowane dane o kliencie
def getUpdatedClientData(client_id, source_to_compile):
    msg = Message()
    msg.client_id = client_id
    msg.source = source_to_compile.read().decode('utf-8')

    response = requests.post('http://localhost:5000/getDatafromClient', json=msg.toJSON())
    response_from_server = response.json()
    response_from_server = response_from_server['data_to_client']

    return response_from_server


@routes.route('/client')
def show_blank_client_view():
    client_id = getClientId()

    return render_template('client.html',
                           output=" - ",
                           is_compiled=" - ",
                           client_id=client_id)


def parse_message_from_server(input_json):
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


@routes.route('/uploader', methods=['POST'])
def upload_file():
    source_to_compile = request.files['file']
    client_id         = request.form.get('client_id', type=int)

    response_from_server = getUpdatedClientData(client_id, source_to_compile)

    return redirect(url_for('routes.show_update_client_view', client=response_from_server))


@routes.route('/updateClientData')
def show_update_client_view():
    client2 = request.args['client']
    client  = parse_message_from_server(client2)

    return render_template('client.html',
                           client_id=client.client_id,
                           is_reload=client.is_reload,
                           is_compiled=client.is_compiled,
                           output=client.program_output)

