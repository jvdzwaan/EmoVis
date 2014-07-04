from django.contrib import admin
from corpus.models import Titel, Auteur, Genre, Subgenre

admin.site.register(Titel)
admin.site.register(Auteur)
admin.site.register(Genre)
admin.site.register(Subgenre)
