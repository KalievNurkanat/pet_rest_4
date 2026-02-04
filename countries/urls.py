from django.urls import path
from countries.views import (CityAPIView, CountryAPIView,
                              CityDetailAPIView, CountryDetailAPIView, ReviewCityView, 
                              ReviewEditView)

urlpatterns = [
     path("city/", CityAPIView.as_view()),
     path("", CountryAPIView.as_view()),
     path("city/<int:id>/", CityDetailAPIView.as_view()),
     path("<int:id>/", CountryDetailAPIView.as_view()),
     path("city/review/", ReviewCityView.as_view()),
     path("city/review/<int:id>/", ReviewEditView.as_view())
]