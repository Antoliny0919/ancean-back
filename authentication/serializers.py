from typing import Any, Dict, TypeVar
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AbstractBaseUser, update_last_login
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from users.models import User

AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)

api_settings = getattr(settings, 'SIMPLE_JWT', None)

class CustomTokenObtainSerializer(TokenObtainSerializer):

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        self.user = get_object_or_404(User, **authenticate_kwargs)

        return {}

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        return cls.token_class.for_user(user)  # type: ignore
    

class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings["UPDATE_LAST_LOGIN"]:
            update_last_login(None, self.user)

        return data
