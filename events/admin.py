from django.contrib import admin
from .models import Event, Invitation

# Registriere das Event-Modell in der Admin-Oberfläche
admin.site.register(Event)

# Registriere das Invitation-Modell in der Admin-Oberfläche
admin.site.register(Invitation)
