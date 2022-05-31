from datetime import datetime
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import Movie
from ratelimit.decorators import ratelimit

# Create your views here.


@ratelimit(key="ip", rate="30/m", block=True)
def front_page(request):
    if request.method == "GET":
        movies = Movie.objects.filter(available_from__lte=datetime.today())
        paginator = Paginator(movies, 5)
        page = request.GET.get("page", 1)
        try:
            movies_paginated = paginator.get_page(page)
        except PageNotAnInteger:
            movies_paginated = paginator.page(1)
        except EmptyPage:
            movies_paginated = paginator.page(paginator.num_pages)
        return render(request, "core/frontpage.html", {"movies": movies_paginated})
