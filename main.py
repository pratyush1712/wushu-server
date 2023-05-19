import os
import json
from dotenv import load_dotenv
from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
from flask_cors import CORS, cross_origin
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
    JWTManager,
)
from list_serve import WushuEmail

load_dotenv()
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
mongo_server_url = os.environ.get("MONGODB_URL")
app.client = MongoClient(mongo_server_url)
db = app.client[os.environ.get("DB_NAME")]
list_serv_members = db[os.environ.get("LISTSERV_MEMBERS_COLLECTION")]
app.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=20)
jwt = JWTManager(app)


# --------------Main-----------------
@app.route("/")
@cross_origin()
def init():
    return json.dumps("Welcome to Cornell Wushu Server")


# --------------Auth-----------------
@app.route("/token", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return json.dumps("Wrong email or password"), 401
    access_token = create_access_token(identity=email)
    return json.dumps({"access_token": access_token})


@app.route("/logout", methods=["POST"])
def logout():
    response = json.dumps("logout successful")
    unset_jwt_cookies(response)
    return response


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(hours=2))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response


# --------------ListServ-----------------
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
@jwt_required()
@cross_origin()
def send_email():
    body = json.loads(request.data)
    print(body)
    try:
        if body.get("sendAll"):
            receivers = [member["email"] for member in list_serv_members.find()]
        else:
            receivers = body.get("receivers")
        email = WushuEmail(
            os.environ.get("GMAIL_USER"),
            os.environ.get("GMAIL_PASSWORD"),
            body.get("type"),
            body.get("body"),
        )
        print(receivers)
        email.send_email(receivers)
    except Exception as e:
        return json.dumps(str(e))
    return json.dumps("Email Sent Succesfully!")


if __name__ == "__main__":
    app.run("localhost", 8080, True)
