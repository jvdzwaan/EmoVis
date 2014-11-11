from models import Titel, Auteur, Genre, Subgenre
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = ('pers_id', 'voornaam', 'achternaam')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('genre_id', 'genre')


class SubgenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subgenre
        fields = ('subgenre_id', 'subgenre')


class TitleSerializer(serializers.ModelSerializer):
    auteurs = AuthorSerializer(many=True)
    genres = GenreSerializer(many=True)
    subgenres = SubgenreSerializer(many=True)

    class Meta:
        model = Titel
        fields = ('ti_id', 'titel', 'jaar', 'auteurs', 'genres', 'subgenres')
