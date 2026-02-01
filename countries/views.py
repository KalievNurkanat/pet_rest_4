from countries.models import City, Country, Review
from countries.serializers import (CitySerializer, CountrySerializer,
                                    CityDetailsSerializer, CityEditDetailsSerializer, CountryDetailsSerializer, CityCreateSerializer,
                                    ReviewCitySerializer)
from django.db.models import Sum, Avg
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
# Create your views here.

class CityAPIView(ListCreateAPIView):
    queryset = City.objects.select_related("cities")
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CitySerializer
        return CityCreateSerializer

class CityDetailAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"

    def get_queryset(self):
        if self.request.method == "GET":
            return City.objects.annotate(total_city_rating=Avg("city_rating__rating")).prefetch_related("city_rating")
        return City.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CityDetailsSerializer
        return CityEditDetailsSerializer


class CountryAPIView(ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.annotate(total_population=Sum("cities__population"),
                                total_rating_for_rest=Avg("cities__city_rating__rating")).prefetch_related(
                                                                                            "cities",
                                                                                            "cities__city_rating"
                                                                                        )
    serializer_class = CountryDetailsSerializer
    lookup_field = "id"


class ReviewCityView(CreateAPIView):
    serializer_class = ReviewCitySerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




