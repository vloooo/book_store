from django.shortcuts import render, redirect
from storefront.models import Books, Orders


def index(request):
    if request.user.is_staff:
        books = Books.objects.all()
    else:
        books = Books.objects.filter(available=True)
    context = {'books': books}
    return render(request, 'storefront/home.html', context)


def to_cart(request, pk):
    book = Books.objects.get(pk=pk)
    order = Orders.objects.filter(is_active=True)

    if order.exists():
        order = order.first()
        order.books.add(book)
        order.sum += book.price
        order.save()

    else:
        order = Orders.objects.create(user=request.user, sum=book.price)
        order = order.first()
        order.books.add(book)
        order.save()

    return redirect('storefront:index')


def cart(request):
    context = {'order': request.user.orders.filter(is_active=True).first()}
    return render(request, 'storefront/cart.html', context)


def close_order(request):
    if request.method == 'POST':
        order = request.user.orders.filter(is_active=True).first()
        order.is_active = False
        order.save()
        return redirect('storefront:index')

    else:
        order = request.user.orders.filter(is_active=True).first()
        context = {'order': order, 'u_shu': True}
    return render(request, 'storefront/cart.html', context)


def orders_archive(request):
    return render(request, 'storefront/orders.html')
