from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 🏠 Home
    path('', views.home, name='home'),

    # 🎮 Game
    path('game/<int:id>/', views.game_detail, name='game_detail'),

    # 📌 Playlist
    path('add-to-playlist/<int:game_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('remove-from-playlist/<int:game_id>/', views.remove_from_playlist, name='remove_from_playlist'),
    path('my-playlist/', views.my_playlist, name='my_playlist'),

    # 💳 Purchase & Play
    path('purchase/<int:game_id>/', views.purchase_game, name='purchase_game'),
    path('play/<int:game_id>/', views.play_online, name='play_online'),

    # ⭐ Subscription
    path('subscribe/', views.subscribe, name='subscribe'),

    # 👤 Auth
    path('login/', auth_views.LoginView.as_view(
        template_name='games/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 📝 Signup
    path('signup/', views.signup, name='signup'),
]