from django.db import models
from django.contrib.auth.models import User

# Modell für ein Event
class Event(models.Model):
    title = models.CharField(max_length=200)  # Titel des Events
    date = models.DateTimeField()  # Datum und Uhrzeit des Events
    description = models.TextField()  # Beschreibung des Events
    location = models.CharField(max_length=200)  # Ort des Events
    creator = models.ForeignKey(User, on_delete=models.CASCADE)  # Benutzer, der das Event erstellt hat

    def __str__(self):
        return self.title  # Gibt den Titel des Events als String zurück

# Modell für eine Einladung
class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Das Event, zu dem eingeladen wird
    inviter = models.ForeignKey(User, related_name='invitations_sent', on_delete=models.CASCADE)  # Benutzer, der die Einladung verschickt
    invitee = models.ForeignKey(User, related_name='invitations_received', on_delete=models.CASCADE)  # Benutzer, der eingeladen wird
    status = models.CharField(max_length=10, choices=[('accepted', 'Accepted'), ('declined', 'Declined'), ('pending', 'Pending')], default='pending')  # Status der Einladung

    def __str__(self):
        return f"{self.invitee.username} - {self.event.title}"  # Gibt den Benutzernamen des Eingeladenen und den Titel des Events als String zurück