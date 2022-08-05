import uuid
from django.utils.html import mark_safe
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
User._meta.get_field('email')._unique = True


class Slider(models.Model):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=60)
    description = models.CharField(max_length=100)
    slider_image = models.ImageField(upload_to='slideimg')
    price_tag = models.ImageField(upload_to='price_tag')

    def __str__(self):
        return str(self.title)


AVAILABILITY_CHOICES = (
    ('YES','In Stock'),
    ('NO','Not Available In Stock'),
)

CATEGORY_CHOICES = (
    ('FEATURE','Features Items'),
    ('T-SHIRT','T-shirt'),
    ('BLAZERS','Blazers'),
    ('SUNGLASSES','Sunglasses'),
    ('KIDS', 'Kids'),
    ('P-SHIRT', 'Polo-shirt'),
    ('RI','Recommended Items'),
    ('WOMENS','WOMENS'),
    ('FASHION','FASHION'),
    ('HOUSEHOLDS','HOUSEHOLDS'),
    ('INTERIORS','INTERIORS'),
    ('CLOTHING','CLOTHING'),
    ('BAGS','BAGS'),
    ('SHOES','SHOES'),
    ('MENS','MENS')
)

class Product(models.Model):
   # product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=10)
    subcategory = models.CharField(max_length=50)
    Brand = models.CharField(max_length=20)
    selling_price = models.IntegerField()
    discounted_price = models.IntegerField()
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    pub_time = models.TimeField()
    prod_image = models.ImageField(upload_to='productimg')
    prod_image_detail = models.ImageField(upload_to='productimgdetail')
    availability = models.CharField(choices=AVAILABILITY_CHOICES,max_length=3)
    condition = models.CharField(max_length=20)
    rating = models.ImageField(upload_to='rating')
    prod_tag = models.ImageField(upload_to='tag')
    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.product_name)


    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.prod_image.url))

class Countdown(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.name)

class Theme(models.Model):
    color = models.CharField(max_length=1000)
    user = models.CharField(max_length=1000)

    def __str__(self):
        return self.user

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.user)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Sideofferbar(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    sideofferbar = models.ImageField(upload_to='offerimg')

    def __str__(self):
        return str(self.title)

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Wishlist'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,
                             null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self) -> object:
        total = self.product.discounted_price * self.quantity
        return total


STATE_CHOICES = (
    ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal'),
    ('Chandigarh','Chandigarh'),
    ('Dadra & Nagar Haveli and Daman & Diu','Dadra & Nagar Haveli and Daman & Diu'),
    ('Delhi','Delhi'),
    ('Jammu and Kashmir','Jammu and Kashmir'),
    ('Lakshadweep','Lakshadweep'),
    ('Puducherry','Puducherry'),
    ('Ladakh','Ladakh'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True,null=True)
    name = models.CharField(max_length=200, blank=True,null=True)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):
        return str(self.user)
