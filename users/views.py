from users.serializers import UserRegisterSerializer, UserAuthenticateSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import SimpleJWTSerializer
# Create your views here.

class SimpleJWTView(TokenObtainPairView):
    serializer_class = SimpleJWTSerializer


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
