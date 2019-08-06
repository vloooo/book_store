from django.shortcuts import render, redirect
from storefront.models import Books, Orders, OrderedBook
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from storefront import messages as msg
from django.contrib.auth.models import User
from storefront.forms import BookForm
from django.contrib.auth.decorators import user_passes_test


def index(request):
    if request.user.is_staff:
        books = Books.objects.all()
    else:
        books = Books.objects.filter(available=True)
    context = {'books': books}
    return render(request, 'storefront/home.html', context)

@login_required
def to_cart(request, pk):

    book = Books.objects.get(pk=pk)
    decr_book_amount(request, book)
    active_order = Orders.objects.filter(is_active=True).first()

    if active_order is not None:
        ordered_book = OrderedBook.objects.filter(book=book, order=active_order, price=book.price).first()
        if ordered_book is not None:
            ordered_book.amount += 1
            ordered_book.save()
        else:
            OrderedBook.objects.create(book=book, order=active_order, price=book.price)

        active_order.sum += book.price
        active_order.save()

    else:
        active_order = Orders.objects.create(user=request.user, sum=book.price)
        OrderedBook.objects.create(book=book, order=active_order, price=book.price)

    return redirect('storefront:index')


def decr_book_amount(request, ordered_book):
    try:
        ordered_book.amount -= 1
        ordered_book.save()
    except IntegrityError:
        messages.info(request, msg.sold_last_book)

        return redirect('storefront:index')

@login_required
def cart(request):
    context = {'order': request.user.orders.filter(is_active=True).first()}
    return render(request, 'storefront/cart.html', context)


@require_POST
@login_required
def close_order(request):
    order = request.user.orders.filter(is_active=True).first()

    if 'approve' in request.POST:
        order.is_active = False
        order.save()
        message = msg.scs_msg('order', 'approved')
    else:
        ordered_books = OrderedBook.objects.filter(order=order)

        for item in ordered_books:
            item.book.amount += item.amount
            item.book.save()

        order.delete()
        message = msg.scs_msg('order', 'canceled')

    messages.success(request, message)
    return redirect('storefront:index')


@user_passes_test(lambda user: user.is_staff)
def show_users(request):
    context = {'users': User.objects.all()}
    return render(request, 'storefront/users.html', context)


@user_passes_test(lambda user: user.is_staff)
def staff_book_list(request):
    context = {'books': Books.objects.all()}
    return render(request, 'storefront/books.html', context)


@user_passes_test(lambda user: user.is_staff)
def del_user(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    messages.success(request, msg.scs_msg('user', 'deleted'))
    return redirect('storefront:show_users')


@user_passes_test(lambda user: user.is_staff)
def del_book(request, pk):
    book = Books.objects.get(pk=pk)
    book.delete()
    messages.success(request, msg.scs_msg('book', 'deleted'))
    return redirect('storefront:show_books')


def book_profile(request, pk):
    book = Books.objects.get(pk=pk)
    context = {'book': book}
    return render(request, 'storefront/book_profile.html', context)


@user_passes_test(lambda user: user.is_staff)
def book_edit(request, pk=None):

    if request.method == 'POST':
        try:
            book = Books.objects.get(pk=pk)
            form = BookForm(request.POST, instance=book)
        except ObjectDoesNotExist:
            form = BookForm(request.POST)

        if form.is_valid():
            book = form.save()

            messages.success(request, msg.scs_msg('book', 'edited'))
            return redirect('storefront:profile_book', pk=book.pk)
    else:
        if pk is None:
            form = BookForm()
        else:
            book = Books.objects.get(pk=pk)
            form = BookForm(instance=book)

    context = {'form': form}
    return render(request, 'user_auth/register.html', context)


def orders_archive(request):
    return render(request, 'storefront/orders.html')
