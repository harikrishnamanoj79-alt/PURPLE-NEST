from django.contrib import admin
from .models import (
    User, Category, Product, Cart, Order, OrderItem, 
    DeliveryTracking, Review, ContactMessage, Payment, 
    Report, Wishlist
)


# -----------------------------
# 1️⃣ Custom User Admin
# -----------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)


# -----------------------------
# 2️⃣ Category Admin
# -----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


# -----------------------------
# 3️⃣ Product Admin
# -----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'category__name')
    list_editable = ('price', 'stock', 'is_featured')
    ordering = ('-created_at',)


# -----------------------------
# 4️⃣ Cart Admin
# -----------------------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('added_at',)


# -----------------------------
# 5️⃣ OrderItem Inline (for viewing inside Orders)
# -----------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


# -----------------------------
# 6️⃣ Order Admin
# -----------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'payment_method', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('id', 'customer__username', 'delivery_person__username')
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


# -----------------------------
# 7️⃣ DeliveryTracking Admin
# -----------------------------
@admin.register(DeliveryTracking)
class DeliveryTrackingAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_person', 'status', 'updated_at')
    list_filter = ('status',)
    search_fields = ('order__id', 'delivery_person__username')
    ordering = ('-updated_at',)


# -----------------------------
# 8️⃣ Review Admin
# -----------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('product__name', 'user__username')
    ordering = ('-created_at',)


# -----------------------------
# 9️⃣ ContactMessage Admin
# -----------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    ordering = ('-created_at',)


# -----------------------------
# 🔟 Payment Admin
# -----------------------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'payment_status', 'transaction_id', 'paid_at')
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('order__id', 'transaction_id')
    ordering = ('-paid_at',)


# -----------------------------
# 1️⃣1️⃣ Report Admin
# -----------------------------
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'total_sales', 'total_orders', 'created_at')
    list_filter = ('report_type',)
    ordering = ('-created_at',)


# -----------------------------
# 1️⃣2️⃣ Wishlist Admin
# -----------------------------
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('added_at',)
