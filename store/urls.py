from django.urls import path
from .views import *

urlpatterns = [
    #path('', home, name='home'),  # Homepage URL
    path('', book_list_view, name='book-list'),  # List all books
    path('search/',search_books, name='book-search'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'), # Book detail view
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('staff-login/', staff_login, name='staff-login'),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
    path('staff/add-book/', add_book, name='add_book'),
    path('staff/delete-book/<int:book_id>/',delete_book, name='book-delete'),
    path('staff/update-book/<int:book_id>/',update_book, name='book-update'),




]
# urls.py
from .views import *

urlpatterns += [
    path('password_reset/', DirectPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('books/<str:category>/', book_category, name='book-category')
    # Other URL patterns
]


from django.urls import path
from .views import add_to_cart, cart_view, remove_from_cart, update_cart

urlpatterns += [
    path('cart/add/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', update_cart, name='update_cart'),
    path('watchlist/add/<int:book_id>/', add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/',view_watchlist, name='watchlist'),
    path('my-orders/', my_orders, name='my_orders'),
]

urlpatterns += [
    path('place-order/', place_order, name='place_order'),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_failed/', payment_failed, name='payment_failed'),
    path('verify-payment/',verify_payment, name='verify_payment')

   
]
