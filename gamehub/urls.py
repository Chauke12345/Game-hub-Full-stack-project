"""
URL configuration for gamehub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from games import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    path('', include('games.urls')),

    # Home
    path('', views.home, name='home'),

    # Game
    path('game/<int:id>/', views.game_detail, name='game_detail'),

    # Playlist
    path('add-to-playlist/<int:game_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('remove-from-playlist/<int:game_id>/', views.remove_from_playlist, name='remove_from_playlist'),
    path('my-playlist/', views.my_playlist, name='my_playlist'),

    # Purchase
    path('purchase/<int:game_id>/', views.purchase_game, name='purchase_game'),
    path('payment/<int:game_id>/', views.fake_payment, name='fake_payment'),
    path('play/<int:game_id>/', views.play_online, name='play_online'),



    # Auth (🔥 THIS FIXES YOUR ERROR)
    path('login/', auth_views.LoginView.as_view(
        template_name='games/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Signup
    path('signup/', views.signup, name='signup'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('subscribe/', views.subscribe, name='subscribe'),
    path('play/<int:game_id>/', views.play_game, name='play_game'),

  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)