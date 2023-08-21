import os
from flask import Blueprint, request, jsonify, current_app as app, make_response
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/token", methods=["POST"])
def create_token():
    expires = app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email is None or password is None:
        return jsonify({"error": "Missing email or password"}), 400

    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    if email != admin_email or password != admin_password:
        return jsonify({"error": "Wrong email or password"}), 401

    access_token = create_access_token(identity=email, expires_delta=expires)

    # Create a response object and set the access cookies
    response = make_response(jsonify({"access_token": access_token}))
    response.set_cookie(
        "access_token_cookie",
        value=access_token,
        samesite="None",
        secure=True,
        httponly=True,
    )

    return response


@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response


@auth_bp.route("/auth-check")
@jwt_required()
def auth_check():
    return jsonify({"authenticated": True})
