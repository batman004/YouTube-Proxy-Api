from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api-key")

ACTIVE = "ACTIVE"
INACTIVE = "INACTIVE"
THRESHOLD = 1

api_keys = {}


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    # check if api key in dict and if it is still valid
    if api_key not in api_keys or api_keys[api_key]["status"] == INACTIVE:
        print(api_keys[api_key]["status"])
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
        )

    return api_key


def invoke_api(api_key: str = Depends(api_key_auth)):
    invoke_count = api_keys[api_key]["invoke_count"]
    invoke_count += 1

    api_keys[api_key]["invoke_count"] = invoke_count
    if invoke_count > THRESHOLD:
        api_keys[api_key]["status"] = INACTIVE
