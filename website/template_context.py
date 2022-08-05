from .models import Product
from django.db.models import Min, Max


def get_filters(request):
    minMaxPrice=Product.objects.aggregate(Min('discounted_price'),Max('discounted_price'))
    data = {
        'minMaxPrice': minMaxPrice,
    }
    return data
