from functools import reduce
import base64
import json

config = {}

def encode_domain(data: bytes) -> str:
    assert len(data) <= 100, "data is longer than 100 bytes"
    f = filter(lambda it: len(it) > 0, [data[0:25], data[25:50], data[50:75], data[75:100]])
    m = map(lambda it: it.hex(), list(f))
    return "x" + (".x".join(list(m)))


def decode_domain(data: str) -> bytes:
    s = data.split(".")
    m = map(lambda it: bytes.fromhex(it[1:]), s)
    return reduce(lambda a, b: a + b, list(m), b'')


def encode_txt(data: bytes) -> str:
    assert len(data) <= 100, "data is longer than 100 bytes"
    return base64.b64encode(data).decode()


def decode_txt(data: str) -> bytes:
    return base64.b64decode(data)

def load_config():
    global config
    with open("../config/config.json", "r") as config_file:
        config = json.loads( "".join(config_file.readlines()) )
    return config

if __name__ == '__main__':
    data = b'1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    encode = encode_domain(data)
    print(encode)
    decode = decode_domain(encode)
    print(decode)
    assert data == decode

    encode = encode_txt(data)
    print(encode)
    decode = decode_txt(encode)
    print(decode)
    assert data == decode
