import json
import os
import ast
import socket
from secrets import AdditiveSecretSharing, ShamirSecretSharing

IP = "192.168.1.101"
PORT = 9999
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
server_socket.bind((IP, PORT))


def get_secret(data_msg):
    return data_msg.split(" ")[1].split("=")[1]

def get_return_ip(connection):
    return connection.getpeername()


def get_req_args(req_msg):
    req_params = req_msg.split("\r\n\r\n")[1]
    req_dict = json.loads(req_params)
    print("REQ params: ", req_params)
    print("REQ dict: ", req_dict)
    return req_dict

def get_client_id(sender_ip, stored):
    clients = stored.get("clients")
    if clients:
        for client, value in clients.items():
            if value == sender_ip:
                user = client
                if user:
                    return user
    return None

def get_secret_shares(client_id, stored):
    secrets = stored.get("secrets")

    for secret_id, value in secrets.items():
        if secret_id  == client_id:
            client_shares = value
            if client_shares:
                return client_shares

    return None

def get_target_share(target_id, client_id, stored):

    secrets = stored.get("secrets")
    for secret_id, value in secrets.items():
        if secret_id == target_id:
            return_share = value[int(client_id)-1]
            if return_share:
                return return_share
    return None

def replace_secret_shares(client_id, stored, shares):
    secrets = stored.get("secrets")
    secrets[client_id] = shares
    return stored

def replace_sumpoint(clientid, stored, sumpoint):
    c_id = int(clientid)
    c_id = c_id-1

    sumpoints = stored.get("sumpoints")
    sumpoints[c_id] = sumpoint
    return stored

def update_storage(updated_shares):
    with open("data.json", "w+") as outfile:
        json.dump(updated_shares, outfile, indent=4)

def get_sumpoints(connection, data_msg, stored):
    target_id = get_secret(data_msg)
    ret_ip = get_return_ip(connection)
    client_id = get_client_id(ret_ip[0],stored)
    ret_sumpoints = stored['sumpoints']

    retval = {}
    retval["sumpoints"] = ret_sumpoints
    if client_id:
        if ret_sumpoints:
            connection.sendall(bytes(json.dumps(retval).encode("utf-8")))
        else:
            connection.sendall(bytes("nothing to send, something may be broken!".encode("utf-8")))

            def get_api(connection, data_msg, stored):
    target_id = get_secret(data_msg)
    ret_ip = get_return_ip(connection)

    #GET Index for share access
    client_id = get_client_id(ret_ip[0],stored)

    ret_share = get_target_share(target_id, client_id, stored)

    retval = {}
    retval["share"] = ret_share
    retval["target_id"] = target_id
    if client_id:
        if ret_share:
            connection.sendall(bytes(json.dumps(retval).encode("utf-8")))
        else:
            connection.sendall(bytes("nothing to send, something may be broken!".encode("utf-8")))
        #The following in case we want to get all shares a certain client generated..
        #secret_shares = get_secret_shares(client_id, stored)
        #if secret_shares:
        #    connection.sendall(bytes(json.dumps(secret_shares).encode("utf-8")))
        #else:
        #    connection.sendall(bytes("Nothing to send, did the target client POST their secret to generate shares?".encode("utf-8")))

def post_api(connection, data_msg):
    data = get_req_args(data_msg)
    shares = data.get('shares')
    ret_ip = get_return_ip(connection)

    client_id = get_client_id(ret_ip[0],stored)

    updated_shares = replace_secret_shares(client_id, stored, shares)
    update_storage(updated_shares)

    if client_id:
        connection.sendall(bytes("updated the secret".encode("utf-8")))

    else:
        connection.sendall(bytes("nothing to send, something broken??".encode("utf-8")))

#TODO: Store the sumpoint on server in data.json(":sumpoints")
def post_api_sumpoint(connection, data_msg):
    data = get_req_args(data_msg)
    sumpoint = data.get("sumpoint")
    ret_ip = get_return_ip(connection)
    client_id = get_client_id(ret_ip[0], stored)

    updated_sumpoint = replace_sumpoint(client_id, stored, sumpoint)
    update_storage(updated_sumpoint)

    if client_id:
          connection.sendall(bytes("updated spoint for client".encode("utf-8")))
    else:
        connection.sendall(bytes("something didn't work when updating spoint".encode("utf-8")))


def get_req(req):
    reqs = req.split(" ")
    req_method = reqs[0]
    req_path = reqs[1]
    return req_method, req_path

def get_stored_data():
    stored = {}
    filename = "data.json"
    if not os.path.exists(filename):
        with open(filename, 'w'): pass

    with open(filename, "r") as json_file:
        try:
            stored = json.load(json_file)
        except json.decoder.JSONDecodeError: pass
    return stored

while True:
    server_socket.listen()
    connection, client_address = server_socket.accept()
    stored = get_stored_data()
    try:
        data = connection.recv(1024)
        decode = data.decode("utf-8")
        message = str(decode)
        req_method, req_path = get_req(message)
        if req_method == "GET" and "/receive?client=" in req_path:
            get_api(connection, message, stored)

        elif req_method == "GET" and "/receive?sumpoints=" in req_path:
            get_sumpoints(connection, message, stored)

        elif req_method == "POST" and req_path == "/shares":
            post_api(connection, message)

        elif req_method == "POST" and req_path =="/sumpoint":
            post_api_sumpoint(connection, message)

        connection.close()
    finally:
        connection.close()
