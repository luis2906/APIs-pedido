# Generated by Django 2.2.3 on 2019-09-11 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='cantidad',
            field=models.IntegerField(max_length=255),
        ),
    ]
