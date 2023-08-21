from flask import Blueprint, request, jsonify, current_app
from werkzeug.exceptions import BadRequest
from endpoints.utils.db import performances, members
from flask_jwt_extended import jwt_required
import uuid

performances_bp = Blueprint("performances", __name__)


def validate_performance_data(data):
    fields = ["location", "date", "eventName", "url", "members"]

    for field in fields:
        if field not in data:
            raise BadRequest(f"Missing {field} in request data")


@performances_bp.route("/", methods=["POST"])
@jwt_required()
def create_performance():
    data = request.json
    data["_id"] = str(uuid.uuid1())
    performances.insert_one(data)
    return jsonify(data), 201


@performances_bp.route("/", methods=["GET"])
def get_performances():
    performances_list = list(performances.find())
    return jsonify(performances_list)


@performances_bp.route("/<id>", methods=["GET"])
def get_performance(id):
    performance = performances.find_one({"_id": id})
    if performance is not None:
        return jsonify(performance)
    return jsonify({"message": f"No performance found with id: {id}"}), 404


@performances_bp.route("/<id>", methods=["PUT"])
@jwt_required()
def update_performance(id):
    data = request.json
    try:
        performances.update_one({"_id": id}, {"$set": data})
    except Exception as e:
        print(e)
        return jsonify({"message": "Performance not Found"}), 404
    return jsonify(data), 200


@performances_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_performance(id):
    performances.delete_one({"_id": id})
    return jsonify(id), 200
