from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from api.config import ApiKeySettings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api-key")


api_keys = {}


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    # check if api key in dict and if it is still valid
    try:
        if (
            api_key not in api_keys
            or api_keys[api_key]["status"] == ApiKeySettings().INACTIVE
        ):
            print(api_keys[api_key]["status"])
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
            )

        return api_key
    except Exception as e:
        return {"Exception": e}


def invoke_api(api_key: str = Depends(api_key_auth)):
    try:
        invoke_count = api_keys[api_key]["invoke_count"]
        invoke_count += 1

        api_keys[api_key]["invoke_count"] = invoke_count
        if invoke_count > ApiKeySettings().THRESHOLD:
            api_keys[api_key]["status"] = ApiKeySettings().INACTIVE
    except Exception as e:
        print(e)
