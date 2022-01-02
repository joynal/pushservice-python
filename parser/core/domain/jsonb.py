# Setup jsonb encoder/decoder
import json


def jsonb_encoder(value):
    return b'\x01' + json.dumps(value).encode('utf-8')


def jsonb_decoder(value):
    return json.loads(value[1:].decode('utf-8'))
