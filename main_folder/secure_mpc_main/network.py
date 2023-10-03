import numpy as np
from scipy.interpolate import lagrange
import socket
import json
import threading

from smpc_secrets import ShamirSecretSharing
from encryption import Encryption, read_key

BYTE_SIZE = 1024


def parse_meta(payload):
    meta = dict()
    for m in payload.split(";"):
        fields = m.split("=")
        if len(fields) == 2:
            meta[fields[0]] = fields[1]

    return meta


def handle_server_data_exchange(meta, node, own_shares, response):
    client = Client(ip=meta.get("node_ip"), port=int(meta.get("node_port")))
    msg = f"method=get_shares_for;node_id={node.id};share_type='f'"
    resp = client.send(msg)
    shares_received = (json.loads(resp)).get("data")
    node.merge_shares_with(own_shares=own_shares, shares=shares_received)
    response["data"] = str(node.shares.get("d"))


def node_callback(connection, config, node, initial_data):
    meta = parse_meta(config.get("data"))
    response = dict()

    if meta.get("method") == "get_shares_for":
        shares = node.get_shares_for(node_id=int(meta.get("node_id")), share_type="f")
        response["data"] = shares.tolist()
        response["status"] = "OK"

    elif meta.get("method") == "create_shares":
        node.shares = dict()
        index = int(meta.get("index"))
        node.create_shares(data=initial_data[index])

    elif meta.get("method") == "merge_shares":
        received_shares = json.loads(meta.get("shares"))
        d = node.merge_shares(shares=received_shares)
        response["data"] = str(d)
        response["status"] = "OK"

    elif meta.get("method") == "merge_with_shares_from":
        own_shares = json.loads(meta.get("shares"))
        t = threading.Thread(
            target=handle_server_data_exchange, args=(meta, node, own_shares, response)
        )
        t.start()
        t.join()

    connection.sendall(bytes(json.dumps(response).encode("utf-8")))


def server_callback(connection, config, node, initial_data):
    meta = parse_meta(config.get("data"))
    response = dict()
    key = read_key()
    encryption = Encryption(key=key)
    print(f"initial_data: {initial_data}")
    print(f"meta: {meta}")

    if meta.get("method") == "send_cipher":
        ciphertext = meta.get("ciphertext")
        if ciphertext is not None and len(ciphertext) > 0:
            total_size = meta.get("total_size")
            print(f"meta: {meta}")
            node.cipher += bytes(bytearray.fromhex(ciphertext))
            print(f"cipher data: {node.cipher}")
            print(f"total size: {total_size}")
        response["status"] = "OK"

    elif meta.get("method") == "send_cipher_iv":
        iv = meta.get("iv")
        node.iv = bytes(bytearray.fromhex(iv))
        print(f"iv: {iv}, node iv: {node.iv}, len: {len(node.iv)}")
        response["status"] = "OK"

    elif meta.get("method") == "send_cipher_completed":
        print(f"completion cipher data: {node.cipher}, {node.iv}")
        cipher = node.cipher
        print(f"bytes cipher: {cipher}")
        print(f"iv: {node.iv}")
        decrypted = encryption.decrypt(ciphertext=cipher, iv=node.iv)
        print(f"decrypted: {decrypted}")
        new_data = np.array(json.loads(decrypted.decode("utf-8")))
        node.data = np.vstack((node.data, new_data)) if len(node.data) > 0 else new_data
        print(f"node data: {node.data}")
        node.cipher = bytes()
        response["status"] = "OK"

    elif meta.get("method") == "receive_centroids" and len(node.data) > 0:
        centroids = node.compute(data=node.data, plot=True, plotname="server-kmeans")
        print(f"computed centroids: {centroids}")
        response["data"] = dict()
        for (i, centroid) in centroids.items():
            response["data"][i] = centroid.tolist()
        response["status"] = "OK"

    elif meta.get("method") == "send_centroid_shares":
        received_shares = json.loads(meta.get("shares"))
        node_id = int(meta.get("node_id"))
        index = int(meta.get("index"))
        print(f"index: {index}")
        centroid = initial_data.get(index)
        print(f"node centroid: {centroid}")
        node.create_shares(data=centroid)
        print(f"node shares: {node.shares}")
        print(f"received shares: {received_shares}")
        print(f"len: {len(node.get_own_shares('f'))}, {len(received_shares)}")
        node.merge_shares(shares=received_shares, by=merge_sum)
        d_to_send = node.get_shares("d")
        g_to_send = node.get_shares_for(node_id=node_id, share_type="f")
        print(f"merged: {node.shares}")
        print(f"shares to send: {d_to_send}")
        response["data"] = dict()
        response["data"]["g"] = json.dumps(g_to_send.tolist())
        response["data"]["d"] = json.dumps(d_to_send.tolist())
        response["data"]["node_id"] = node.id
        response["status"] = "OK"

    elif meta.get("method") == "send_centroid_shares_d":
        received_d = np.array(json.loads(meta.get("d")))
        index = int(meta.get("index"))
        node_d = node.get_shares("d")
        d = np.vstack((received_d, node_d)).T
        node.data["global_centroids"][index] = 0.5 * interpolate(d)
        print(f"d: {d}")
        print(f"node global centroids: {node.data}")
        response["status"] = "OK"

    connection.sendall(bytes(json.dumps(response).encode("utf-8")))


