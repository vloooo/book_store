from django.contrib import admin
from storefront.models import Books, Orders, Author, Genre


admin.site.register(Books)
admin.site.register(Orders)
admin.site.register(Author)
admin.site.register(Genre)

