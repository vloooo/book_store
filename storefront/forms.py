from storefront.models import Books, Author, Genre
from django import forms


class BookForm(forms.ModelForm):

    class Meta:
        model = Books
        fields = '__all__'


class GenreForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = '__all__'

class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = '__all__'