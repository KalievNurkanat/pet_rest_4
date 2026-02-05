from rest_framework import serializers
from countries.models import City, Country, Review
from rest_framework.exceptions import ValidationError
from users.models import CustomUser

class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username"]

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name"]

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]

    def validate_country(self, name):
        if Country.objects.filter(name=name).exists():
            raise ValidationError("Such a city already exists")
        return name

class CityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

    def validate_name(self, name):
            if City.objects.filter(name=name).exists():
                raise ValidationError("Such a city already exists")
            return name
    
class CityEditDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class ReviewCitySerializer(serializers.ModelSerializer):
    author = UserBaseSerializer(read_only=True)
    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, attrs):
        user = self.context["request"].user
        count = Review.objects.filter(author=user).count()
        if count >= 1:
            raise serializers.ValidationError("You can't write reviews anymore")
        return attrs
    
    

class ReviewCityEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class CityDetailsSerializer(serializers.ModelSerializer):
    country_id = CountrySerializer()
    city_rating = ReviewCitySerializer(many=True)
    total_city_rating = serializers.FloatField(read_only=True)
    class Meta:
        model = City
        fields = ["id", "name", "population","total_city_rating", "country_id", "city_rating"]

class CountryDetailsSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)
    total_population = serializers.IntegerField(read_only=True)
    total_rating_for_rest = serializers.FloatField(read_only=True)
    class Meta:
        model = Country
        fields = ["id", "name", "total_population","total_rating_for_rest", "cities"]


