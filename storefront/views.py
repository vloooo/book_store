from django.shortcuts import render, redirect
from storefront.models import Books, Orders, OrderedBook
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from storefront import messages as msg
from django.contrib.auth.models import User
from storefront.forms import BookForm, AuthorForm, GenreForm
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator


def index(request, a_name=None, g_name=None, sort_p=None, sort_y=None):
    if request.user.is_staff:
        books = Books.objects.all()
    else:
        books = Books.objects.filter(available=True)
    if a_name is not None:
        books = books.filter(author__name=a_name)
    elif g_name is not None:
        books = books.filter(genre__name=g_name)
    elif sort_p is not None:
        if sort_p == 'd':
            books = books.order_by('price')
        else:
            books = books.order_by('-price')
    elif sort_y is not None:
        if sort_y == 'd':
            books = books.order_by('year')
        else:
            books = books.order_by('-year')

    paginator = Paginator(books, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    context = {'books': page.object_list, 'page': page}
    return render(request, 'storefront/home.html', context)


@login_required
def to_cart(request, pk):

    book = Books.objects.get(pk=pk)
    decr_book_amount(request, book)
    active_order = Orders.objects.filter(is_active=True, user=request.user).first()

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

    messages.success(request, msg.scs_msg('book', 'added to cart'))
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
    active_order = request.user.orders.filter(is_active=True).first()
    context = {'order': active_order,
               'ord_books': OrderedBook.objects.filter(order=active_order)}
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
    paginator = Paginator(User.objects.all().order_by('pk'), 10, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)
    context = {'users': page.object_list, 'page': page}
    return render(request, 'storefront/users.html', context)


@user_passes_test(lambda user: user.is_staff)
def staff_book_list(request):
    paginator = Paginator(Books.objects.all(), 10, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)
    context = {'books': page.object_list, 'page': page}
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
            form = BookForm(request.POST, request.FILES, instance=book)
        except ObjectDoesNotExist:
            form = BookForm(request.POST, request.FILES)

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
    return render(request, 'storefront/edit_book.html', context)


def orders_archive(request):
    active_order = request.user.orders.filter(is_active=True).first()
    ord_books = OrderedBook.objects.filter(order=active_order)

    paginator = Paginator(request.user.orders.all(), 5, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)
    context = {'ord_books': ord_books, 'orders': page.object_list, 'page': page}
    return render(request, 'storefront/orders.html', context)


@user_passes_test(lambda user: user.is_staff)
def add_author(request):

    if request.method == 'POST':
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, msg.scs_msg('author', 'added'))
            return redirect('storefront:index')
    else:
        form = AuthorForm()

    context = {'form': form}
    return render(request, 'storefront/edit_book.html', context)


@user_passes_test(lambda user: user.is_staff)
def add_genre(request):

    if request.method == 'POST':
        form = GenreForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, msg.scs_msg('genre', 'added'))
            return redirect('storefront:index')
    else:
        form = GenreForm()

    context = {'form': form}
    return render(request, 'storefront/edit_book.html', context)
