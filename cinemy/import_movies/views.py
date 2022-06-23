from django.shortcuts import render
from ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required
from import_movies.utils import CsvNotFound
from import_movies.forms import ImportMovieForm
from django.contrib import messages


@ratelimit(key="ip", rate="100/m", block=True)
@login_required()
def import_movies(request):
    if request.method == "GET":
        return render(request, "import_movies/import_movies.html")
    if request.method == "POST":
        form = ImportMovieForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request, f"{form.cleaned_data['title']} was imported successfully"
                )
            except CsvNotFound as e:
                messages.success(request, e)
        else:
            errors_dict = dict(form.errors)
            for field in errors_dict:
                if type(errors_dict[field] == list):
                    for error in errors_dict[field]:
                        messages.success(request, f"\n - {error}")
                else:
                    messages.success(request, f"\n - {errors_dict[field]}")
        return render(request, "import_movies/import_movies.html")
