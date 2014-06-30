import operator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from models import Titel, Auteur, Titelxauteur, Genre

_corpus_ids = ['rotg001lstr03', 'rotg001lstr01', 'ling001apol01', 
    'bild002dich04', 'hoof001thes01', 'hare003agon01', 'asse001kwak01', 
    'bred001rodd01', 'nore003list01', 'moli015lubb02', 'beet004dich01', 
    'bidl001nede01', 'quin031wanh02', 'rotr001groo02', 'corn104verm01', 
    'venn001tafe03', 'vos_002wjcb01', 'rode001aure01', 'vinc001hoog01', 
    'vinc001list01', 'marr001marc01', 'quin031mede01', 'teng001jjov01', 
    'heyn003cons01', 'cost001teeu01', '_jaa005200101', 'vond001gysb04', 
    'grie002pkey01', 'rijk001atha01', 'vos_001kluc04', 'corn001dood01', 
    'lope001dull01', 'nooz002inek01', 'vinc001pefr02', 'zand008deme01', 
    'vond001gysb01', 'hoev003dood02', 'hoev003dood01', 'moli015verw02', 
    'lang020gava01', 'alew001puit01', 'koss004nied01', '_tij003190201', 
    'croi003meid01', 'asse001gusm02', 'bred001spaa01', 'tijs003merk01', 
    'fres003inen01', 'aren001kroo01', 'weye002holl01', 'hoev003rech01', 
    'focq001mini02', 'quin031spoo02', 'lang020arle01', 'bidl001besc01', 
    'moli015schy01', 'ling001sard01', 'rijk001hede02', 'ling001cleo01',
    'rijn001oude01', 'leeu004tove02', 'chap010mark02', 'zeve001phbl01',
    'vond001dewe08', 'foss005poly02', 'bred001moor01', 'elst004jano01',
    'smid001konr02', '_tro001fams03', '_tro001fams02', 'rulo001inwy01', 
    'vond001salm02', 'lang020chph01', 'stij003anme01', 'noms001iema01', 
    '_bru001brui01', '_jaa005196601', 'six_001mede01', 'stee033adag01', 
    'huyg001trij01', 'rivi001jeug01', 'swae001verh01', 'plui001rein01',
    'ogie002toon01', 'bred001schy01', 'bont001bele02', 'vos_002kluc01',
    'bred001luce01', 'hare003piet01', 'stee033bele01', 'boon045leid02',
    '_jaa005196701', 'bred001gria01', 'vond001pasc02', 'gaet001ontm01',
    'foss005manl01', 'asse001open01', 'huyd001achi01', 'nooz002kluc01',
    'vond001pete01', 'vond001hier01', '_tij003190901', 'swae001vcel02', 
    'vos_002mede03', 'swae001vcel01', 'expe001suri01', 'vond001pala01', 
    'wild007abra01', '_jaa005197101', 'bidl001zege01', 'bidl001kare02',
    'mira010verw02', 'corn001andr03', 'quin031agri02', 'aren001joan01',
    'ouda001haag01', 'grae002alci01', 'bidl001fabi01', 'gilb007lief01',
    'mol_014bedr01', 'lijn002vlug01', '_nie174nieu02', 'nooz003gete02', 
    'brui008verh02', 'hoge001fkhk01', 'nuyt001adme01', 'sche001mele01', 
    'bren001scha01', 'moli015inge01', 'vos_001iema03', 'zoet001meys02', 
    'lesa002kris02', 'zeer001eers01', '_vry001vrya01', 'hoev003isab01', 
    'moli015fiel02', 'raci001ifig01', 'lope001joan01', 'hoof009blyd01', 
    'lope001gedw04', 'fres003pefr01', 'noms001mich01', 'corn001cid_02',
    'corn001hora02', 'barb020tomy01', 'koni001twee01', '_tro001fams07', 
    'bidl001eerz01', 'vond001jose05', 'hoof001achi01', 'will028belg09', 
    'bie_001groe01', 'moli015bela01', 'ling001amar01', 'krul001pamp02', 
    'croi003gewa01', 'anto001gely02', 'rivi001vero01', '_tij003189201', 
    'alew001besl01', 'moli015burg01', 'corn001cinn01', 'bern001athi01', 
    'meij001verl01', 'buys001brui05', 'buys001brui04', 'buys001brui03', 
    'buys001brui02', 'lang020chpm01', 'bren001goud01', 'kalb001muli01', 
    'stee033tham01', 'berg038donj02', 'stee033andr01', 'corn001poli02', 
    'bred001kluc04', 'laan006rede01', 'boel009bedr01', 'wild007swer01', 
    'bred001stom01', 'raci001mith01', 'pels001verw02', 'vond001elek01', 
    'doms001besc03', 'bidl001vert01', 'ling001ontd01', 'hoof001geer01', 
    'sain011orak01', 'scha003leve01', 'lope001bekl02', 'sauv003maho01', 
    'marr001eeuw01', 'peys001tove01', 'gres007edua01', 'hoof002door01', 
    'vond001dewe10', 'bred001dage01', 'stij003cype01', 'vond001maeg04', 
    'plui001verl02', 'plui001verl01', 'blan049juff01', 'bidl001oper01', 
    'ross006zing01', '_qua002quae02', 'vond001dewe01', '_taf002tafe01', 
    'vos_001kluc05', '_vie002vier01', 'scha003voor01', 'vinc001leev01', 
    'raci001hest01', 'blan049aben01', 'vond001dewe02', 'corn001sert01', 
    'brui008gron01', 'moli015scho02', 'vond001dewe04', 'vond001dewe05', 
    'vond001luci01', 'scha003bela01', 'vond001dewe09', '_tro001fams08', 
    'quin031toon01', 'haps002soph02', 'bred006kris01', '_kor002kort01',
    'stee033beon01', 'feit007patr01', 'vos_002aran03', 'broe061tafe01',
    'bran002vein02', 'vond001dewe03', 'hoof001gran01', 'bred001ange01', 
    'tijs003wind01', 'stey002geve01', 'zasy001borg01', '_vla008vlae01'] 

