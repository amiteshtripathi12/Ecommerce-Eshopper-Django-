# Generated by Django 4.0.4 on 2022-06-26 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='digital',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
