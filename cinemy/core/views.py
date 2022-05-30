from django.shortcuts import render

# Create your views here.


def front_page(request):
    if request.method == "GET":
        return render(request, "core/frontpage.html")
