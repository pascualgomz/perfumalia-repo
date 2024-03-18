from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

class LoginPageView(TemplateView):
    template_name = 'login.html'

class SingUpPageView(TemplateView):
    template_name = 'singup.html'

class ProfilePageView(TemplateView):
    template_name = 'user.html'

class PerfumesPageView(TemplateView):
    template_name = 'perfumes.html'

class PerfumesDetailsPageView(TemplateView):
    template_name = 'perfumesdetails.html'

class CartPageView(TemplateView):
    template_name = 'cart.html'

class OrdersPageView(TemplateView):
    template_name = 'orders.html'

class OrderDetailsPageView(TemplateView):
    template_name = 'orderdetails.html'

class PaymentPageView(TemplateView):
    template_name = 'payment.html'

class SearchResultsPageView(TemplateView):
    template_name = 'searchresults.html'

class SubscriptionPageView(TemplateView):
    template_name = 'subscription.html'