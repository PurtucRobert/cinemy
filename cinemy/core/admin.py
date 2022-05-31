from django.contrib import admin
from core.models import Movie


class MovieAdmin(admin.ModelAdmin):
    exclude = ("imdb_link",)

    def save_model(self, request, obj, form, change):
        obj.imdb_link = "https://www.imdb.com/title/" + request.POST["imdb_id"] + "/"
        super().save_model(request, obj, form, change)


admin.site.register(Movie, MovieAdmin)
# Register your models here.
