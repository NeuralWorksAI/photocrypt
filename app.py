from flask import Flask
from flask_restful import Resource, Api, reqparse
from hashlib import sha256
import os
import wget
from image_to_ascii import ImageToAscii

app = Flask(__name__)
api = Api(app)

def getCode():
    ImageToAscii(imagePath="pure.png", outputFile="ascii.txt")
    f = open("ascii.txt", "r")
    text = f.read()
    os.remove("pure.png")
    os.remove("ascii.txt")
    return sha256(text.encode()).hexdigest()

parser = reqparse.RequestParser()
parser.add_argument('url', required=True, type=str)
parser.add_argument('caps', required=True, type=str)
parser.add_argument('chars', required=True, type=str)
parser.add_argument('length', required=True, type=int)

class PassCode(Resource):
    def get(self):
        args = parser.parse_args()
        url = args['url']
        caps = args['caps']
        chars = args['chars']
        length = args['length']
        try:
            image = wget.download(str(url), out = "pure.png")
        except:
            return {'code': 'error'}, 400, {'Access-Control-Allow-Origin': '*'}
        encrypted_string = getCode()[:length]
        if caps == "true":
            encrypted_string = encrypted_string[1:] + "A"
        if chars == "true":
            encrypted_string =  "!"+ encrypted_string[1:]
        return {'code': encrypted_string}, 200, {'Access-Control-Allow-Origin': '*'}

api.add_resource(PassCode, '/')