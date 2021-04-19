from flask import Flask, make_response, jsonify
from hashlib import sha256
import os
import wget
from image_to_ascii import ImageToAscii

app = Flask(__name__)

def getCode():
    ImageToAscii(imagePath="pure.png", outputFile="ascii.txt")
    f = open("ascii.txt", "r")
    text = f.read()
    os.remove("pure.png")
    os.remove("ascii.txt")
    return sha256(text.encode()).hexdigest()

@app.route('/<path:url>/<string:caps>/<string:chars>/<int:length>',methods=['GET'])
def landingPage(url, caps, chars, length):
    image = wget.download(str(url), out = "pure.png")
    encrypted_string = getCode()[:length]
    if caps == "true":
        encrypted_string = encrypted_string[1:] + "A"
    if chars == "true":
        encrypted_string =  "!"+ encrypted_string[1:]
    resp = make_response(jsonify(
        code=encrypted_string
    ))
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp