import jwt
import typing
from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from Backend.src.api.root import settings
from Backend.src.api.v1.dataclasses.user import UserStructure
from Backend.src.api.v1.contrib.utils import calculate_expires


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


class OAuth:
    def __init__(self):
        self.__algorithm = settings.ALGORITHM
        self.__secret_key = settings.SECRET_KEY
        self.__secret_key_refresh = settings.SECRET_KEY_REFRESH

        # Default expired times for access and refresh tokens
        self.__expired_time = timedelta(minutes=settings.EXPIRED_TIME_ACCESS_TOKEN)
        self.__expired_time_refresh = timedelta(
            days=settings.EXPIRED_TIME_REFRESH_TOKEN
        )

    def get_user(self, token: str = Depends(oauth2_scheme)) -> UserStructure:
        """
        Get user from database and pack in dict.
        :return: payload {'email': email, 'username': username}
        """
        user = self.validate_token(token)
        return user

    def create_tokens(self, payload: typing.Dict) -> typing.Dict:
        """
        Create and return auth JWT tokens
        :param payload: dict user info for
        :return: Bearer tokens dict(access_token, refresh_token)
        """

        payload.update({"exp": datetime.utcnow() + self.__expired_time})
        access_token = jwt.encode(
            payload, self.__secret_key, algorithm=self.__algorithm
        )

        payload.update({"exp": datetime.utcnow() + self.__expired_time_refresh})
        refresh_token = jwt.encode(
            payload, self.__secret_key_refresh, algorithm=self.__algorithm
        )

        expires_in = calculate_expires()

        bearer_tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": expires_in,
        }
        return bearer_tokens

    def validate_token(
        self, token: str, is_refresh: bool = False
    ) -> typing.Dict or UserStructure:
        """
        Validate user token and return dict user.
        :param token: tokens [access/refresh]
        :param is_refresh: True if token is `refresh_token` or False if `access_token`
        :return: payload with user info if token is access or former a new bearer_info if token is refresh
        """
        try:
            payload = jwt.decode(
                token,
                self.__secret_key_refresh if is_refresh else self.__secret_key,
                algorithms=self.__algorithm,
            )
        except jwt.ExpiredSignature:
            raise HTTPException(status_code=400, detail="Token Expired!")
        except (jwt.DecodeError, jwt.InvalidSignatureError):
            raise HTTPException(status_code=400, detail="Invalid token!")

        return self.create_tokens(payload) if is_refresh else payload
