# Generated by Django 2.2.3 on 2019-09-11 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='numero_identificacion',
            field=models.BigIntegerField(unique=True),
        ),
    ]