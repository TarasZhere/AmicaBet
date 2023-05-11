import os

SERVER_URL = f"http://{os.environ['SERVER_API']}:80/"
# SERVER_URL = "http://{ipaddress here}:80/"

headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
}
