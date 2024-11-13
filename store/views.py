

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Book
from django.db.models import Q 
from django.core.paginator import Paginator

from .models import *
# View to list all books
def book_list_view(request):
    search_query = request.GET.get('search')
    books = Book.objects.all()  # Get all books

    if search_query:
        books = books.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query))
    
    # Paginate the book list
    paginator = Paginator(books, 4)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/book_list.html', {'books': page_obj})

# View to show details of a single book
class BookDetailView(DetailView):
    model = Book
    template_name = 'store/book_detail.html'
    context_object_name = 'book'
# Homepage that displays a list of books
def home(request):
    return render(request, 'store/home.html')
# views.py
from django.shortcuts import render
from .models import Book  # Adjust the import according to your Book model

def search_books(request):
    query = request.GET.get('search')
    results = []
    if query:
        results = Book.objects.filter(title__icontains=query)  # Adjust the field as necessary
    return render(request, 'store/book_list.html', {'books': results, 'query': query})


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)  # Log in the new user
            return redirect('book-list')  # Redirect to the home page after registration
    else:
        form = UserRegisterForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user role
                if user.is_staff:
                    return redirect('staff_dashboard')  # Redirect to staff dashboard if user is staff
                else:
                    return redirect('book-list')  # Redirect to book list for normal users
            else:
                return render(request, 'store/user_login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = AuthenticationForm()
    return render(request, 'store/user_login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('book-list')  # Redirect to the home page after logout
# views.py
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    return render(request, 'store/profile.html')

# views.py
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.urls import reverse_lazy

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.views import PasswordResetView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes










class DirectPasswordResetView(PasswordResetView):
    template_name = 'store/password_reset_form.html'  # Specify your custom template here

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            # Generate a one-time use token for the password reset
            token = default_token_generator.make_token(user)
            # Encode the user ID
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Redirect to the password reset confirmation page
            reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            return redirect(reset_url)
        except User.DoesNotExist:
            # Handle case where user is not found
            return super().form_invalid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'store/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'store/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'store/password_reset_complete.html'

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Cart, CartItem

# Get or create a cart for the user
def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    return None  # Handle anonymous users differently

# Add book to cart
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = get_cart(request)
    
    if cart:
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not created:
            cart_item.quantity += 1  # Increase quantity if already in the cart
            cart_item.save()
    return redirect('cart_view')  # Redirect to cart view

# View cart
def cart_view(request):
    cart = get_cart(request)
    items = cart.cartitem_set.all() if cart else []
    total_price = 0
    
    for item in items:
        total_price += item.book.price * item.quantity  # Calculate total price in the view
    
    return render(request, 'store/cart_view.html', {'items': items, 'total_price': total_price})

# Remove item from cart
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart_view')

# Update item quantity in cart
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    new_quantity = request.POST.get('quantity')
    if new_quantity.isdigit() and int(new_quantity) > 0:
        cart_item.quantity = int(new_quantity)
        cart_item.save()
    return redirect('cart_view')



# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditProfileForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'store/edit_profile.html', {'form': form})

@login_required
def add_to_watchlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, book=book)
    if created:
        messages.success(request, f"{book.title} has been added to your watchlist.")
    else:
        messages.info(request, f"{book.title} is already in your watchlist.")
    return redirect('watchlist')

@login_required
def view_watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    return render(request, 'store/watchlist.html', {'watchlist_items': watchlist_items})



def book_category(request, category):
    # Filter books based on the given category
    books = Book.objects.filter(genre__iexact=category)
    return render(request, 'store/book_list.html', {'books': books, 'category': category})


def staff_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('staff_dashboard')  # Redirect to staff dashboard if login is successful
            else:
                # If user is not staff or credentials are invalid
                return render(request, 'store/staff_login.html', {'form': form, 'error': 'Invalid credentials or not a staff member'})
    else:
        form = AuthenticationForm()
    return render(request, 'store/staff_login.html', {'form': form})




from django.contrib.auth.decorators import login_required, user_passes_test

def staff_required(user):
    return user.is_staff
@login_required
@user_passes_test(staff_required)
def staff_dashboard(request):
    # Example: Fetch some data to display in the dashboard
    total_books = Book.objects.count()
    total_users = User.objects.filter(is_staff=False).count()

    context = {
        'total_books': total_books,
        'total_users': total_users,
    }
    return render(request, 'store/staff_dashboard.html', context)
from .forms import BookForm
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book-list')  # Redirect to the book list after adding a book
    else:
        form = BookForm()

    return render(request, 'store/add_book.html', {'form': form})



@staff_member_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book-list')  # Redirect to the book list after deleting a book
    return render(request, 'store/delete_book.html', {'book': book})
def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book-list')  # Redirect to the book list after updating a book
    else:
        form = BookForm(instance=book)

    return render(request, 'store/update_book.html', {'form': form, 'book': book})


from .models import Book, Order, OrderItem
from .forms import OrderItemForm
from decimal import Decimal
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order, OrderItem

@login_required
def place_order(request):
    # Get all cart items for the current user
    cart_items = CartItem.objects.filter(cart__user=request.user)

    if not cart_items.exists():
        # If there are no items in the cart, redirect back to the cart page
        return redirect('cart_view')

    # Calculate the total amount for the order
    total_amount = sum(item.book.price * item.quantity for item in cart_items)
    total_amount_in_paise = int(total_amount * 100)  # Convert to paise

    # Create a Razorpay order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
    razorpay_order = client.order.create({
        'amount': total_amount_in_paise,
        'currency': 'INR',
        'payment_capture': '1'
    })

    # Save the order details in the database
    order = Order.objects.create(
        user=request.user,
        total_amount=total_amount
    )

    # Save each cart item as an order item
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=item.quantity,
            price=item.book.price
        )

    # Clear the cart after placing the order
    cart_items.delete()

    # Pass the Razorpay order ID to the payment page
    context = {
        'order': order,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'total_amount': total_amount
    }

    return render(request, 'store/payment.html', context)


import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_signature = data.get("razorpay_signature")
        order_id = data.get("order_id")

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

        # Verify the payment signature
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # Update the order status to 'Paid' (implement this in your Order model)
            order = Order.objects.get(id=order_id)
            order.status = 'Paid'
            order.save()

            return JsonResponse({'status': 'success'})

        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'status': 'failure'}, status=400)
    return JsonResponse({'status': 'invalid'}, status=400)


def payment_success(request):
    return render(request, 'store/payment_success.html')

def payment_failed(request):
    return render(request, 'store/payment_failed.html')

def verify_payment(request):
    # Your payment verification logic goes here
    return JsonResponse({'status': 'Payment verification complete'})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    context = {
        'orders': orders
    }
    return render(request, 'store/my_orders.html', context)