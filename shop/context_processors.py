from .models import Category, Cart, CartItem
from .views import _cart_id


def counter(request): # показує кількість елементів в кошику
    item_count = 0
    if 'admin' in request.path: # перевіряємо чи є request.path містить слово 'admin'
        return {}
    else:  # якщо ні, тоді ми будемо вираховувати кількість елементів в кошику
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1]) # повертає тільки один об'єкт
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except Cart.DoesNotExist:
            item_count = 0
    return dict(item_count=item_count)

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
