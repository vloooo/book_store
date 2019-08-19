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
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from api.serializers import BookSerialiser, FullDataShowSerializer, OrdBookSerialiser
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from user_auth.models import ExtraData


from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_204_NO_CONTENT
from django.db.models import Q
from datetime import datetime
from rest_framework.exceptions import ValidationError


@api_view(['GET'])
def api_book(request, pk=0):
    book = Books.objects.all()
    serializer = BookSerialiser(book)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([permissions.AllowAny, ])
def index(request):
    if request.user.is_staff:
        books = Books.objects.all()
    else:
        books = Books.objects.filter(available=True)

    if 'filter' in request.GET:
        target = request.GET['filter']

        if target == 'author':
            books = books.filter(author__icontains=request.GET['name'])
        else:
            books = books.order_by(request.GET['filter'])

    paginator = PageNumberPagination()
    results = paginator.paginate_queryset(books, request)
    serializer = BookSerialiser(results, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['DELETE'])
def del_user(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()

    return Response({"detail": "Successfully deleted"},
                    status=HTTP_204_NO_CONTENT)


@api_view(['GET'])
def api_active_order(request):
    active_order = Orders.objects.filter(
        is_active=True, user=request.user).first()
    books = OrderedBook.objects.filter(order=active_order)
    serializer = OrdBookSerialiser(books, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def api_archive(request):
    books = OrderedBook.objects.filter(
        order__user=request.user).order_by("-order__date")[:7]
    serializer = OrdBookSerialiser(books, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def api_user(request):
    extra_data = ExtraData.objects.get(user=request.user)
    serializer = FullDataShowSerializer(extra_data)
    return JsonResponse(serializer.data, safe=False)


class BooksMetaView(ModelViewSet):
    serializer_class = BookSerialiser
    queryset = Books.objects.all()


class ShowUsers(ModelViewSet):
    serializer_class = FullDataShowSerializer
    queryset = ExtraData.objects.all()


# @csrf_exempt
# @api_view(['POST', "PUT"])
# @permission_classes([permissions.AllowAny, ])
# def edit_book(request): 
#     print (request.data)          
#     print ('sdgsd', request.FILES, 'wuiyewr')          

#     serializer = FullDataShowSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=ValueError):
#         serializer.create(validated_data=request.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.error_messages,
#                     status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST', "PUT"])
@permission_classes([permissions.AllowAny, ])
@authentication_classes([BasicAuthentication, ])
def login(request):
    print(request.data)

    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Please provide both username/email and password'},
                        status=HTTP_400_BAD_REQUEST)

    users = User.objects.filter(Q(email=username) | Q(username=username))
    if not users.exists():
        return Response({'error': 'username or email'},
                        status=HTTP_404_NOT_FOUND)

    user = authenticate(username=users.first().username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    extra_data = ExtraData.objects.get(user=user)
    serializer = FullDataShowSerializer(extra_data)
    return Response({'token': token.key, 'user': serializer.data},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny, ])
@authentication_classes([BasicAuthentication, ])
def registration(request):

    username = request.data.get("username")
    password = request.data.get("password")
    password_conf = request.data.get("confirm_password")
    email = request.data.get("email")

    if username is None or password is None or password_conf is None or email is None:
        return Response({'error': 'Please provide all of this username, email, password'},
                        status=HTTP_400_BAD_REQUEST)
    elif password != password_conf:
        return Response({'error': 'passwords didn\'t match'},
                        status=HTTP_400_BAD_REQUEST)

    users = User.objects.filter(Q(email=email) | Q(username=username))
    if users.exists():
        return Response({'error': 'This email or name is used for another account. Please, enter another one.'},
                        status=HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=request.data.get("username"),
        email=email
    )

    user.set_password(request.data.get("password"))
    user.save()

    try:
        ExtraData.objects.create(user=user,
                                 gender=request.data.get("gender"),
                                 birthday=request.data.get("birthday"))
    except:
        ExtraData.objects.create(user=user,
                                 gender=request.data.get("gender"))

    token, _ = Token.objects.get_or_create(user=user)
    extra_data = ExtraData.objects.get(user=user)
    serializer = FullDataShowSerializer(extra_data)
    return Response({'token': token.key, 'user': serializer.data},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def logout(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        print('errr')

    return Response({"detail": "Successfully logged out."},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(['PUT'])
def profile_edit(request):

    user = request.user

    username = request.data.get("username")
    email = request.data.get("email")

    users = User.objects.filter(
        (Q(email=email) | Q(username=username)) & ~Q(id=user.id))
    print(users)
    if users.exists():
        # raise ValidationError('This email or name is used for another account. Please, enter another one.')
        return Response({'error': 'This email or name is used for another account. Please, enter another one.'},
                        status=HTTP_400_BAD_REQUEST)

    user.username = username
    user.email = email

    if request.data.get("password") != '':
        user.set_password(request.data.get("password"))
    user.save()

    extra_data = ExtraData.objects.get(user=user)
    extra_data.gender = request.data.get("gender")

    if request.data.get("birthday") != '':
        extra_data.birthday = request.data.get("birthday")
    extra_data.save()

    serializer = FullDataShowSerializer(extra_data)
    return Response({'user': serializer.data},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def close_order(request):
    order = request.user.orders.filter(is_active=True).first()

    if 'approve' in request.data:
        order.is_active = False
        order.save()

    else:
        ordered_books = OrderedBook.objects.filter(order=order)

        for item in ordered_books:
            item.book.amount += item.amount
            item.book.save()

        order.delete()

    return Response({"detail": "Successfully closed"},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def to_cart(request, pk):
    user = request.user

    book = Books.objects.get(pk=pk)
    active_order = Orders.objects.filter(is_active=True, user=user).first()
    decr_book_amount(book)

    if active_order is not None:
        ordered_book = OrderedBook.objects.filter(
            book=book, order=active_order, price=book.price).first()
        if ordered_book is not None:
            ordered_book.amount += 1
            ordered_book.save()
        else:
            OrderedBook.objects.create(
                book=book, order=active_order, price=book.price)

        active_order.sum += book.price
        active_order.save()

    else:
        active_order = Orders.objects.create(user=user, sum=book.price)
        OrderedBook.objects.create(
            book=book, order=active_order, price=book.price)

    return Response({"detail": "Successfully added to cart"},
                    status=HTTP_200_OK)


def decr_book_amount(ordered_book):
    try:
        ordered_book.amount -= 1
        ordered_book.save()
    except IntegrityError:
        return Response(status=HTTP_400_BAD_REQUEST)
