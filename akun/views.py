from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profil
from ujian.models import Soal


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("home")

        return render(request, "akun/login.html", {
            "error": "Username atau Password salah."
        })

    return render(request, "akun/login.html")


def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = UserCreationForm(request.POST or None)

    if request.method == "POST":
        email = request.POST.get("email")
        security_question = request.POST.get("security_question")
        security_answer = request.POST.get("security_answer")

        if form.is_valid():
            user = form.save(commit=False)
            if email:
                user.email = email
            user.save()

            # create profile with security question
            Profil.objects.create(
                user=user,
                security_question=security_question or "",
                security_answer=(security_answer or "").strip()
            )

            return redirect("login")

    return render(request, "akun/register.html", {
        "form": form
    })


@login_required
def dashboard(request):
    return redirect("home")


@login_required
def admin_panel(request):
    if not request.user.is_staff:
        return redirect("home")
    return render(request, "akun/admin_panel.html")


def logout_view(request):
    # Simpan izin gerbang jaringan (jika ada) sebelum sesi dihancurkan
    has_network_access = request.session.get('network_access_granted', False)
    logout(request)
    # Kembalikan izin gerbang jaringan agar perangkat tidak ditendang ke luar
    if has_network_access:
        request.session['network_access_granted'] = True

    return redirect("home")


# Password reset via security question - step 1: ask username
def password_reset_username(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        return redirect('password_reset_question_user', username=username)

    return render(request, 'akun/password_reset_username.html')


# Password reset via security question - step 2: show question and set new password
def password_reset_question(request, username):
    user = User.objects.filter(username=username).first()
    if not user:
        return render(request, 'akun/password_reset_username.html', {'error': 'Username tidak ditemukan.'})

    profil = Profil.objects.filter(user=user).first()
    if not profil or not profil.security_question:
        return render(request, 'akun/password_reset_username.html', {'error': 'Tidak ada pertanyaan keamanan untuk user ini.'})

    if request.method == 'POST':
        answer = (request.POST.get('security_answer') or '').strip()
        newpass = request.POST.get('new_password')
        newpass2 = request.POST.get('new_password2')

        if answer.lower() == (profil.security_answer or '').lower():
            if newpass and newpass == newpass2:
                user.set_password(newpass)
                user.save()
                return render(request, 'akun/password_reset_done_question.html')
            else:
                return render(request, 'akun/password_reset_question.html', {'username': username, 'question': profil.security_question, 'error': 'Password baru tidak cocok atau kosong.'})
        else:
            return render(request, 'akun/password_reset_question.html', {'username': username, 'question': profil.security_question, 'error': 'Jawaban salah.'})

    return render(request, 'akun/password_reset_question.html', {'username': username, 'question': profil.security_question})


def user_change_password(request):
    from django.contrib.auth import authenticate, login
    if request.method == 'POST':
        username = request.POST.get('username')
        oldpass = request.POST.get('old_password')
        newpass = request.POST.get('new_password')
        newpass2 = request.POST.get('new_password2')
        
        user = authenticate(request, username=username, password=oldpass)
        if user is None:
            return render(request, 'akun/change_password.html', {'error': 'Username atau Password lama salah.'})
            
        if newpass and newpass == newpass2:
            user.set_password(newpass)
            user.save()
            return redirect('login')
        else:
            return render(request, 'akun/change_password.html', {'error': 'Password baru tidak cocok atau kosong.'})
    return render(request, 'akun/change_password.html')
