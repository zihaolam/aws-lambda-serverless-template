from typing import Optional
from schemas import AuthTokenPayload
from services.partner import PartnerService
from utils.auth_helper import login, signup, verify_cognito_token
import config, logging


def signup_mock_account():
    logging.info("Signing up mock account")
    signup("mock@mock.com", "mock_password")


def get_mock_auth_token():
    return login("mock@mock.com", "mock_password")


def get_mock_token_payload():
    return login("mock@mock.com", "mock_password", parse_payload=True)


def _generate_email_from_account_name(account_name: str, test=False):
    if test:
        return "leanplatform02@gmail.com"
    return f"{account_name}@seed.com".replace(" ", "")

def signup_mock_partner(account_name: Optional[str]=None, avatar_url: Optional[str]=None):
    email = _generate_email_from_account_name(account_name, test=True)
    try:
        signup(email, "password123!", config.UserGroups.PARTNER)
    except Exception as e:
        logging.exception(e)
        
    new_partner = PartnerService.create(PartnerService.create_schema(name="MockPartner", countries=["VN"], email=email, avatar_url=avatar_url if avatar_url is not None else f"https://ui-avatars.com/api/?name={account_name}"))

    return new_partner

def get_mock_partner_auth_token() -> AuthTokenPayload:
    return login("leanplatform02@gmail.com", "password123!", parse_payload=True)
