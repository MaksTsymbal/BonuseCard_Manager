from django.urls import path
from . import views

urlpatterns = [
    path('card_details/<int:pk>/', views.card_details, name='card_details'),
    path('create-card/', views.create_card, name='create-card'),
    path('update-card/<int:pk>/', views.update_card, name='update-card'),
    path('all-cards/', views.all_cards, name='all-cards'),
    path('card-queue/', views.card_queue, name='card-queue'),
    path('activate-card/<int:pk>/', views.activate_card, name='activate-card'),
    path('disable-card/<int:pk>/', views.disable_card, name='disable-card'),
    path('workspace/', views.workspace, name='workspace'),
    path('all-disabled-cards/', views.all_disabled_cards, name='all-disabled-cards'),
    path('view-cards/', views.view_all_cards, name='view-cards'),
]