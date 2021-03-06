from django.db import models
from django.contrib.auth.models import User


class Books(models.Model):
    title = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(blank=True, default=0)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='books/', null=True, blank=True)
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['year']
        default_related_name = 'books'

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)


class Orders(models.Model):
    ord_books = models.ManyToManyField(Books, symmetrical=True, through='OrderedBook', through_fields=('order', 'book'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sum = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']
        default_related_name = 'orders'

    def __str__(self):
        return str(self.pk)


class OrderedBook(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(blank=True, default=1)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        unique_together = ('order', 'book', 'price')


class Author(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name