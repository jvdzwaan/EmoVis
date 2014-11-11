import json
from elasticsearch import Elasticsearch

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse

from corpus.models import Titel
from entity_vis.models import Character, EntityScore, SpeakingTurn
from entity_vis.entitysc import get_r_score, moving_average
from entity_vis.es import search_query, term_query, doc_count


def entities_in_play(request, title_id):
    # angular sends post data in the request.body
    if request.body:
        categories = json.loads(request.body).get('categories')
    else:
        categories = []

    if len(categories) < 2:
        return JsonResponse([], safe=False)

    entity_cat1 = categories[0]
    entity_cat2 = categories[1]

    entity_type = 'liwc'

    q = term_query('text_id', title_id)

    # doc count
    num_results = doc_count(q, 'event')

    # characters
    q = term_query('text_id', title_id, num_results)
    q["sort"] = [{"order": {"order": "asc"}}]
    q["aggs"] = {
        "characters": {
            "terms": {
                "field": "actor",
                "size": 5
            }
        }
    }
    result = search_query(q, 'event')

    data = []

    characters = result.get('aggregations').get('characters').get('buckets')
    for character in characters:
        name = character.get('key')
        values = []
        for hit in result.get('hits').get('hits'):
            field = '{}-entities'.format(entity_type)
            entity_data1 = hit.get('_source').get(field).get('data') \
                              .get(entity_cat1, [])
            entity_data2 = hit.get('_source').get(field).get('data') \
                              .get(entity_cat2, [])
            char = hit.get('_source').get('actor')
            turn = hit.get('_source').get('order')
            if char == name and entity_data1:
                score1 = len(entity_data1)
            else:
                score1 = 0

            if char == name and entity_data2:
                score2 = len(entity_data2)
            else:
                score2 = 0
            score = get_r_score(score1, score2)
            values.append(score)

        # smoothing
        scores = moving_average(values, 10).tolist()

        values = []
        turn = 1
        for sc in scores:
            values.append({'turn': turn, 'Score': sc})
            turn += 1

        data.append({'key': name, 'values': values})

    return JsonResponse(data, safe=False)


def browse_entities(request):
    context = {}
    return render(request, 'entity_vis/browse_entities.html', context)


def entity_words(request):
    categories = request.GET.get('categories', '')
    if not categories:
        categories = []
    else:
        categories = categories.split(',')

    entity_words = {}
    ew_year = {}
    ew_genre = {}
    ew_genre_year = {}
    num_texts = 0

    for cat in categories:
        print cat
        q = {
            "query": {
                "match_all": {}
            },
            "size": 0,
            "aggregations": {
                cat: {
                    "terms": {
                        "field": "liwc-entities.data.{}".format(cat),
                        "size": 1000
                    }
                },
                "num_texts": {
                    "cardinality": {
                        "field": "text_id"
                    }
                },
                "entities-year": {
                    "histogram": {
                        "field": "year",
                        "interval": 10,
                        "min_doc_count": 0,
                        "extended_bounds": {
                            "min": 1600,
                            "max": 1850
                        }
                    },
                    "aggs": {
                        "entity": {
                            "terms": {
                                "field": "liwc-entities.data.{}".format(cat),
                                "size": 25
                            }
                        },
                        "texts": {
                            "cardinality": {
                                "field": "text_id"
                            }
                        },

                    }
                },
                "entities-genre": {
                    "terms": {
                        "field": "subgenre",
                        "size": 100
                    },
                    "aggs": {
                        "entity": {
                            "terms": {
                                "field": "liwc-entities.data.{}".format(cat),
                                "size": 25
                            }
                        },
                        "texts": {
                            "cardinality": {
                                "field": "text_id"
                            }
                        }
                    }
                },
                "subgenre": {
                    "terms": {
                        "field": "subgenre",
                        "size": 25
                    },
                    "aggs": {
                        "year": {
                            "histogram": {
                                "field": "year",
                                "interval": 10,
                                "min_doc_count": 0,
                                "extended_bounds": {
                                    "min": 1600,
                                    "max": 1850
                                }
                            },
                            "aggs": {
                                "entity": {
                                    "terms": {
                                        "field": "liwc-entities.data.{}"
                                                 .format(cat),
                                        "size": 25,
                                    }
                                },
                                "texts": {
                                    "cardinality": {
                                        "field": "text_id"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        result = search_query(q, 'event')
        entity_words[cat] = result.get('aggregations').get(cat).get('buckets')
        num_texts = int(result.get('aggregations').get('num_texts')
                              .get('value'))
        ew_genre[cat] = result.get('aggregations').get('entities-genre') \
                              .get('buckets')
        ew_year[cat] = result.get('aggregations').get('entities-year') \
                             .get('buckets')
        ew_genre_year[cat] = result.get('aggregations').get('subgenre') \
                                   .get('buckets')
    context = {
        'entity_words': entity_words,
        'num_texts': num_texts,
        'ew_year': ew_year,
        'ew_genre': ew_genre,
        'ew_genre_year': ew_genre_year,
        'range': range(25)
    }

    return render(request, 'entity_vis/entitywords.html', context)


def entity_categories(request):
    q = {
        "fields": ["name", "words"],
        "size": 100,
        "query": {
            "match_all": {}
        }
    }
    return JsonResponse(search_query(q, "entitycategory"))


def entity_word_pairs(request):
    input_cat = 'Body'
    input_term = 'hart'
    output_cats = ['Posemo', 'Negemo']

    q = {
        "query": {
            "term": {
                "liwc-entities.data.{}".format(input_cat): {
                    "value": "{}".format(input_term)
                }
            }
        },
        "size": 0
    }

    agg = {}

    for cat in output_cats:
        agg[cat] = {
            "terms": {
                "field": "liwc-entities.data.{}".format(cat),
                "size": 1000
            }
        }
    q["aggs"] = agg

    return JsonResponse(search_query(q, 'event'))


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
