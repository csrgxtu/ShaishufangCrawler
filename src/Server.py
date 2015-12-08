import subprocess
import os
from flask import Flask, make_response
app = Flask(__name__)

@app.route("/uid/<uid>")
def getIsbns(uid):
    subprocess.call(["./runUID", uid])

    with open(uid + ".csv", 'r') as f:
        body = f.read()

    return body

if __name__ == "__main__":
    app.run(debug=True)
