# Generated by Django 4.0.4 on 2022-06-07 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_product_prod_image_detail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Countdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('time', models.DateTimeField()),
            ],
        ),
    ]
