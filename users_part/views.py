from users_part.serializers import UserRegisterSerializer, UserAuthenticateSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
# Create your views here.

class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserAuthView(CreateAPIView):
    serializer_class = UserAuthenticateSerializer
    def post(self, request):
        serializer = UserAuthenticateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token, _ = Token.objects.get_or_create(user=user)

        return Response(data={"Token": token.key}, status=200)
