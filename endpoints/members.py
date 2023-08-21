from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from endpoints.utils.db import members, performances
from flask_jwt_extended import jwt_required

members_bp = Blueprint("members", __name__)


def validate_member_data(data):
    fields = [
        "yearJoined",
        "name",
        "description",
        "major",
        "classYear",
        "funFact",
        "image",
        "displayOnSite",
        "eboard",
        "performances",
    ]

    for field in fields:
        if field not in data:
            print(f"Missing {field} in request data")
            raise BadRequest(f"Missing {field} in request data")


@members_bp.route("/", methods=["GET"])
def get_members():
    resp = members.find({})
    return jsonify(list(resp)), 200


@members_bp.route("/", methods=["POST"])
@jwt_required()
def create_member():
    data = request.json
    members.insert_one(data)
    return jsonify(data), 201


@members_bp.route("/<id>", methods=["GET"])
def get_member(id):
    member = members.find_one({"_id": id})
    if member:
        return jsonify(member), 200
    return jsonify({"message": "Member not found"}), 404


@members_bp.route("/<id>", methods=["PUT"])
@jwt_required()
def update_member(id):
    data = request.json
    try:
        members.update_one({"_id": id}, {"$set": data})
    except Exception as e:
        print(e)
        return jsonify({"message": "Member not Found."}), 404

    return jsonify(data), 200


@members_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_member(id):
    members.delete_one({"_id": id})
    return jsonify(id), 200


@members_bp.route("/eboard", methods=["GET"])
def get_eboard_members():
    eboard_members = members.find({"eboard": {"$exists": True, "$ne": None}})
    return jsonify(list(eboard_members)), 200
