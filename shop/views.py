# shop/views.py
# ------------------------------------------------------------
# Django Ambulance/Store Management System
# Role-based views for Customer, Admin, and Delivery Staff
# ------------------------------------------------------------

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Sum, Avg,Count
from django.http import HttpResponse
from django.utils import timezone

from .models import *
from .forms import *


# ======================================================
# 1️⃣ COMMON VIEWS (Publicly Accessible)
# ======================================================

def home(request):
    """Homepage showing categories and featured products."""
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True)[:8]
    return render(request, 'home.html', {
        'categories': categories,
        'featured_products': featured_products
    })


def about(request):
    """About Page."""
    return render(request, 'about.html')


def contact(request):
    """Contact form page."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def product_list(request):
    """List all products with search and filter."""
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id
    })


def category_filter(request, category_id):
    """Filter products by category."""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'product_list.html', {
        'category': category,
        'products': products,
        'categories': categories,
    })


def product_detail(request, product_id):
    """Product detail with reviews and buy/add options."""
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)

    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('product_detail', product_id=product.id)
    else:
        review_form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': review_form
    })


# ======================================================
# 2️⃣ CUSTOMER / USER VIEWS
# ======================================================

def register_user(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'customer'
            user.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome aboard.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})



def login_user(request):
    if request.user.is_authenticated:
        # If already logged in, redirect based on role
        role = getattr(request.user, 'role', 'customer')
        return redirect_based_on_role(role)

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")

            role = getattr(user, 'role', 'customer')
            return redirect_based_on_role(role)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def redirect_based_on_role(role):
    """Redirect users based on their role."""
    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'delivery':
        return redirect('delivery_dashboard')
    else:  # customer
        return redirect('home')


@login_required
def logout_user(request):
    """Logout current user."""
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('home')


@login_required
def profile(request):
    """User profile page."""
    return render(request, 'profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    """Edit profile information."""
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    return render(request, 'edit_profile.html')


@login_required
def order_page(request, product_id):
    """Order now page for a product."""
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'order_page.html', {'product': product})

@login_required(login_url='login')
def cart_checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('cart_view')

    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        payment_method = request.POST.get('payment_method', 'COD')
        address = request.POST.get('address', request.user.address)

        order = Order.objects.create(
            customer=request.user,
            total_amount=total_amount,
            status='pending',
            payment_method=payment_method,
            address=address
        )

        # Save all cart items as order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear the cart after order
        cart_items.delete()

        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'single_product_checkout': False
    })





@login_required(login_url='login')
def order_confirmation(request, order_id):
    """Order confirmation page."""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'order_confirmation.html', {'order': order})


@login_required
def my_orders(request):
    """Display all orders of a user."""
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


# -------------------------------
# Wishlist Views
# -------------------------------

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('wishlist')


# -------------------------------
# Cart Views
# -------------------------------

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart successfully!")
    return redirect('cart_view')




@login_required
def update_cart_quantity(request, product_id):
    if request.method == "POST":
        new_qty = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
        cart_item.quantity = new_qty
        cart_item.save()
    return redirect('cart_view')

@login_required(login_url='login')
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


# -------------------------------
# Checkout Page
# -------------------------------
@login_required(login_url='login')
def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # When the user clicks "Buy Now" (first POST request)
    if request.method == 'POST' and 'payment_method' not in request.POST:
        quantity = int(request.POST.get('quantity', 1))
        subtotal = product.price * quantity

        # Render the checkout page with product details
        return render(request, 'checkout.html', {
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
            'total': subtotal,  # Can include shipping later
        })

    # When the user submits the checkout form (second POST request)
    elif request.method == 'POST' and 'payment_method' in request.POST:
        quantity = int(request.POST.get('quantity', 1))
        payment_method = request.POST.get('payment_method', 'COD')
        address = request.POST.get('address', getattr(request.user, 'address', 'Not Provided'))
        total_price = product.price * quantity

        # Create order and order item
        order = Order.objects.create(
            customer=request.user,
            status='pending',
            payment_method=payment_method,
            total_amount=total_price,
            address=address
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        messages.success(request, "Order placed successfully!")
        return redirect('order_confirmation', order_id=order.id)

    # Handle GET request (in case someone directly visits the page)
    else:
        quantity = 1
        subtotal = product.price
        return render(request, 'checkout.html', {
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
            'total': subtotal,
        })




# ======================================================
# 3️⃣ ADMIN VIEWS
# ======================================================


def admin_required(user):
    return user.is_staff or user.is_superuser


@login_required(login_url='login')
def admin_dashboard(request):
    # Prevent non-admin users from seeing this
    if not hasattr(request.user, 'role') or request.user.role != 'admin':
        messages.error(request, "Access denied: Admins only.")
        return redirect('home')

    # Dashboard stats
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_sales = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0

    # Recent 5 orders
    recent_orders = (
        Order.objects.select_related('customer')
        .order_by('-created_at')[:5]
    )

    # Orders by status
    order_status_data = (
        Order.objects.values('status')
        .annotate(count=Count('id'))
        .order_by()
    )

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'recent_orders': recent_orders,
        'order_status_data': order_status_data,
    }

    return render(request, 'admin/dashboard.html', context)

@login_required(login_url='login')
def add_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        is_featured = 'is_featured' in request.POST

        category = get_object_or_404(Category, id=category_id)
        Product.objects.create(
            name=name,
            category=category,
            price=price,
            description=description,
            stock=stock,
            image=image,
            is_featured=is_featured,
        )
        messages.success(request, "Product added successfully!")
        return redirect('admin_dashboard')
    return render(request, 'admin/add_product.html', {'categories': categories})

@login_required(login_url='login')
def manage_products(request):
    """Display all products for admin with search and edit/delete options."""
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all().order_by('-created_at')
    return render(request, 'admin/manage_products.html', {'products': products})



@login_required

def edit_product(request, product_id):  # make sure the parameter matches your URL
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()  # <-- this populates the dropdown

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category_id = request.POST.get('category')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.description = request.POST.get('description')
        product.is_featured = 'is_featured' in request.POST

        if request.FILES.get('image'):
            product.image = request.FILES['image']

        product.save()
        return redirect('admin_dashboard')

    return render(request, 'adminedit_product.html', {
        'product': product,
        'categories': categories,  # <-- passed to template
    })

@login_required(login_url='login')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('manage_products')  # or 'admin_dashboard' if that’s your main admin page
    
    return render(request, 'admin/confirm_delete.html', {'product': product})

@login_required(login_url='login')
def manage_categories(request):
    # Allow only users with role='admin'
    if request.user.role != 'admin':
        messages.error(request, "Access denied. Admins only.")
        return redirect('home')

    # ✅ Handle adding a new category
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if name:
            Category.objects.create(
                name=name,
                description=description,
                image=image
            )
            messages.success(request, f"Category '{name}' added successfully!")
            return redirect('manage_categories')
        else:
            messages.error(request, "Category name is required!")

    # ✅ Fetch all categories for display
    categories = Category.objects.all().order_by('name')

    return render(request, 'admin/manage_categories.html', {
        'categories': categories
    })

@login_required(login_url='login')
def edit_category(request, category_id):
    # Restrict access to admin users
    if request.user.role != 'admin':
        messages.error(request, "Access denied. Admins only.")
        return redirect('home')

    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if not name:
            messages.error(request, "Category name is required.")
            return redirect('edit_category', category_id=category.id)

        # Update fields
        category.name = name
        category.description = description

        # Only replace image if a new one is uploaded
        if image:
            category.image = image

        category.save()
        messages.success(request, f"Category '{category.name}' updated successfully!")
        return redirect('manage_categories')

    return render(request, 'admin/edit_category.html', {'category': category})


@login_required(login_url='login')
def delete_category(request, category_id):
    if request.user.role != 'admin':
        messages.error(request, "Access denied. Admins only.")
        return redirect('home')

    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect('manage_categories')


@login_required(login_url='login')
def manage_users(request):
    if request.user.role != 'admin':
        return redirect('home')

    selected_role = request.GET.get('role', '')

    users = User.objects.all().order_by('-date_joined')
    if selected_role:
        users = users.filter(role=selected_role)

    context = {
        'users': users,
        'selected_role': selected_role,
    }
    return render(request, 'admin/manage_users.html', context)



@login_required(login_url='login')
def block_user(request, user_id):
    if request.user.role != 'admin':  # ✅ check by role instead
        messages.error(request, "Access denied. Admins only.")
        return redirect('home')
    
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f"{user.username} has been blocked.")
    return redirect('manage_users')



@login_required(login_url='login')
def unblock_user(request, user_id):
    if request.user.role != 'admin':  # ✅ use role check
        messages.error(request, "Access denied. Admins only.")
        return redirect('home')
    
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f"{user.username} has been unblocked.")
    return redirect('manage_users')



@login_required(login_url='login')
def promote_user(request, user_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admins only.")
        return redirect('home')
    
    user = get_object_or_404(User, id=user_id)
    user.is_staff = True
    user.save()
    messages.success(request, f"{user.username} has been promoted to admin.")
    return redirect('manage_users')

@login_required(login_url='login')
def manage_orders(request):
    # Allow access if user has admin role or is marked as staff
    if not (hasattr(request.user, 'role') and request.user.role == 'admin') and not request.user.is_staff:
        messages.error(request, "Access denied. Admins only.")
        return redirect('home')
        
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin/manage_orders.html', {'orders': orders})




@login_required(login_url='login')
def admin_order_detail(request, order_id):
    """Admin view for viewing full order details."""
    order = get_object_or_404(Order, id=order_id)
    items = OrderItem.objects.filter(order=order)
    return render(request, 'admin/order_detail.html', {
        'order': order,
        'items': items
    })


@login_required(login_url='login')
def delete_order(request, order_id):
    if not (hasattr(request.user, 'role') and request.user.role == 'admin') and not request.user.is_staff:
        messages.error(request, "Access denied. Admins only.")
        return redirect('home')

    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Order deleted successfully!")
    return redirect('manage_orders')
   

@login_required(login_url='login')
def view_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin/view_orders.html', {'orders': orders})


@login_required(login_url='login')
def assign_delivery(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    delivery_persons = User.objects.filter(role='delivery')

    if request.method == 'POST':
        delivery_id = request.POST.get('delivery_person')
        if delivery_id:
            delivery_person = User.objects.get(id=delivery_id)
            order.delivery_person = delivery_person
            order.status = 'processing'
            order.save()
            DeliveryTracking.objects.create(order=order, delivery_person=delivery_person, status='assigned')
            messages.success(request, f"Delivery assigned to {delivery_person.username}")
            return redirect('view_orders')

    return render(request, 'admin/assign_delivery.html', {
        'order': order,
        'delivery_persons': delivery_persons
    })


@login_required(login_url='login')
def sales_report(request):
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')
    sales = Order.objects.filter(status='delivered')

    if from_date and to_date:
        sales = sales.filter(created_at__range=[from_date, to_date])

    total_orders = sales.count()
    total_revenue = sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    avg_order_value = sales.aggregate(Avg('total_amount'))['total_amount__avg'] or 0

    return render(request, 'admin/sales_report.html', {
        'sales': sales,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'avg_order_value': avg_order_value
    })


@login_required(login_url='login')
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {new_status}.')
        else:
            messages.error(request, 'Invalid status value.')
        return redirect('admin_dashboard')  # or change this to where you list orders
    
    return render(request, 'admin/update_order_status.html', {'order': order})

def view_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'delivery/order_details.html', context)


# ======================================================
# 4️⃣ DELIVERY STAFF VIEWS
# ======================================================

def delivery_required(user):
    return user.is_authenticated and user.role == 'delivery'


@user_passes_test(delivery_required)
def delivery_dashboard(request):
    active_deliveries = DeliveryTracking.objects.filter(delivery_person=request.user).exclude(status='delivered')
    completed_deliveries = DeliveryTracking.objects.filter(delivery_person=request.user, status='delivered')

    return render(request, 'delivery/dashboard.html', {
        'active_deliveries': active_deliveries,
        'completed_deliveries': completed_deliveries
    })


@user_passes_test(delivery_required)
def delivery_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, delivery_person=request.user)
    return render(request, 'delivery/order_details.html', {'order': order})


@user_passes_test(delivery_required)
def update_delivery_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, delivery_person=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        order.status = new_status
        order.save()
        DeliveryTracking.objects.create(order=order, delivery_person=request.user, status=new_status, notes=notes)
        messages.success(request, f"Order #{order.id} marked as {new_status}.")
        return redirect('delivery_dashboard')
    return render(request, 'delivery/update_status.html', {'order': order})


@user_passes_test(delivery_required)
def delivery_history(request):
    deliveries = DeliveryTracking.objects.filter(delivery_person=request.user, status='delivered').order_by('-updated_at')
    return render(request, 'delivery/history.html', {'deliveries': deliveries})


# ======================================================
# 5️⃣ UTILITY / EXTRA VIEWS
# ======================================================

def search_products(request):
    query = request.GET.get('q')
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    categories = Category.objects.all()
    return render(request, 'product_list.html', {'products': products, 'categories': categories})


def terms_and_conditions(request):
    return render(request, 'terms.html')


def error_404_view(request, exception):
    return render(request, '404.html', status=404)
