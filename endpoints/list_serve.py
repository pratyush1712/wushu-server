import os
import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from endpoints.utils.db import list_serv_members
from endpoints.utils.wushu_email import WushuEmail

list_serv_bp = Blueprint("list_serv", __name__)


@list_serv_bp.route("/", methods=["POST"])
def add_listserv_member():
    body = request.get_json()
    list_serv_members.create_index("email", unique=True)
    list_serv_members.insert_one(body)
    return json.dumps(body, default=str), 200


@list_serv_bp.route("/", methods=["GET"])
def get_listserv_members():
    resp = list(list_serv_members.find())
    return json.dumps(resp, default=str)


@list_serv_bp.route("/", methods=["DELETE"])
def remove_listserv_members():
    body = json.loads(request.data)
    resp = list_serv_members.delete_one(body)
    return json.dumps(resp, default=str)


@list_serv_bp.route("/send_email", methods=["POST"])
@jwt_required()
def send_email():
    body = json.loads(request.data)
    try:
        if body.get("everyone"):
            receivers = [member["email"] for member in list_serv_members.find()]
        else:
            receivers = body.get("receivers")
        email = WushuEmail(
            os.environ.get("GMAIL_USER"),
            os.environ.get("GMAIL_PASSWORD"),
            body.get("type"),
            body.get("body"),
        )
        email.send_email(receivers)
    except Exception as e:
        return json.dumps(str(e))
    return json.dumps("Email Sent Succesfully!")
