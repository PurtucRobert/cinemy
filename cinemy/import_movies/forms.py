from django import forms
from import_movies.models import ImportMoviesModel


class ImportMovieForm(forms.ModelForm):
    class Meta:
        model = ImportMoviesModel
        fields = "__all__"
