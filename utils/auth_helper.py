import logging
import time
from typing import Dict, List
from jose import jwk, jwt
from jose.exceptions import JWTError
from jose.utils import base64url_decode
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEventV2
import urllib.request
from urllib.request import Request
import json, boto3, botocore

import config
from exceptions import AuthException, LambdaException
from models.helpers import generate_key
from models.constants import ModelTypes
from schemas import AuthTokenPayload

cognito_jwk_url = f"https://cognito-idp.ap-southeast-1.amazonaws.com/{config.COGNITO_USER_POOL_ID}/.well-known/jwks.json"


cognito = boto3.client("cognito-idp", region_name=config.REGION)


def get_jwks() -> Dict[str, List[Dict[str, str]]]:
    req = Request(cognito_jwk_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as url:
        try:
            return json.loads(url.read())["keys"]
        except Exception as e:
            print(e)


# jwks = get_jwks()
# Setup cognito user pool and app client, then uncomment this function to enable authentication
jwks = {}

cognito_role_to_model_type_mapping = {
    config.UserGroups.BASIC: ModelTypes.USER,
    # add more user groups here for permissions access control
    config.UserGroups.GOOGLE: ModelTypes.USER,
}


def verify_cognito_token(token: str) -> AuthTokenPayload:
    """verifies bearer token provided in authorization header

    Args:
        token (str): Token will be retrieved from header with fastapi oauth2_scheme.

    Raises:
        HTTPException: Exception for invalid token or expired token

    Returns:
        AuthTokenPayloadSchema: Contents of decoded jwt access_token
    """
    # get the kid from the headers prior to verification
    try:
        headers = jwt.get_unverified_headers(token)
    except JWTError as e:
        raise AuthException("Corrupted Payload")

    kid = headers["kid"]
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(jwks)):
        if kid == jwks[i]["kid"]:
            key_index = i
            break
    if key_index == -1:
        print("Public key not found in jwks.json")
        return False
    # construct the public key

    public_key = jwk.construct(jwks[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit(".", 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        raise AuthException("Corrupted Payload")
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims["exp"]:
        raise AuthException("Expired Token")
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims["aud"] != config.COGNITO_APP_CLIENT_ID:
        raise AuthException("Wrong App Client Id")

    # now we can use the claims
    cognito_group = claims["cognito:groups"]

    if len(cognito_group):
        role = cognito_group[0]

    token_payload = AuthTokenPayload.parse_obj(
        {
            **claims,
            "user_id": generate_key(
                cognito_role_to_model_type_mapping[role], claims["email"]
            ),
        }
    )

    return token_payload


def check_authenticated(event: APIGatewayProxyEventV2) -> AuthTokenPayload:
    try:
        bearer_token = event.headers["authorization"].split("Bearer ")[1]
        return verify_cognito_token(bearer_token)
    except (IndexError):
        raise AuthException("Invalid Bearer Token")
    except (KeyError):
        raise AuthException("Invalid User Group")


def login(email: str, password: str, parse_payload=False) -> AuthTokenPayload:
    try:
        # Add user to pool
        signin_response = cognito.admin_initiate_auth(
            AuthFlow="ADMIN_NO_SRP_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
            ClientId=config.COGNITO_APP_CLIENT_ID,
            UserPoolId=config.COGNITO_USER_POOL_ID,
        )

        token = signin_response["AuthenticationResult"]["IdToken"]

        if parse_payload:
            return verify_cognito_token(token)

        return token

    except Exception as err:
        logging.exception(err)

        raise LambdaException(message="Invalid username or password", status_code=409)


def signup(email: str, password: str, group: str = config.UserGroups.BASIC):
    try:
        # Add user to pool
        cognito.sign_up(
            ClientId=config.COGNITO_APP_CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[{"Name": "email", "Value": email}],
        )

        cognito.admin_confirm_sign_up(
            UserPoolId=config.COGNITO_USER_POOL_ID, Username=email
        )
        cognito.admin_add_user_to_group(
            UserPoolId=config.COGNITO_USER_POOL_ID, Username=email, GroupName=group
        )

    except Exception as err:
        logging.exception(err)
        raise LambdaException(message=err, status_code=409)
