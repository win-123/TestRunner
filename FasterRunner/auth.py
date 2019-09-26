import time

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from FasterRunner.settings import INVALID_TIME
from fastuser import models
from utils import validation_info


class Authenticator(BaseAuthentication):
    """
    账户鉴权认证 token
    """

    def authenticate(self, request):

        token = request.query_params.get("token", None)
        obj = models.UserToken.objects.filter(token=token).first()

        if not obj:
            raise exceptions.AuthenticationFailed(validation_info.VALIDATION_INFO["fail"])

        update_time = int(obj.update_time.timestamp())
        current_time = int(time.time())

        if current_time - update_time >= INVALID_TIME:
            raise exceptions.AuthenticationFailed(validation_info.VALIDATION_INFO["time_out"])

        # valid update valid time
        obj.token = token
        obj.save()

        return obj.user, obj

    def authenticate_header(self, request):
        return 'Auth Failed'
