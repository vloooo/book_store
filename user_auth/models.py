from django.contrib.auth.models import User
from django.db import models


# additional information for standard user model
class ExtraData(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='extra_data')

    birthday = models.DateField(null=True,
                                blank=True)

    gender = models.CharField(max_length=20,
                              choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                              null=True)

    def __str__(self):
        return self.user.username