class Client:
    def __init__(self, ip=socket.gethostname(), port=9999, name=""):
        self.name = name
        self.port = port
        self.ip = ip
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, data):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))

        try:
            self.client_socket.sendall(bytes(data.encode("utf-8")))
            payload = self.client_socket.recv(BYTE_SIZE)

            decode = payload.decode("utf-8")
            msg = str(decode)

        finally:
            # self.client_socket.close()
            pass

        # self.client_socket.close()

        return msg


class Server:
    def __init__(self, ip=socket.gethostname(), port=9999):
        self.port = port
        self.ip = ip
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))

    def _handle_server_receive(self, node, callback, initial_data):
        connection, addr = self.server_socket.accept()
        try:
            data = connection.recv(BYTE_SIZE)
            decode = data.decode("utf-8")
            message = str(decode)
            config = dict()
            config["node"] = addr
            config["data"] = message
            callback(connection, config, node, initial_data)

        finally:
            connection.close()
            # pass

    def receive(self, node, callback, initial_data=[]):
        self.server_socket.listen(5)
        print(f"{node.name} ready!")

        while True:
            self._handle_server_receive(
                node=node, callback=callback, initial_data=initial_data
            )


def merge(f, g):
    assert len(f) == len(g), "length mismatch!"
    d = np.array([(f[i] - g[i]) ** 2 for i in range(len(f))])
    return np.sum(d)


def merge_sum(f, g):
    assert len(f) == len(g), "length mismatch!"
    return np.vstack((f, g)).sum(axis=0)


def reconstruct(shares):
    x = np.arange(1, len(shares) + 1)
    y = shares
    f = lagrange(x, y)
    return f(0)


def interpolate(shares):
    result = np.array([])
    for share in shares:
        x = np.arange(1, len(share) + 1)
        y = share
        f = lagrange(x, y)
        result = np.append(result, f(0))
    return result


class NetworkData:
    def __init__(self, name, compute=None):
        self.name = name
        self.data = np.array([])
        self.cipher = bytes()
        self.iv = bytes()
        self.compute = compute


class ShamirShare:
    def __init__(self, name, n, k, node_id):
        self.name = name
        self.n = n
        self.k = k
        self.id = node_id
        self.shares = dict()
        self.data = dict()

    def _get_share_computations(self, n, t, secrets):
        computations = []
        for secret in secrets:
            shamir = ShamirSecretSharing(n=n, t=t)
            shares = shamir.generate(s=secret)
            computations.append((shamir, shares))
        return computations

    def reset_shares(self):
        self.shares = dict()

    def create_shares(self, data, share_type="f"):
        computations = self._get_share_computations(n=self.n, t=self.n, secrets=data)
        f = [computations[i][0].poly for i in range(len(data))]
        print("f")
        shares = [[f[i](j) for i in range(len(f))] for j in range(1, self.n + 1)]

        shares = np.array(shares)
        self.shares[share_type] = shares
        return shares

    def merge_shares(self, shares, by=merge_sum, from_type="f", to_type="d"):
        """
        :param to_type: resulting shares type
        :param from_type: input shares type
        :param by: merging function
        :param shares: shares to merge
        :return: merged shares
        """
        own_shares = self.get_own_shares(share_type=from_type)
        return self.merge_shares_with(
            own_shares=own_shares, shares=shares, by=by, to_type=to_type
        )

    def merge_shares_with(self, own_shares, shares, by=merge_sum, to_type="d"):
        """
        :param own_shares: node's shares
        :param to_type: resulting shares type
        :param by: merging function
        :param shares: shares to merge
        :return: merged shares
        """
        self.shares[to_type] = by(own_shares, shares)
        return self.shares[to_type]

    def get_shares_for(self, node_id, share_type):
        return self.get_shares(share_type=share_type)[node_id - 1]

    def get_shares(self, share_type):
        # takes id of node from which we want the shares
        # returns the shares
        #
        # establish connection with node with 'id' using the port and ip from __init__
        # request the shares
        return self.shares.get(share_type)

    def get_own_shares(self, share_type):
        return self.get_shares_for(node_id=self.id, share_type=share_type)


