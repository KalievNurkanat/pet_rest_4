import requests
from users.serializers import GoogleCodeSerilizer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
import os


User = get_user_model()

class GoogleLoginOauth(CreateAPIView):
    serializer_class = GoogleCodeSerilizer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        token_response = requests.post(
            url='https://oauth2.googleapis.com/token',
            data={
                "code":code,
                "client_id": os.environ.get('GOOGLE_CLIENT_ID'),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": os.environ.get('GOOGLE_REDIRECT_URI'),
                "grant_type": "authorization_code"
            }
        )

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response({"Error": "invalid access token"})
        
        user_info = requests.get(
            url="https://www.googleapis.com/oauth2/v3/userinfo",
            params={"alt": "json"},
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()

        email = user_info["email"]
        first_name = user_info.get("given_name", "")
        last_name = user_info.get("family_name", "")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "is_active":True
            }
        )

        if not created:
            if not user.first_name or not user.last_name:
                user.first_name = user.first_name or first_name
                user.last_name = user.last_name or last_name
                user.save()

        refresh_token = RefreshToken.for_user(user)
        
        return Response({"Refresh token": str(refresh_token),
                         "Access token": str(refresh_token.access_token)})



        