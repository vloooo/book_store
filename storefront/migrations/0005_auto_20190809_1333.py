# Generated by Django 2.2.4 on 2019-08-09 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0004_auto_20190809_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='books/'),
        ),
    ]
