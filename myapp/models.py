from django.db import models


class Lobby(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Flat(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

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

# user id bes soli


# password with friends
