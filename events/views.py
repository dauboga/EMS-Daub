from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Event, Invitation
from django.http import HttpResponseBadRequest, HttpResponseForbidden

# View-Funktion für die Benutzerregistrierung
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            if User.objects.filter(username=username).exists():
                return HttpResponseBadRequest("Username already exists")
            else:
                User.objects.create_user(username=username, password=password)
                return redirect('login')
        else:
            return HttpResponseBadRequest("Username and password are required")
    return render(request, 'register.html')

# View-Funktion für die Eventerstellung
@login_required

@login_required
def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        description = request.POST.get('description')
        location = request.POST.get('location')
        if title and date and description and location:
            # Erstelle das Event
            event = Event.objects.create(
                title=title,
                date=date,
                description=description,
                location=location,
                creator=request.user
            )
            # Erstelle eine Einladung für den Ersteller des Events und setze den Status auf 'accepted'
            Invitation.objects.create(
                event=event,
                inviter=request.user,
                invitee=request.user,
                status='accepted'
            )
            return redirect('event_list')
        else:
            return HttpResponseBadRequest("All fields are required")
    return render(request, 'create_event.html')
    
# View-Funktion für das Versenden von Einladungen ## Wird noch nicht genutzt, für den Ausbau
@login_required
def invite(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        invitee_username = request.POST.get('invitee_username')
        if event_id and invitee_username:
            event = get_object_or_404(Event, id=event_id)
            invitee = get_object_or_404(User, username=invitee_username)
            Invitation.objects.create(event=event, inviter=request.user, invitee=invitee)
            return redirect('event_detail', event_id=event_id)
        else:
            return HttpResponseBadRequest("Event ID and invitee username are required")
    return render(request, 'invite.html')

# View-Funktion für die Zu- und Absage ## Wird noch nicht genutzt, für den Ausbau
@login_required
def respond_invitation(request):
    if request.method == 'POST':
        invitation_id = request.POST.get('invitation_id')
        status = request.POST.get('status')
        if invitation_id and status:
            invitation = get_object_or_404(Invitation, id=invitation_id)
            invitation.status = status
            invitation.save()
            return redirect('invitation_list')
        else:
            return HttpResponseBadRequest("Invitation ID and status are required")
    return render(request, 'respond_invitation.html')

# View-Funktion für das Login
def login_view(request):
    if request.method == 'POST':
        # 1. Benutzername und Passwort aus dem Formular abrufen
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # 2. Benutzer authentifizieren
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # 3. Benutzer anmelden
            login(request, user)
            return redirect('home')  # Passe dies an deine Startseite an
        else:
            # Füge eine Fehlermeldung hinzu, wenn die Authentifizierung fehlschlägt
            return render(request, 'login.html', {'error': 'Ungültiger Benutzername oder Passwort'})
    
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

@login_required
def event_list(request):
    created_events = Event.objects.filter(creator=request.user)
    invited_events = Event.objects.filter(invitation__invitee=request.user)
    
    events = created_events | invited_events  # Kombiniere die QuerySets
    
    context = {
        'events': events.distinct(),  # Entferne doppelte Einträge
    }
    return render(request, 'event_list.html', context)


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    invitation = Invitation.objects.filter(event=event, invitee=request.user).first()

    if request.method == "POST" and "join_event" in request.POST:
        if not invitation:
            Invitation.objects.create(event=event, inviter=event.creator, invitee=request.user, status='pending')
            return redirect('event_detail', event_id=event_id)
        else:
            return HttpResponseBadRequest("You have already been invited to this event.")

    accepted_invitees = Invitation.objects.filter(event=event, status='accepted')
    declined_invitees = Invitation.objects.filter(event=event, status='declined')

    context = {
        'event': event,
        'invitation': invitation,
        'accepted_invitees': accepted_invitees,
        'declined_invitees': declined_invitees,
    }
    return render(request, 'event_detail.html', context)

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.creator != request.user:
        return HttpResponseForbidden("You are not allowed to delete this event.")
    
    event.delete()
    return redirect('event_list')

@login_required
def change_invitation_status(request, event_id, status):
    event = get_object_or_404(Event, id=event_id)
    invitation = get_object_or_404(Invitation, event=event, invitee=request.user)
    
    if status not in ['accepted', 'declined']:
        return HttpResponseBadRequest("Invalid status")
    
    invitation.status = status
    invitation.save()
    
    return redirect('event_detail', event_id=event_id)

@login_required
def create_invitation(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if Invitation.objects.filter(event=event, invitee=request.user).exists():
        return HttpResponseBadRequest("You have already been invited to this event.")
    
    Invitation.objects.create(event=event, inviter=event.creator, invitee=request.user, status='pending')
    return redirect('event_detail', event_id=event_id)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request, 'home.html')