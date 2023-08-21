import os
import json
from flask import Flask, jsonify
from datetime import timedelta
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies
from flask_jwt_extended import get_jwt, get_jwt_identity
from datetime import datetime, timedelta, timezone
from endpoints.auth import auth_bp
from endpoints.list_serve import list_serv_bp
from endpoints.images import images_bp
from endpoints.members import members_bp
from endpoints.performances import performances_bp

# app config
app = Flask(__name__, static_folder="assets", static_url_path="/assets")
app.config["IMAGES_FOLDER"] = "assets/images"

# cors config
app.config["CORS_HEADERS"] = "Content-Type"
CORS(
    app,
    origins=["https://cornellwushu.github.io", "http://localhost:3000"],
    supports_credentials=True,
)

# auth config
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
jwt = JWTManager(app)


# --------------Main-----------------
@app.route("/")
@cross_origin()
def init():
    return json.dumps("Welcome to Cornell Wushu Server")


@app.after_request
def refresh_expiring_jwts(response):
    """
    After request handler to refresh JWT tokens that are close to expiry.

    Args:
        response: The original response object.

    Returns:
        Flask response object, possibly with a refreshed access token.
    """
    try:
        current_jwt = get_jwt()
    except Exception as e:
        return response

    expiration_timestamp = current_jwt.get("exp")

    if not expiration_timestamp:
        app.logger.warning("No expiration timestamp in JWT. Skipping token refresh.")
        return response

    current_time = datetime.now(timezone.utc)
    threshold_time = current_time + timedelta(days=2)
    threshold_timestamp = datetime.timestamp(threshold_time)

    if expiration_timestamp < threshold_timestamp:
        new_access_token = create_access_token(identity=get_jwt_identity())
        set_access_cookies(response, new_access_token)
    return response


app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(list_serv_bp, url_prefix="/list_serv")
app.register_blueprint(images_bp, url_prefix="/images")
app.register_blueprint(members_bp, url_prefix="/members")
app.register_blueprint(performances_bp, url_prefix="/performances")

if __name__ == "__main__":
    app.run("localhost", 8080, True)
