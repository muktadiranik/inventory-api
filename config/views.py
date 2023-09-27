from django.shortcuts import redirect


# Django Admin, use {% url 'admin:index' %}
def home(request):
    return redirect("admin:index")
