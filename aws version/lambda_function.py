from hashlib import sha256
import os
import json
import wget
from image_to_ascii import ImageToAscii

def getCode():
    ImageToAscii(imagePath="pure.png", outputFile="ascii.txt")
    f = open("ascii.txt", "r")
    text = f.read()
    os.remove("pure.png")
    os.remove("ascii.txt")
    return sha256(text.encode()).hexdigest()

def lambda_handler(event, context):
    url = event['queryStringParameters']['url']
    caps = event['queryStringParameters']['caps']
    chars = event['queryStringParameters']['chars']
    length = event['queryStringParameters']['length']
    try:
        image = wget.download(str(url), out = "pure.png")
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('error')
        }
    encrypted_string = getCode()[:length]
    if caps == "true":
        encrypted_string = encrypted_string[1:] + "A"
    if chars == "true":
        encrypted_string =  "!"+ encrypted_string[1:]
    return {
            'statusCode': 200,
            'body': json.dumps(encrypted_string)
        }