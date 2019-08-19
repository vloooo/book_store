from rest_framework import serializers
from storefront.models import Books, Orders, OrderedBook
from user_auth.models import ExtraData
from django.contrib.auth.models import User


class BookSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = '__all__'


class UserShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', "is_staff", "is_active", "id")


class FullDataShowSerializer(serializers.ModelSerializer):

    user = UserShowSerializer(required=True)

    class Meta:
        model = ExtraData
        fields = ('user', 'gender', 'birthday')


class OrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = ('id', 'date', 'sum', 'is_active')


class BookForOrderSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = ("id", "title")


class OrdBookSerialiser(serializers.ModelSerializer):
    book = BookForOrderSerialiser(required=True)
    order = OrdersSerializer(required=True)

    class Meta:
        model = OrderedBook
        fields = ('price', 'amount', 'book', 'order')
