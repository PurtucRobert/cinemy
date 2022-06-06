from django.shortcuts import render
from ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required
from .models import Cinema

# Create your views here.


@login_required()
@ratelimit(key="ip", rate="30/m", block=True)
def select_cinema(request):
    if request.method == "GET":
        cinemas = Cinema.objects.all()
        return render(request, "cinema/select_cinema.html", {"cinemas": cinemas})
