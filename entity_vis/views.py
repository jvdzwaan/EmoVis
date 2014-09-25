import json

from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from corpus.models import Titel
from entity_vis.models import Character, EntityScore, SpeakingTurn
from entity_vis.es import get_r_score, moving_average


def entities_in_play(request):
    title_id = 'feit007patr01'
    title = get_object_or_404(Titel, pk=title_id)

    characters = Character.objects.filter(play=title) \
                                  .order_by('-num_speaking_turns')[0:5]

    ent_class_1 = 'liwc-Posemo'
    ent_class_2 = 'liwc-Negemo'

    speakingturns = SpeakingTurn.objects.filter(character__play=title) \
                                        .order_by('order')

    result = {}
    for character in characters:
        result[character.name] = []

    for sp in speakingturns:
        for character in characters:
            if sp.character == character:
                try:
                    esc1 = EntityScore.objects.get(Q(speakingturn=sp),
                                                   Q(entity__name=ent_class_1))
                except EntityScore.DoesNotExist:
                    esc1 = None

                try:
                    esc2 = EntityScore.objects.get(Q(speakingturn=sp),
                                                   Q(entity__name=ent_class_2))
                except EntityScore.DoesNotExist:
                    esc2 = None

                result[character.name].append(get_r_score(esc1, esc2))
            else:
                result[character.name].append(0.0)

    # smooth results
    n = 3

    data = []
    for character in characters:
        scores = moving_average(result[character.name], n).tolist()
        values = []
        count = 1
        for score in scores:
            values.append({
                'Turn': count,
                'score': score
            })
            count += 1

        data.append({
            'name': character.name,
            'values': values
        })

    context = {
        'title_id': title.ti_id,
        'title': title.titel,
        'year': title.jaar,
        'authors': [a.voornaam+' '+a.achternaam for a in title.auteurs.all()],
        'genres': [genre.genre for genre in title.genres.all()],
        'subgenres': [subgenre.subgenre for subgenre in title.subgenres.all()],
        'data': json.dumps(data),
        'speakingturns': speakingturns
    }

    return render(request, 'entity_vis/index.html', context)
