# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Auteur(models.Model):
    pers_id = models.CharField(primary_key=True, max_length=7)
    ppn = models.TextField(blank=True)
    ppn_oud = models.TextField(blank=True)
    achternaam = models.TextField(blank=True)
    voornaam = models.TextField(blank=True)
    voornaam_volledig = models.TextField(blank=True)
    alfabetiseer = models.TextField(blank=True)
    jaar_geboren = models.TextField(blank=True)
    jaar_overlijden = models.TextField(blank=True)
    geb_datum = models.TextField(blank=True)
    overl_datum = models.TextField(blank=True)
    geb_plaats = models.TextField(blank=True)
    overl_plaats = models.TextField(blank=True)
    lijfspreuk = models.TextField(blank=True)
    bntl_comment = models.TextField(blank=True)
    aanvullend = models.TextField(blank=True)
    lexicon = models.TextField(blank=True)
    taalcode = models.TextField(blank=True)
    taalcode_2 = models.TextField(blank=True)
    periode = models.TextField(blank=True)
    vrouw = models.TextField(blank=True)
    secundair = models.TextField(blank=True)
    letterkunde = models.TextField(blank=True)
    taalkunde = models.TextField(blank=True)
    geb_plaats_code = models.TextField(blank=True)
    geb_land_code = models.TextField(blank=True)
    overl_plaats_code = models.TextField(blank=True)
    overl_land_code = models.TextField(blank=True)
    voorvoegsel = models.TextField(blank=True)
    jeugdliteratuur = models.TextField(blank=True)
    suriname = models.TextField(blank=True)
    nonfictie = models.TextField(blank=True)
    nnbw = models.TextField(blank=True)
    nnbw_commentaar = models.TextField(blank=True)
    nnbw_deel = models.TextField(blank=True)
    nnbw_kolom = models.TextField(blank=True)
    ppn_ncc = models.TextField(blank=True)
    bio_portaal = models.TextField(blank=True)
    zuidafrika = models.TextField(blank=True)
    fries = models.TextField(blank=True)
    limburg = models.TextField(blank=True)
    buitenland = models.TextField(blank=True)
    auteursactie = models.TextField(blank=True)
    alias = models.TextField(blank=True)
    nlab = models.TextField(blank=True)
    class Meta:
        db_table = 'auteur'


    def __unicode__(self):
        return '{voornaam} {achternaam}'.format(voornaam=self.voornaam,
                                                achternaam=self.achternaam)

class Auteurxberoep(models.Model):
    pers_id = models.CharField(max_length=7, blank=True)
    beroep_id = models.CharField(max_length=2, blank=True)
    id = models.CharField(primary_key=True, max_length=5)
    class Meta:
        db_table = 'auteurxberoep'

class Auteurxorganisatie(models.Model):
    id = models.CharField(primary_key=True, max_length=3)
    pers_id = models.CharField(max_length=7, blank=True)
    dbnl_orga_id = models.CharField(max_length=14, blank=True)
    class Meta:
        db_table = 'auteurxorganisatie'

class Beeld(models.Model):
    id = models.CharField(primary_key=True, max_length=4)
    bestandsnaam = models.TextField(blank=True)
    ti_id = models.CharField(max_length=15, blank=True)
    omschrijving = models.TextField(blank=True)
    medium = models.TextField(blank=True)
    maker = models.TextField(blank=True)
    datering = models.TextField(blank=True)
    herkomst = models.TextField(blank=True)
    bron = models.TextField(blank=True)
    onderschrift = models.TextField(blank=True)
    trefwoorden = models.TextField(blank=True)
    rechten = models.TextField(blank=True)
    sortering = models.TextField(blank=True)
    pagina = models.TextField(blank=True)
    class Meta:
        db_table = 'beeld'

class Beroep(models.Model):
    beroep_id = models.CharField(primary_key=True, max_length=2)
    omschrijving = models.TextField(blank=True)
    class Meta:
        db_table = 'beroep'

class Genre(models.Model):
    genre_id = models.CharField(primary_key=True, max_length=2)
    genre = models.TextField(blank=True)
    order = models.TextField(blank=True)
    class Meta:
        db_table = 'genre'


    def __unicode__(self):
        return self.genre

