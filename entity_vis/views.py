import json
from elasticsearch import Elasticsearch

from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from corpus.models import Titel
from entity_vis.models import Character, EntityScore, SpeakingTurn
from entity_vis.entitysc import get_r_score, moving_average
from entity_vis.es import search_query


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


def find_in_speakingturns(request, concept):
    es = Elasticsearch()
    index_name = 'embodied_emotions'
    doc_type = 'event'

    concepts = {
        'berusting': ['Berusting', 'Berustinghe', 'Berusten', 'Berust',
                      'Beruste', 'Berustend', 'Berustende', 'Berustte'],
        'lijdzaam': ['Lijdzaam', 'Lijdzame', 'Lijdzaem', 'Lydzaame',
                     'Lijdtsaem', 'Lydsaam', 'Lijdzaame', 'Lydzaam',
                     'Lijdzamer', 'Lydzamer',
                     'Lijdzaamer', 'Lydzaamer', 'Lijdsamer', 'Lydsamer',
                     'Lijdsaamer', 'Lydsaamer', 'Lijdzaamheid', 'Lydsamheydts',
                     'Lidtsaemheit', 'Lijdtsaemheyt', 'Lydzaamheid',
                     'Lydzaamheit', 'Lijdzaemheit', 'Lijdtsaemheydt',
                     'Lijtsaemheyd', 'Lijdsaemheyt', 'Lytsaamheden'],
        'gelaten': ['Gelaten', 'Gelatene', 'Gelaeten', 'Gelacten',
                    'Gelatener', 'Ghelaten', 'Gelaaten', 'Gelaeten',
                    'Gelaatende', 'Gelatende', 'Gelatenheid', 'Gelatenheit',
                    'Gelatentheit', 'Gelaatenheid', 'Gelatenheid']
    }

    words = concepts.get(concept, [])

    # number of results for each word
    doc_counts = []
    total = 0
    for word in words:
        q = {
            "query": {
                "match": {
                    "text": word
                }
            }
        }
        result = es.count(index=index_name, doc_type=doc_type, body=q)
        num = int(result.get('count', 0))
        total += num
        doc_counts.append({'word': word, 'count': num})

    # search results
    q = {
        "query": {
            "query_string": {
                "default_field": "text",
                "query": ' OR '.join(words)
            }
        },
        "sort": ["year", "text_id", "order"],
        "aggs": {
            "frequencies": {
                "terms": {
                    "field": "text",
                    "size": 100
                }
            }
        }
    }

    result = es.search(index=index_name, doc_type=doc_type, body=q, size=total)
    speakingturns = []
    for doc in result.get('hits', []).get('hits', []):
        title = Titel.objects.get(pk=doc.get('_source').get('text_id'))
        speakingturns.append({
            'year': doc.get('_source').get('year'),
            'title': title.titel,
            'text': doc.get('_source').get('text'),
            'actor': doc.get('_source').get('actor', 'GEEN')
        })

    word_frequencies = result.get('aggregations').get('frequencies') \
                             .get('buckets')

    context = {
        'title': 'Zoekresultaten in speakingturns voor "{}"'.format(concept),
        'concept': concept,
        'doc_counts': doc_counts,
        'speakingturns': speakingturns,
        'word_frequencies': word_frequencies
    }

    return render(request, 'entity_vis/speakingturns.html', context)
