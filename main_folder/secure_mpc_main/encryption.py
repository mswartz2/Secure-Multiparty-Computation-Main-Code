import sslcrypto


def read_key(filename="keyfile"):
    with open(filename, "rb") as keyfile:
        # Read key from file
        key = keyfile.read()
    return key


class Encryption:
    def __init__(self, key=None):
        # Generate random key
        if key is None:
            self.key = sslcrypto.aes.new_key()
        else:
            self.key = key

    def get_key(self):
        return self.key

    def store_key(self, filename="keyfile"):
        with open(filename, "wb") as keyfile:
            # Writing key to a file
            keyfile.write(self.key)

    def encrypt(self, data):
        ciphertext, iv = sslcrypto.aes.encrypt(data, self.key)
        return ciphertext, iv

    def decrypt(self, ciphertext, iv):
        decrypted = sslcrypto.aes.decrypt(ciphertext, iv, self.key)
        return decrypted
