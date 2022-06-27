from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import base64


class ObtainAuthTokenBase64(ObtainAuthToken):
    @classmethod
    def get_extra_actions(self):
        return []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": base64.b64encode(token.key.encode("ascii"))})


obtain_auth_token_base64 = ObtainAuthTokenBase64.as_view()
