from django.shortcuts import render, get_object_or_404

from corpus.models import Titel

def entities_in_play(request):
    title_id = 'feit007patr01'
    title = get_object_or_404(Titel, pk=title_id)

    context = {
        'title_id': title.ti_id,
        'title': title.titel,
        'year': title.jaar,
        'authors': [a.voornaam+' '+a.achternaam for a in title.auteurs.all()], 
        'genres': [genre.genre for genre in title.genres.all()],
        'subgenres': [subgenre.subgenre for subgenre in title.subgenres.all()]
    }
    
    return render(request, 'entity_vis/index.html', context)
