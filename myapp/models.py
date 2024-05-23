from django.contrib.auth.models import User
from django.db import models


class Lobby(models.Model):
    name = models.CharField(max_length=100, default='Новое Лобби')
    max_people = models.IntegerField(default=4)
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=255, blank=True, null=True, default='')
    lobby_type = models.CharField(max_length=10, choices=[('male', 'Мужское'), ('female', 'Женское')], default='male')
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='owned_lobbies', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='joined_lobbies', blank=True)

    def __str__(self):
        return self.name


# class Flat(models.Model):
#     link = models.CharField(primary_key=True, max_length=512)
#     total_meters = models.FloatField(default=0.0)
#     region = models.CharField(max_length=256, default="")
#     district = models.CharField(max_length=256, default="")
#     street = models.CharField(max_length=256, default="")
#     underground = models.CharField(max_length=256, default="")
#     house = models.CharField(max_length=256, default="")
#     rooms = models.IntegerField(default=0)

#     price_per_m2_coeff = models.IntegerField(default=0)
#     common_ecology_coeff = models.IntegerField(default=0)
#     population_density_coeff = models.IntegerField(default=0)
#     green_spaces_coeff = models.IntegerField(default=0)
#     negative_impact_coeff = models.IntegerField(default=0)
#     phone_nets_coeff = models.IntegerField(default=0)
#     crime_coeff = models.FloatField(default=0.0)
#     lobby = models.ForeignKey(Lobby, related_name='flats', on_delete=models.CASCADE, null=True)

class Flat(models.Model):
    link = models.CharField(primary_key=True, max_length=512)
    price_per_month = models.IntegerField(default=0)
    total_meters = models.FloatField(default=0.0)
    lobby = models.ForeignKey(Lobby, related_name='flats', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.link


class Rating(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('flat', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.flat} as {self.score}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

# class Flat(models.Model):
#     link = models.CharField(max_length=512, primary_key=True)
#     floor = models.IntegerField()
#     floors_count = models.IntegerField()
#     total_meters = models.FloatField()
#     price_per_m2 = models.IntegerField()
#     price_per_month = models.IntegerField()
#     commissions = models.IntegerField()
#     region = models.CharField(max_length=256)
#     district = models.CharField(max_length=256)
#     street = models.CharField(max_length=256)
#     underground = models.CharField(max_length=256)
#     house = models.CharField(max_length=256)
#     rooms = models.IntegerField()
#     common_ecology_coeff = models.IntegerField()
#     population_density_coeff = models.IntegerField()
#     green_spaces_coeff = models.IntegerField()
#     negative_impact_coeff = models.IntegerField()
#     phone_nets_coeff = models.IntegerField()
#     crime_coeff = models.FloatField()

# флэт после нажатия кнопки добавления в список, из ответа создает запись
# lobby список, one to many users-
# список для всех id lobby, ссылка, many to many flats

# user id


# password with friends
