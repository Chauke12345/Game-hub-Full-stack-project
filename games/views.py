from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Game, Profile, Purchase
from .forms import SignUpForm


# =========================
# 🏠 HOME
# =========================
def home(request):
    games = Game.objects.all()

    owned_games = []
    if request.user.is_authenticated:
        owned_games = Purchase.objects.filter(
            user=request.user
        ).values_list('game_id', flat=True)

    return render(request, 'games/home.html', {
        'games': games,
        'owned_games': owned_games
    })


# =========================
# 🎮 GAME DETAIL
# =========================
def game_detail(request, id):
    game = get_object_or_404(Game, id=id)

    owned = False
    if request.user.is_authenticated:
        owned = Purchase.objects.filter(
            user=request.user,
            game=game
        ).exists()

    return render(request, 'games/game_detail.html', {
        'game': game,
        'owned': owned
    })


# =========================
# 📌 PLAYLIST
# =========================
@require_POST
def add_to_playlist(request, game_id):
    playlist = request.session.get('playlist', [])

    if game_id not in playlist:
        playlist.append(game_id)

    request.session['playlist'] = playlist
    return redirect('my_playlist')


def my_playlist(request):
    playlist = request.session.get('playlist', [])
    games = Game.objects.filter(id__in=playlist)

    return render(request, 'games/my_playlist.html', {'games': games})


@require_POST
def remove_from_playlist(request, game_id):
    playlist = request.session.get('playlist', [])

    if game_id in playlist:
        playlist.remove(game_id)

    request.session['playlist'] = playlist
    return redirect('my_playlist')


# =========================
# 💳 PURCHASE FLOW
# =========================
@login_required
def purchase_game(request, game_id):
    return redirect('fake_payment', game_id=game_id)


@login_required
def fake_payment(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if Purchase.objects.filter(user=request.user, game=game).exists():
        messages.info(request, "You already own this game.")
        return redirect('game_detail', id=game.id)

    if request.method == 'POST':
        Purchase.objects.create(user=request.user, game=game)
        messages.success(request, "✅ Payment successful! Game unlocked.")
        return redirect('game_detail', id=game.id)

    return render(request, 'games/payment.html', {'game': game})


# =========================
# 🎮 PLAY ONLINE (PURCHASED)
# =========================
@login_required
def play_online(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if not Purchase.objects.filter(user=request.user, game=game).exists():
        messages.error(request, "❌ You must purchase this game first.")
        return redirect('game_detail', id=game.id)

    return redirect(game.play_url)


# =========================
# ⭐ SUBSCRIPTION
# =========================
@login_required
def subscribe(request):
    profile = request.user.profile
    profile.is_subscribed = True
    profile.save()

    messages.success(request, "⭐ Subscription activated!")
    return redirect('home')


# =========================
# 🎮 PLAY (SUBSCRIPTION BASED)
# =========================
@login_required
def play_game(request, game_id):
    if not request.user.profile.is_subscribed:
        return redirect('subscribe')

    return render(request, 'games/play.html', {'game_id': game_id})


# =========================
# 👤 SIGNUP
# =========================

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            password=password
        )
        user.save()

        return redirect("login")

    return render(request, "games/signup.html")

# =========================
# 👤 AUTO CREATE PROFILE
# =========================
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        
