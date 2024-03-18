from django.urls import path
from .views import *

urlpatterns = [ 
    path("", HomePageView.as_view(), name='home'),
    path("login", LoginPageView.as_view(), name='login'),
    path("sing-up", SingUpPageView.as_view(), name='singup'),
    path("user", ProfilePageView.as_view(), name='profile'),
    path("perfumes", PerfumesPageView.as_view(), name='perfumes'),
    path("perfumes/<int:pk>/", PerfumesDetailsPageView.as_view(), name='perfumedetails'),
    path("cart", CartPageView.as_view(), name='cart'),
    path("order", OrdersPageView.as_view(), name='orders'),
    path("order/<int:pk>/", OrderDetailsPageView.as_view(), name='orderdetails'),
    path("cart/checkout", PaymentPageView.as_view(), name='payment'),
    path("user", ProfilePageView.as_view(), name='profile'),
    path("search", SearchResultsPageView.as_view(), name='searchresults'),
    path("subscription", SubscriptionPageView.as_view(), name='subscription'),
] 