class NetworkShare:
    def __init__(self, name, node_id, k, n=2):
        """
        :param id: node's id
        :param k: number of participants
        :param n: shamir's polynomial degree
        """
        self.name = name
        self.id = node_id
        self.k = k
        self.n = n
        self.shares = dict()

    def reconstruct_output(self, shares):
        return interpolate(shares)

    def _get_share_computations(self, n, t, secrets):
        computations = []
        for secret in secrets:
            shamir = ShamirSecretSharing(n=n, t=t)
            shares = shamir.generate(s=secret)
            computations.append((shamir, shares))
        return computations

    def create_shares(self, data, share_type="f"):
        """
        :param share_type: the type of shares to create
        :param data: network data
        :return: shares of data
        """
        # returns shares of data
        computations = self._get_share_computations(n=self.n, t=self.n, secrets=data)
        f = [computations[i][0].poly for i in range(len(data))]
        shares = [[f[i](j) for i in range(self.n)] for j in range(1, self.k + 1)]

        shares = np.array(shares)
        self.shares[share_type] = shares

        return self.get_own_shares(share_type=share_type)

    def set_shares(self, shares, share_type):
        self.shares[share_type] = shares

    def merge_shares(self, shares, by=merge, from_type="f", to_type="d"):
        """
        :param to_type: resulting shares type
        :param from_type: input shares type
        :param by: merging function
        :param shares: shares to merge
        :return: merged shares
        """
        own_shares = self.get_own_shares(share_type=from_type)
        return self.merge_shares_with(
            own_shares=own_shares, shares=shares, by=by, to_type=to_type
        )

    def merge_shares_with(self, own_shares, shares, by=merge, to_type="d"):
        """
        :param own_shares: node's shares
        :param to_type: resulting shares type
        :param by: merging function
        :param shares: shares to merge
        :return: merged shares
        """
        self.shares[to_type] = by(own_shares, shares)
        return self.shares[to_type]

    def get_shares_for(self, node_id, share_type):
        return self.get_shares(share_type=share_type)[node_id - 1]

    def get_shares(self, share_type):
        # takes id of node from which we want the shares
        # returns the shares
        #
        # establish connection with node with 'id' using the port and ip from __init__
        # request the shares
        return self.shares.get(share_type)

    def get_own_shares(self, share_type):
        return self.get_shares_for(node_id=self.id, share_type=share_type)


class NetworkNode:
    def __init__(
        self, name, node_id, k, ip=socket.gethostname(), port=9999, n=2, is_server=False
    ):
        self.n = n
        self.k = k
        self.name = name
        self.node_id = node_id
        self.ip = ip
        self.port = port
        self.shares = dict()
        self.node = NetworkShare(name=name, node_id=self.node_id, k=self.k)
        self.is_server = is_server
        self.client = Client(ip=ip, port=port)

    def send(self, data):
        """
        Send shares
        """
        return self.client.send(data)

    def get_shares_for(self, node_id, share_type="f"):
        msg = f"method=get_shares_for;node_id={node_id};share_type={share_type}"
        response = self.send(msg)
        return json.loads(response)

    def merge_shares(self, node_id, shares, share_type):
        msg = f"method=merge_shares;shares={json.dumps(shares.tolist())}"
        response = self.send(msg)
        return json.loads(response)

    def merge_shares_with(self, own_shares, shares):
        msg = f"method=merge_shares_with;own_shares={json.dumps(own_shares.tolist())};shares={json.dumps(shares.tolist())}"
        response = self.send(msg)
        return json.loads(response)

    def merge_with_shares_from(self, node, shares):
        msg = f"method=merge_with_shares_from;node_ip={node.ip};node_port={node.port};shares={json.dumps(shares.tolist())}"
        response = self.send(msg)
        return json.loads(response)

    def create_shares(self, index):
        msg = f"method=create_shares;index={index}"
        response = self.send(msg)
        return json.loads(response)
