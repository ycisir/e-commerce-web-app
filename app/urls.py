from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search', views.SearchView.as_view(), name='search'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),



    path('password-change/', views.MyPasswordChangeView.as_view(), name='password-change'),
    path('password-reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('signup/', views.SignupView.as_view(), name='signup'),
    path('accounts/login/', views.MyLoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),


    path('address/', views.AddressView.as_view(), name='address'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('cart/', views.ShowCartView.as_view(), name='cart'),
    path('plus-cart/', views.plus_cart),
    path('minus-cart/', views.minus_cart),
    path('remove-cart/', views.remove_cart),
    path('add-to-cart/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('buy/', views.BuyNowView.as_view(), name='buy-now'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment-done/', views.PaymentDoneView.as_view(), name='payment-done'),
    path('payment-success/', views.PaymentSuccessView.as_view(), name='payment-success'),

    path('mobiles/', views.mobile, name='mobiles'),
    path('mobile/<slug:data>', views.mobile, name='mobile-filter'),

    path('laptops/', views.laptop, name='laptops'),
    path('laptop/<slug:data>', views.laptop, name='laptop-filter'),

    path('top-wears/', views.top_wear, name='top-wears'),
    path('top-wear/<slug:data>', views.top_wear, name='top-wear-filter'),

    path('bottom-wears/', views.bottom_wear, name='bottom-wears'),
    path('bottom-wear/<slug:data>', views.bottom_wear, name='bottom-wear-filter'),
]
