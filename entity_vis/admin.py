from django.contrib import admin
from entity_vis.models import Entity, Character, SpeakingTurn


class CharacterAdmin(admin.ModelAdmin):
    # There are so many plays (Titels) that it takes forever to build the
    # ForeignKey drop down, so use raw_id_fields.
    raw_id_fields = ('play',)


admin.site.register(Entity)
admin.site.register(Character, CharacterAdmin)
admin.site.register(SpeakingTurn)
