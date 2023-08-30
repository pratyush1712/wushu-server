import os
import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from endpoints.utils.db import list_serv_members
from endpoints.utils.wushu_email import WushuEmail

email_service_bp = Blueprint("email_service", __name__)


@email_service_bp.route("/", methods=["POST"])
def add_listserv_member():
    body = request.get_json()
    list_serv_members.create_index("email", unique=True)
    list_serv_members.insert_one(body)
    return json.dumps(body, default=str), 200


@email_service_bp.route("/", methods=["GET"])
def get_listserv_members():
    resp = list(list_serv_members.find())
    return json.dumps(resp, default=str)


@email_service_bp.route("/", methods=["DELETE"])
def remove_listserv_members():
    body = json.loads(request.data)
    resp = list_serv_members.delete_one(body)
    return json.dumps(resp, default=str)


@email_service_bp.route("/send", methods=["POST"])
@jwt_required()
def send_email():
    try:
        request_data = request.json

        if not request_data:
            return jsonify({"message": "No data provided"}), 400

        is_broadcast = request_data.get("isBroadcast", False)
        email_body = request_data.get("emailBody")
        email_subject = request_data.get("emailSubject")
        recipient_list = request_data.get("recipientList")

        if not email_body or not recipient_list:
            return jsonify({"message": "Email body or recipients not provided"}), 400

        if is_broadcast:
            all_member_emails = [member["email"] for member in list_serv_members.find()]
            receivers = all_member_emails
        else:
            receivers = recipient_list

        wushu_email = WushuEmail(
            os.environ.get("GMAIL_USER"),
            os.environ.get("GMAIL_PASSWORD"),
            email_subject,
            email_body,
        )

        wushu_email.send_email(receivers)

    except Exception as e:
        return jsonify({"message": "Error sending email", "error": str(e)}), 500

    return jsonify({"message": "Email sent successfully!"}), 200
