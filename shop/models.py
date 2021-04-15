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

    def __str__(self):
        return self.name
