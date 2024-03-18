from django.shortcuts import render



def admin_login(request):
    return render(request, 'admin/login.html')