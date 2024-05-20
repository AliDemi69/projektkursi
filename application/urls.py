from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("best-deals",views.get_all_products, name="best_deals"),
    path("about", views.about, name="about"),
    path("terms", views.terms, name="terms"),
    path("privacy", views.privacy, name="privacy"),
    path('register', views.user_register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('search', views.search, name='search'),
    path('add-to-cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>', views.remove_from_cart, name='remove_from_cart'),
    path('view-cart', views.view_cart, name='view_cart'),
    path('update-cart-item/<int:cart_item_id>', views.update_cart_item, name='update_cart_item'),
    path('checkout', views.checkout, name='checkout'),
    path('order-history', views.order_history, name='order_history'),
    path('filter-products/<int:category_id>', views.filter_products_by_category, name='filter_products_by_category'),
]
