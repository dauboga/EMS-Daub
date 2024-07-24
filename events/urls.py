from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Definiere die URL-Muster für die Events-App
urlpatterns = [
    path('register/', views.register, name='register'), # URL für die Benutzerregistrierung
    path('create_event/', views.create_event, name='create_event'), # URL für die Eventerstellung
   # path('invite/', views.invite, name='invite'), # URL für das Versenden von Einladungen
   # path('respond_invitation/', views.respond_invitation, name='respond_invitation'), # URL für die Zu- und Absage
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('event_list/', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),  # URL für Event-Details
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),  # URL für Event-Löschung
    path('event/<int:event_id>/create_invitation/', views.create_invitation, name='create_invitation'),  # URL für Einladungserstellung
    path('event/<int:event_id>/change_status/<str:status>/', views.change_invitation_status, name='change_invitation_status'),  # URL für Statusänderung
    path('logout/', views.logout_view, name='logout'),  # Logout-URL hinzufügen
]