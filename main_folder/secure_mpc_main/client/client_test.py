import json
import socket
import argparse
import os
from secrets import AdditiveSecretSharing, ShamirSecretSharing

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER_IP = "192.168.1.101"
SERVER_PORT = 9999

#Client1 = 192.168.1.102
#Client2 = 192.168.1.103
#Client3 = 192.168.1.104

def print_usage():
    print("Either we send the secret and number of clients via -secret flag and -num_clients flags, or recieve our secret via -client")
    print("Usage: python3 client_test.py -secret <numb> -num_clients <number of clients> | -client <number_of_client>")

#TODO Assuming that we already know where data.json is...
def update_shares(clientid, share):
    print('updating clientid ', clientid)
    print('with share: ', share)
    shares = get_shares()
    shares[clientid] = share
    new_shares = {}
    new_shares["shares"] = shares

    with open("data.json", "w") as outfile:
        json.dump(new_shares, outfile, indent=4)

#TODO Instead request clientID from server... update  right now send it in via arg
def calc_addition(secret, n, clientid):
    shares = []
    additive_sharing = AdditiveSecretSharing(n=n)
    shares = additive_sharing.generate(s=secret)
    s = additive_sharing.reconstruct(shares=shares)
    # print(f"secret: {secret}")
    # print(f"shares: {shares}")
    # print(f"reconstructed: {s}")

    update_shares(clientid,shares[clientid])
    return shares

def get_shares():
    stored = {}
    filename = "data.json"
    if not os.path.exists(filename):
        with open(filename, 'w'): pass

    with open(filename, "r") as json_file:
        try:
            stored = json.load(json_file)
        except json.decoder.JSONDecodeError: pass
        print("Reading stored data file: ", stored.get("shares"))
    return stored.get("shares")

def add_shares(data):
    stored = json.loads(data)
    shares = stored.get("shares")
    sumpoint=0
    for share in shares:
        sumpoint = sumpoint + share

    return sumpoint


#TODO: Calculate secret shares on CLIENT itself, and share those with SERVER. These will stored on server in data.json{..."shares":{"1":[1,2,3],"2":[x,x,x]..}}
#TODO: Later.. Change CLIENT Request a LIST of their shares from all client(s) [f0, g0, r0] instead of requesting individually..?
#TODO: CLIENT SUMs Shares as SUMPOINT 
#TODO: CLIENT POST SUMPOINT - POST to server in data.json{..."sumpoints":[123,x,x]}} ie, POST 123 = data.sumpoints[client_id=val]
#TODO: CLIENT GET LIST SUMPOINT(s) - Store locally data.json{..."sumpoints":[123,145,132]} or somewhere else
#TODO: CLIENT Calculates Sum of SUMPOINT(s) - 123 + 145 + 132 = 400
#TODO: CLIENT now has SUM
#TODO: How should CLIENT know all other clients have POSTED SUMPOINT???  Assume?
parser = argparse.ArgumentParser(description='Set?| up API calls to server via TCP.')
parser.add_argument('-secret', type=int, help='Secret to share')
parser.add_argument('-num_clients', type=int, help='Number of clients')
parser.add_argument('-client', type=int, help='Client number to get a share')
parser.add_argument('-client_id', type=int, help='Our client ID, 1,2,3')
parser.add_argument('-sumpoint', type=argparse.FileType('r'))
parser.add_argument('-get_sumpoints', action='store_true', help='flag to GET sumpoints from server', default=False)


args = parser.parse_args()
if not args.client and not args.secret:
    print_usage()

api_calls = {}
msg = ""
#TODO: Save our share based on our clientID instead of hard coding ID
#TODO: Still servers all shares to SERVER... remove our clientID from being shared.
if args.secret and args.num_clients and args.client_id:

    ret_list = calc_addition(args.secret, args.num_clients, args.client_id-1)
    req = {}
    req["shares"]= ret_list
    req_msg = json.dumps(req)
    content_length = len(req_msg)
    msg += "POST /shares HTTP/1.0\r\nHost: "+SERVER_IP+"\r\nContent-Length: {0}\r\n\r\n{1}".format(content_length, req_msg)

elif args.client:
    msg += "GET /receive?client="+str(args.client)+" HTTP/1.0\r\nHost: "+SERVER_IP+"\r\n\r\n"

elif args.sumpoint:
    gson = json.dumps(
        json.load(args.sumpoint),
        indent=4,
        sort_keys=True
    )
    sumpoint = add_shares(gson)
    req = {}
    req["sumpoint"]= sumpoint
    req_msg = json.dumps(req)
    content_length = len(req_msg)

    msg += "POST /sumpoint HTTP/1.0\r\nHost: "+SERVER_IP+"\r\nContent-Length: {0}\r\n\r\n{1}".format(content_length, req_msg)

elif args.get_sumpoints:
    msg += "GET /receive?sumpoints="+str(args.client)+" HTTP/1.0\r\nHost: "+SERVER_IP+"\r\n\r\n"

else:
    print_usage()
    exit()

# print(msg)
try:
    client_socket.connect((SERVER_IP, SERVER_PORT))
    client_socket.sendall(bytes(msg.encode("utf-8")))
    data = client_socket.recv(1024)

    decode = data.decode("utf-8")
    if decode:
        message = str(decode)
        if "share" in message:
            data_dict = json.loads(message)
            c_id = int(data_dict["target_id"])
            c_id = c_id -1
            update_shares(c_id, data_dict["share"])

        if "sumpoints" in message:
            data_dict = json.loads(message)

            SUM = 0
            for point in data_dict['sumpoints']:
                SUM = SUM + point

            print("TOTAL SUM: ", SUM)

finally:
    client_socket.close()

