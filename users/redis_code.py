from django.core.cache import cache
from users.serializers import RedisCodeSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
import random

class GenerateCode(APIView):
    def post(self, request):
        user = request.user
        key = f"code:{user}"
        code = str(random.randint(100000, 999999))

        if not user.is_authenticated:
            raise ValidationError("U are not authenticated")

        cache.set(key, code, timeout=60)

        return Response("code in redis take it there", status=200)
    
class ConfirmCode(CreateAPIView):
    serializer_class = RedisCodeSerializer
    def post(self, request):
        user = self.request.user
        key = f"code:{user}"

        redis_code = cache.get(key)
        code = request.data.get('code')

        if redis_code != code:
            return Response("invalid code", status=400)
        
        if not redis_code:
            return Response("code not found", status=400)
        
        user.is_staff = True
        user.save()
        cache.delete(key)
        return Response("Code activated", status=200)
        

