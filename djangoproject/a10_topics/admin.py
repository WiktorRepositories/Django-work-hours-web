from django.contrib import admin
from a10_topics.models import ProjectMachines, Netzplan, Vorgang, NetzplanVorgang

# Register your models here.
admin.site.register(ProjectMachines)
admin.site.register(Netzplan)
admin.site.register(Vorgang)
admin.site.register(NetzplanVorgang)