class Landen(models.Model):
    land_id = models.CharField(primary_key=True, max_length=7)
    iso3166 = models.TextField(blank=True)
    exoniem_landnaam = models.TextField(blank=True)
    exoniem_officielenaam = models.TextField(blank=True)
    exoniem_hoofdstad = models.TextField(blank=True)
    exoniem_inwoneraanduiding = models.TextField(blank=True)
    exoniem_bijvnw = models.TextField(blank=True)
    endoniem_landnaam = models.TextField(blank=True)
    endoniem_officieel = models.TextField(blank=True)
    endoniem_hoofdstad = models.TextField(blank=True)
    opmerkingen = models.TextField(blank=True)
    naamsvariant = models.TextField(blank=True)
    class Meta:
        db_table = 'landen'

class Landxwerelddeel(models.Model):
    land_id = models.CharField(max_length=7)
    werelddeel_id = models.TextField(blank=True)
    class Meta:
        db_table = 'landxwerelddeel'

class Naamsvariant(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    pers_id = models.CharField(max_length=7, blank=True)
    achternaam = models.TextField(blank=True)
    voornaam = models.TextField(blank=True)
    voorvoegsel = models.TextField(blank=True)
    class Meta:
        db_table = 'naamsvariant'

class Organisatie(models.Model):
    dbnl_orga_id = models.CharField(primary_key=True, max_length=14)
    stad_dorp = models.TextField(db_column='Stad/dorp', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    kamer = models.TextField(db_column='Kamer', blank=True) # Field name made lowercase.
    topo_id = models.TextField(blank=True)
    herkomst = models.TextField(blank=True)
    stichtingsdatum = models.TextField(db_column='Stichtingsdatum', blank=True) # Field name made lowercase.
    stichtingsjaar = models.TextField(db_column='Stichtingsjaar', blank=True) # Field name made lowercase.
    gestandariseerde_naam = models.TextField(db_column='Gestandariseerde naam', blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    varianten = models.TextField(db_column='Varianten', blank=True) # Field name made lowercase.
    opheffingsdatum = models.TextField(blank=True)
    opheffingsjaar = models.TextField(blank=True)
    org_id = models.TextField(blank=True)
    voorvoegsel = models.TextField(blank=True)
    buitenland = models.TextField(blank=True)
    class Meta:
        db_table = 'organisatie'

class Subgenre(models.Model):
    subgenre = models.TextField(blank=True)
    subgenre_id = models.CharField(primary_key=True, max_length=5)
    order = models.TextField(blank=True)
    class Meta:
        db_table = 'subgenre'
    
    
    def __unicode__(self):
        return self.subgenre

class Titel(models.Model):
    ti_id = models.CharField(primary_key=True, max_length=14)
    auteurs = models.ManyToManyField(Auteur, through='Titelxauteur')
    genres = models.ManyToManyField(Genre, through='Titelxgenre')
    subgenres = models.ManyToManyField(Subgenre, through='Titelxsubgenre')
    pers_id_bk = models.CharField(max_length=7, blank=True)
    koepel_id = models.CharField(max_length=14, blank=True)
    kop_borkv_bk = models.TextField(blank=True)
    titel = models.TextField(blank=True)
    subtitel = models.TextField(blank=True)
    jaar = models.TextField(blank=True)
    druk = models.TextField(blank=True)
    vols = models.TextField(blank=True)
    uitgever = models.TextField(blank=True)
    pica_info = models.TextField(blank=True)
    borkv = models.TextField(blank=True)
    genre_bk = models.TextField(blank=True)
    genre2_bk = models.TextField(blank=True)
    subgenre = models.TextField(blank=True)
    geplaatst = models.TextField(blank=True)
    categorie = models.TextField(blank=True)
    bundelcode = models.TextField(blank=True)
    duizend = models.TextField(blank=True)
    duizend_jeugd = models.TextField(blank=True)
    scan_pagina = models.TextField(blank=True)
    scan_opmerkingen = models.TextField(blank=True)
    scan_start = models.TextField(blank=True)
    partner = models.TextField(blank=True)
    scancode = models.TextField(blank=True)
    batch = models.TextField(blank=True)
    mag_op_site = models.TextField(blank=True)
    verdacht_beeld = models.TextField(blank=True)
    x_verdacht_beeld_oud = models.TextField(blank=True)
    ppn = models.TextField(blank=True)
    signatuur = models.TextField(blank=True)
    bibliotheek = models.TextField(blank=True)
    duizend_signatuur = models.TextField(blank=True)
    duizend_complement = models.TextField(blank=True)
    duizend_romans = models.TextField(blank=True)
    dsol = models.TextField(blank=True)
    vlaams_klassiek = models.TextField(blank=True)
    limburg = models.TextField(blank=True)
    taalcode = models.TextField(blank=True)
    closed_domain = models.TextField(blank=True)
    number_2008_2012 = models.TextField(db_column='2008-2012', blank=True) # Field renamed to remove unsuitable characters. Field renamed because it wasn't a valid Python identifier.
    number_2008_2012_syn = models.TextField(db_column='2008-2012-syn', blank=True) # Field renamed to remove unsuitable characters. Field renamed because it wasn't a valid Python identifier.
    clarin = models.TextField(blank=True)
    literatuurplein_id = models.TextField(blank=True)
    limburgportaal = models.TextField(blank=True)
    class Meta:
        db_table = 'titel'
    
    
    def __unicode__(self):
        result = [self.titel]
        for auteur in self.auteurs.all():
            result.append('-')
            result.append(auteur.voornaam)
            result.append(auteur.achternaam)

        result.append('(')
        result.append(self.jaar)
        result.append(')')
        
        return ' '.join(result)

class TitelBevat(models.Model):
    ti_id = models.CharField(max_length=14, blank=True)
    parent_ti_id = models.CharField(max_length=14, blank=True)
    class Meta:
        db_table = 'titel_bevat'

class TitelCat(models.Model):
    ti_id = models.CharField(primary_key=True, max_length=14)
    categorie = models.IntegerField()
    class Meta:
        db_table = 'titel_cat'

class Titelxauteur(models.Model):
    id = models.CharField(primary_key=True, max_length=7)
    ti_id = models.ForeignKey(Titel, db_column='ti_id')
    pers_id = models.ForeignKey(Auteur, db_column='pers_id')
    class Meta:
        db_table = 'titelxauteur'

class Titelxediteur(models.Model):
    id = models.CharField(primary_key=True, max_length=4)
    ti_id = models.CharField(max_length=13, blank=True)
    pers_id = models.CharField(max_length=7, blank=True)
    class Meta:
        db_table = 'titelxediteur'

class Titelxgenre(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    ti_id = models.ForeignKey(Titel, db_column='ti_id')
    genre_id = models.ForeignKey(Genre, db_column='genre_id')
    class Meta:
        db_table = 'titelxgenre'

class Titelxillustrator(models.Model):
    id = models.CharField(primary_key=True, max_length=4)
    ti_id = models.CharField(max_length=14, blank=True)
    pers_id = models.CharField(max_length=7, blank=True)
    class Meta:
        db_table = 'titelxillustrator'

class Titelxsubgenre(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    ti_id = models.ForeignKey(Titel, db_column='ti_id')
    subgenre_id = models.ForeignKey(Subgenre, db_column='subgenre_id')
    class Meta:
        db_table = 'titelxsubgenre'

class Titelxvertaler(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    ti_id = models.CharField(max_length=14, blank=True)
    pers_id = models.CharField(max_length=7, blank=True)
    class Meta:
        db_table = 'titelxvertaler'

class Topo(models.Model):
    topocode = models.CharField(primary_key=True, max_length=8)
    std_spelling = models.TextField(blank=True)
    ligt_in = models.TextField(blank=True)
    provincie = models.TextField(blank=True)
    land = models.TextField(blank=True)
    publiceren = models.TextField(blank=True)
    kloeke_code = models.TextField(db_column='Kloeke_code', blank=True) # Field name made lowercase.
    kloeke_plaatsnaam1 = models.TextField(db_column='Kloeke_plaatsnaam1', blank=True) # Field name made lowercase.
    kloeke_plaatsnaam2 = models.TextField(db_column='Kloeke_plaatsnaam2', blank=True) # Field name made lowercase.
    x_coord = models.TextField(db_column='X_coord', blank=True) # Field name made lowercase.
    y_coord = models.TextField(db_column='Y_coord', blank=True) # Field name made lowercase.
    kloeke_provincie = models.TextField(db_column='Kloeke_provincie', blank=True) # Field name made lowercase.
    kloeke_streekaanduiding = models.TextField(db_column='Kloeke_streekaanduiding', blank=True) # Field name made lowercase.
    postcode_van = models.TextField(blank=True)
    postcode_tot = models.TextField(blank=True)
    timestamp = models.TextField(blank=True)
    commentaar = models.TextField(blank=True)
    voorvoegsel = models.TextField(blank=True)
    omschrijving = models.TextField(blank=True)
    land_id = models.CharField(max_length=7, blank=True)
    class Meta:
        db_table = 'topo'

class Werelddeel(models.Model):
    werelddeel_id = models.CharField(primary_key=True, max_length=2)
    werelddeel = models.TextField(blank=True)
    class Meta:
        db_table = 'werelddeel'

