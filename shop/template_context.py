from django.db.models import Min, Max

from shop.models import Product


def get_filters(request):

    minMaxPrice = Product.objects.aggregate(Min('price'), Max('price'))

    data = {
        'minMaxPrice': minMaxPrice,
    }

    return data