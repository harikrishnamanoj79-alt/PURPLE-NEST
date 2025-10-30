from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    # -----------------------------
    # 1️⃣ COMMON VIEWS (Public)
    # -----------------------------
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search_products, name='search_products'),
    path('products/', views.product_list, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.category_filter, name='category_products'),

    # -----------------------------
    # 2️⃣ CUSTOMER / USER VIEWS
    # -----------------------------
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Order & Checkout
    path('order/<int:product_id>/', views.order_page, name='order_page'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('my_orders/', views.my_orders, name='my_orders'),

    # Wishlist & Cart (Optional)
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'), 
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('cart-checkout/', views.cart_checkout, name='cart_checkout'),
    path('cart/update/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),


    # -----------------------------
    # 3️⃣ ADMIN VIEWS
    # -----------------------------
    # shop/urls.py
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/product/add/', views.add_product, name='add_product'),
    path('admin-panel/products/', views.manage_products, name='manage_products'),
    path('admin-panel/product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('admin-panel/product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('admin-panel/categories/', views.manage_categories, name='manage_categories'),
    path('admin-panel/category/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('admin-panel/categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('admin-panel/manage-orders/', views.manage_orders, name='manage_orders'),
    path('admin-panel/delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('admin-panel/orders/', views.view_orders, name='view_orders'),
    path('admin-panel/order/assign/<int:order_id>/', views.assign_delivery, name='assign_delivery'),
    path('admin-panel/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin-panel/order/status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('admin-panel/users/', views.manage_users, name='manage_users'),
    path('admin-panel/block-user/<int:user_id>/', views.block_user, name='block_user'),
    path('admin-panel/unblock-user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('admin-panel/promote-user/<int:user_id>/', views.promote_user, name='promote_user'),

    path('admin-panel/sales_report/', views.sales_report, name='sales_report'),

    # -----------------------------
    # 4️⃣ DELIVERY VIEWS
    # -----------------------------
    path('delivery/dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    path('delivery/order/<int:order_id>/', views.delivery_order_details, name='delivery_order_details'),
    path('delivery/order/update/<int:order_id>/', views.update_delivery_status, name='update_delivery_status'),
    path('delivery/view-order/<int:order_id>/', views.view_order_details, name='view_order_details'),
    path('delivery/history/', views.delivery_history, name='delivery_history'),

    # -----------------------------
    # 5️⃣ UTILITY / EXTRA VIEWS
    # -----------------------------
    path('terms/', views.terms_and_conditions, name='terms'),
]

# -----------------------------
# MEDIA CONFIGURATION
# -----------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# -----------------------------
# CUSTOM ERROR HANDLER
# -----------------------------
handler404 = views.error_404_view
