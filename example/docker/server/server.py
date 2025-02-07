from flask import Flask

import os

app = Flask(__name__)

def get_value (default = 0):
    if os.path.exists("value.txt"):
        with open("value.txt", "r") as file:
            return int(file.read())
    return default
def set_value (value: int):
    with open("value.txt", "w") as file:
        file.write(str(value))

@app.route('/')
def hello():
    value = get_value()
    set_value(value + 1)
    return f'Hello, World {value} !'