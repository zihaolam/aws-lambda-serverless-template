import os
from dotenv import load_dotenv

STAGE = os.getenv("STAGE")
BASEDIR = os.path.abspath(os.path.dirname(__file__))
ENV_FILE = ".env.dev" if STAGE == "dev" else ".env.prod"
ENV_PATH = os.path.join(BASEDIR, ENV_FILE)

print(f"Loading ENV from: {ENV_PATH}")
load_dotenv(ENV_PATH, override=True)

DATABASE_URL = os.getenv("DATABASE_URL")  # or other relevant config var
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

SERVICE_TOKEN = os.getenv("SERVICE_TOKEN")

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_DOMAIN_NAME = os.getenv("COGNITO_DOMAIN_NAME")
REGION = os.getenv("REGION")
SCOPES = {"me": "Access user's own details"}
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class UserGroups:
    GOOGLE = f"{COGNITO_USER_POOL_ID}_Google"
    BASIC = "user"
    PARTNER = "partner"