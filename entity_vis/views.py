from django.shortcuts import render, get_object_or_404

from corpus.models import Titel

def posemo(request):
    title_id = 'feit007patr01'
    title = get_object_or_404(Titel, pk=title_id)

    context = {
        'title_id': title.ti_id,
        'title': title.titel
    }
    
    return render(request, 'entity_vis/index.html', context)
