import os
import json
from dotenv import load_dotenv
from flask import Flask, request
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
from list_serve import WushuEmail

load_dotenv()
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
mongo_server_url = os.environ.get("MONGODB_URL")
app.client = MongoClient(mongo_server_url)
db = app.client[os.environ.get("DB_NAME")]
list_serv_members = db[os.environ.get("LISTSERV_MEMBERS_COLLECTION")]


@app.route("/")
@cross_origin()
def init():
    return json.dumps("Welcome to Cornell Wushu Server")


@app.route("/add_listserv_member", methods=["POST"])
@cross_origin()
def add_listserv_member():
    body = json.loads(request.data)
    list_serv_members.create_index("email", unique=True)
    resp = list_serv_members.insert_one(body)
    return json.dumps(resp, default=str)


@app.route("/get_listserv_members")
@cross_origin()
def get_listserv_members():
    resp = list(list_serv_members.find())
    return json.dumps(resp, default=str)


@app.route("/remove_listserv_member", methods=["POST"])
@cross_origin()
def remove_listserv_members():
    body = json.loads(request.data)
    resp = list_serv_members.delete_one(body)
    return json.dumps(resp, default=str)


@app.route("/send_email", methods=["POST"])
@cross_origin()
def send_email():
    body = json.loads(request.data)
    try:
        if body.get("sendAll"):
            receivers = [member["email"] for member in list_serv_members.find()]
        else:
            receivers = body.get("receivers")
        email = WushuEmail(
            os.environ.get("GMAIL_USER"),
            os.environ.get("GMAIL_PASSWORD"),
            body.get("type"),
        )
        # email.send_email(receivers)
    except Exception as e:
        return json.dumps(str(e))
    return json.dumps("Email Sent Succesfully!")


if __name__ == "__main__":
    app.run("localhost", 8080, True)
