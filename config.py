import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x97[\xbbvK=\x95\xafC\xc7`\xb9!\x98\xbc\xc0\xf6D\x85\xc5L\xbb\xb6\xb9'