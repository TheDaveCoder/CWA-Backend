import base64
import hmac
import hashlib
import boto3
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from botocore.exceptions import ClientError

# Flask app setup
app = Flask(__name__)
api = Api(app)
CORS(app)

# AWS Cognito settings (Hardcoded for testing)
USER_POOL_ID = "ap-southeast-1_TItFygxtp"
CLIENT_ID = "40r757qh32b5t23r5lldbse929"
CLIENT_SECRET = "1v1i0smmqhk0pkq08e4sbk922ck7rm21lm9rfv34rbmbpk196r90"
REGION = "ap-southeast-1"

# Initialize Cognito client
cognito_client = boto3.client("cognito-idp", region_name=REGION)

def get_secret_hash(username, client_id, client_secret):
    """
    Generate the secret hash required by AWS Cognito.
    """
    message = username + client_id
    secret_hash = hmac.new(
        key=client_secret.encode("utf-8"),
        msg=message.encode("utf-8"),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(secret_hash).decode("utf-8")

class LoginResource(Resource):
    def post(self):
        """
        Handles user authentication with AWS Cognito.
        """
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"message": "Missing email or password"}), 400

        secret_hash = get_secret_hash(email, CLIENT_ID, CLIENT_SECRET)

        try:
            response = cognito_client.initiate_auth(
                ClientId=CLIENT_ID,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": email,
                    "PASSWORD": password,
                    "SECRET_HASH": secret_hash
                }
            )

            # Check if authentication was successful
            if "AuthenticationResult" not in response:
                return jsonify({
                    "message": "Authentication incomplete",
                    "cognito_response": response
                }), 400

            return jsonify({
                "message": "Login successful",
                "id_token": response["AuthenticationResult"]["IdToken"],
                "access_token": response["AuthenticationResult"]["AccessToken"],
                "refresh_token": response["AuthenticationResult"]["RefreshToken"]
            })

        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            return jsonify({"message": "Login failed", "error": error_message}), 401

        except Exception as e:
            return jsonify({"message": "Internal server error", "error": str(e)}), 500

class TestResource(Resource):
    def get(self, token_samp):
        return {"samp": "Hello World"}

    def post(self, token_samp):
        return {"example": request.get_json()}

# Add resources to API
api.add_resource(LoginResource, "/login")  # Login endpoint
api.add_resource(TestResource, "/testMeh/<int:token_samp>")

if __name__ == "__main__":
    app.run(debug=True)
