from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models


class Lobby(models.Model):
    name = models.CharField(max_length=60, default='Новое Лобби')
    max_people = models.IntegerField(default=4, validators=[MaxValueValidator(10)])
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=30, blank=True, null=True, default='')
    lobby_type = models.CharField(max_length=10, choices=[('male', 'Мужское'), ('female', 'Женское'), ('none', 'Смешанное')], default='male')
    description = models.TextField(blank=True, null=True, max_length=250, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='owned_lobbies', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='joined_lobbies', blank=True)

    def __str__(self):
        return self.name


class Flat(models.Model):
    link = models.CharField(primary_key=True, max_length=512)
    price_per_month = models.IntegerField(default=0)
    total_meters = models.FloatField(default=0.0)
    rooms = models.IntegerField(default=0)
    district = models.CharField(default='', max_length=100)
    underground = models.CharField(default='', max_length=100)
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
    last_name = models.CharField(max_length=120, default='unknown')
    first_name = models.CharField(max_length=120, default='unknown')
    email = models.EmailField(unique=True, default='<EMAIL>')
    phone = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Мужской'), ('female', 'Женский')], blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
