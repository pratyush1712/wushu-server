import os
import json
from flask import Blueprint, request, jsonify, current_app as app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from endpoints.utils.db import upload_to_aws, members

images_bp = Blueprint("images", __name__)


@images_bp.route("/upload_image", methods=["POST"])
@jwt_required()
def upload_image():
    file = request.files["image"]
    isEmail = json.loads(request.form.get("email"))
    memberProfile = json.loads(request.form.get("memberProfile"))

    filename = secure_filename(file.filename)

    if isEmail:
        filename = f"emails/{filename}"
    elif memberProfile is not None:
        member = members.find_one({"_id": memberProfile})
        if member is not None:
            file_extension = filename.split(".")[-1]
            filename = f"{member['_id']}.{file_extension}"
            upload_to_aws(file, "wushu-emails", filename)
            members.update_one(
                {"_id": memberProfile},
                {
                    "$set": {
                        "image": f"https://wushu-emails.s3.amazonaws.com/{filename}"
                    }
                },
            )
            return jsonify({"url": f"https://wushu-emails.s3.amazonaws.com/{filename}"})

    upload_to_aws(file, "wushu-emails", filename)

    return jsonify({"url": f"https://wushu-emails.s3.amazonaws.com/{filename}"})
