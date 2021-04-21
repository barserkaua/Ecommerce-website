from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)  # ім'я користувача
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)  # опис
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:  # даний клас змінює назву
        ordering = ('name',)  # упорядковує по імені
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)  # ім'я користувача
    slug = models.SlugField(max_length=250, unique=True)  # як буде відображатися у нашій силці
    description = models.TextField(blank=True)  # опис
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:  # даний клас змінює назву
        ordering = ('name',)  # упорядковує по імені (щоб наші зміни вступили в силу
        # їх потрібно мігрувати
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name


class Cart(models.Model):  # модель корзини
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:  # для сортування та назви таблиці
        ordering = ['date_added']
        db_table = 'Cart'

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):  # включає в себе інформацію про продукт, який є в кошику
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # по факту, ми додаємо нову таблицю до нашої БД
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()  # кількість товару
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):  # вираховує кількість товару
        return self.product.price * self.quantity

    def __str__(self):
        return self.product

# Після того, як ми добавили новий функціонал у моделі,
# необхідно зробити міграцію файлів,
# python manage.py makemigrations
# python manage.py migrate
