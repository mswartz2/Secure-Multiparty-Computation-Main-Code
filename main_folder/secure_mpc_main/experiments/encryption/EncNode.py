from encryption import Encryption, read_key
import json
from kmeans import chunks

splits = {"100%": 1, "50%": 2}


def receive_centroids(node):
    response = node.send(f"method=receive_centroids")
    print(f"centroids: {response}")


def send_encrypted(node, raw_data, split_size, node_id):
    d = len(raw_data) // splits[split_size]  # 50% split
    data = raw_data[:d] if node_id == 1 else raw_data[d:]
    data = json.dumps(data.tolist())

    # Encrypt data
    key = read_key()
    encryption = Encryption(key=key)

    ciphertext, iv = encryption.encrypt(bytes(data.encode('utf-8')))

    # server
    chunk_size = 25
    total_size = len(ciphertext)

    response = node.send(f"method=send_cipher_iv;iv={iv.hex()}")

    for (index, chunk) in chunks(ciphertext, chunk_size=chunk_size):
        msg = f"method=send_cipher;total_size={total_size};chunk_size={chunk_size};index={index};ciphertext={chunk.hex()}"
        response = node.send(msg)

    response = node.send(f"method=send_cipher_completed")
    print(f"completion response: {response}")
