from django.contrib import admin

from .models import *

admin.site.register(Formateur)
admin.site.register(Etudiant)
admin.site.register(Tag)
admin.site.register(Chapiter)
admin.site.register(Question)
admin.site.register(ReponseOption)

admin.site.register(Reponse)
admin.site.register(Comment)
admin.site.register(Formation)
admin.site.register(ChapiterResult)