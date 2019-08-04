from django.contrib.auth.models import User
from django.db import models


class ExtraData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    gender = models.ForeignKey('gender', on_delete=models.PROTECT, related_name='users')

    def set_birthday(self, date):
        self.birthday = date

    def set_gender(self, gndr):
        self.gender = gndr

    def __str__(self):
        return self.user.username


class Gender(models.Model):
    name = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return self.name
