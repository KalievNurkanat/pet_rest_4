from django.db import models
from users_part.models import CustomUser

class Country(models.Model):
    name = models.CharField()
    
    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    name = models.CharField()
    population = models.IntegerField()
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return f"{self.name}"
    
STARS = (
    (i, "*" * i) for i in range(1, 11)
)

class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField(choices=STARS, default=5)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE, related_name="city_rating")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.city}"


