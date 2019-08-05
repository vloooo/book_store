from django.db import models
from django.contrib.auth.models import User


class Books(models.Model):
    title = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(blank=True, default=0)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    available = models.BooleanField(default=True)
    image = models.CharField(max_length=30, null=True, blank=True)
    year = models.PositiveIntegerField()
    genre = models.ForeignKey('Genre', on_delete=models.PROTECT, null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ['year']
        default_related_name = 'books'

    def __str__(self):
        return self.title


class Orders(models.Model):
    books = models.ManyToManyField(Books, symmetrical=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sum = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']
        default_related_name = 'orders'

    def __str__(self):
        return str(self.pk)





class Author(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name