# Generated by Django 4.0.4 on 2022-06-03 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('FEATURE', 'Features Items'), ('T-SHIRT', 'T-shirt'), ('BLAZERS', 'Blazers'), ('SUNGLASSES', 'Sunglasses'), ('KIDS', 'Kids'), ('P-SHIRT', 'Polo-shirt'), ('RI', 'Recommended Items'), ('WOMENS', 'WOMENS'), ('FASHION', 'FASHION'), ('HOUSEHOLDS', 'HOUSEHOLDS'), ('INTERIORS', 'INTERIORS'), ('CLOTHING', 'CLOTHING'), ('BAGS', 'BAGS'), ('SHOES', 'SHOES'), ('MENS', 'MENS')], max_length=10)),
                ('subcategory', models.CharField(max_length=50)),
                ('selling_price', models.IntegerField()),
                ('discounted_price', models.IntegerField()),
                ('desc', models.CharField(max_length=300)),
                ('pub_date', models.DateField()),
                ('pub_time', models.TimeField()),
                ('prod_image', models.ImageField(upload_to='productimg')),
                ('availability', models.CharField(choices=[('YES', 'In Stock'), ('NO', 'Not Available In Stock')], max_length=3)),
                ('condition', models.CharField(max_length=20)),
                ('rating', models.ImageField(upload_to='rating')),
                ('prod_tag', models.ImageField(upload_to='tag')),
            ],
        ),
    ]
