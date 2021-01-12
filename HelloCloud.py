from flask import Flask
server = Flask(__name__)

@server.route("/")
def hello():
    return "hello r u Okay mai na i sus"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port="80")
