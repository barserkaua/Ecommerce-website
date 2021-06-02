from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category_slug>', views.home, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>', views.product, name='product_detail'),
    path('cart', views.cart_detail, name='cart_detail'),
    #path('sort-cheap/', views.home, name='search-price'),
    path('filter-data', views.filter_data, name='filter_data'),
    path('load-more-data', views.load_more_data, name='load_more_data'),
    path('cart/add_product/<int:product_id>', views.add_product, name='add_product'),
    path('cart/add/<int:product_id>', views.add_cart, name='add_cart'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('cart/remove_product/<int:product_id>', views.cart_remove_product, name='cart_remove_product'),
    path('account/create/', views.signUpView, name='signup'),
    path('account/login/', views.loginView, name='login'),
    path('account/logout/', views.logoutView, name='logout'),
    path('cart/order/', views.createOrder, name='create_order'),
    path('cart/order/successfully/', views.successfullyOrder, name='successfully_order'),
    path('search/', views.search, name='search'),

]