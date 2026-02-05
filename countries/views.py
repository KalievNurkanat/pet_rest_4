from countries.models import City, Country, Review
from countries.serializers import (CitySerializer, CountrySerializer,
                                    CityDetailsSerializer, CityEditDetailsSerializer, CountryDetailsSerializer, CityCreateSerializer,
                                    ReviewCitySerializer, ReviewCityEditSerializer)
from django.db.models import Sum, Avg
from common.permissions import IsAuthenticated, IsGuest, OwnerRights, IsAdmin, NotForAdmin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from countries.tasks import send_email, send_daily_report
from nations.settings import EMAIL_SEND_TO
from rest_framework.response import Response
# Create your views here.

class CityAPIView(ListCreateAPIView):
    permission_classes = [IsAdmin | IsGuest]
    queryset = City.objects.select_related("country_id")
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CitySerializer
        return CityCreateSerializer

class CityDetailAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    permission_classes = [IsAdmin | IsGuest]

    def get_queryset(self):
        if self.request.method == "GET":
            return City.objects.annotate(total_city_rating=Avg("city_rating__rating")).prefetch_related("city_rating")
        return City.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CityDetailsSerializer
        return CityEditDetailsSerializer


class CountryAPIView(ListCreateAPIView):
    permission_classes = [IsAdmin | IsGuest]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.annotate(total_population=Sum("cities__population"),
                                total_rating_for_rest=Avg("cities__city_rating__rating")).prefetch_related(
                                                                                            "cities",
                                                                                            "cities__city_rating"
                                                                                        )
    permission_classes = [IsAdmin | IsGuest]
    serializer_class = CountryDetailsSerializer
    lookup_field = "id"


class ReviewCityView(CreateAPIView):
    permission_classes = [IsAuthenticated & NotForAdmin]
    serializer_class = ReviewCitySerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        user_email = self.request.user.email
        send_email(user_email)
        send_daily_report(EMAIL_SEND_TO)


class ReviewEditView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCityEditSerializer
    permission_classes = [OwnerRights]
    lookup_field = "id"
    