_trial_annotation_ids = ['feit007patr01', 'hoof002door01', 'vos_002mede03']

def index(request):
    corpus = Titel.objects.filter(ti_id__in=_corpus_ids).order_by('titel')

    context = {'corpus': corpus,
               'page_title': 'Corpus'
              }

    return render(request, 'corpus/plays.html', context)

def show_title(request, title_id):
    title = get_object_or_404(Titel, pk=title_id)

    return render(request, 'corpus/title.html', {'title': title})


def show_author(request, author_id):
    author = get_object_or_404(Auteur, pk=author_id)

    return render(request, 'corpus/author.html', {'author': author})


def show_all_plays(request):
    genre_drama = Genre.objects.get(genre='Drama').titel_set
    years = [str(jaar) for jaar in range(1600, 1831)]
    select_years = reduce(operator.or_, (Q(jaar__contains=y) for y in years))
    corpus=genre_drama.filter(select_years).order_by('jaar')

    context = {'corpus': corpus,
               'page_title': 'Lijst werken met genre drama 1600-1830'
              }
    
    return render(request, 'corpus/plays.html', context)


def show_trial_annotations(request):
    corpus = Titel.objects.filter(ti_id__in=_trial_annotation_ids). \
        order_by('titel')

    context = {'corpus': corpus,
               'page_title': 'Proefannotaties'
              }

    return render(request, 'corpus/plays.html', context)


def show_year(request, year):
    corpus = Titel.objects.filter(ti_id__in=_corpus_ids) \
                  .filter(jaar__contains=year).order_by('titel')

    context = {'corpus': corpus,
               'year': year
              }

    return render(request, 'corpus/year.html', context)


def show_genres(request):
    genres = Genre.objects.filter(titel__in=_corpus_ids) \
                  .annotate(num_titles=Count('titel'))
    total_titles = Titel.objects.filter(ti_id__in=_corpus_ids).count()

    context = {'genres': genres,
               'total_titles': total_titles}

    return render(request, 'corpus/genres.html', context)
