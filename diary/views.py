from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Trip, TripPhoto
from .forms import RegisterForm, TripForm, TripPhotoForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Аккаунт создан! Добро пожаловать.')
            return redirect('trip_list')
    else:
        form = RegisterForm()
    return render(request, 'diary/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('trip_list')
    else:
        form = AuthenticationForm()
    return render(request, 'diary/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def trip_list(request):
    trips = Trip.objects.select_related('author').prefetch_related('photos')
    return render(request, 'diary/trip_list.html', {'trips': trips})


def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    return render(request, 'diary/trip_detail.html', {'trip': trip})


@login_required
def trip_create(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        photo_form = TripPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.author = request.user
            trip.save()
            if photo_form.is_valid() and photo_form.cleaned_data.get('image'):
                photo = photo_form.save(commit=False)
                photo.trip = trip
                photo.save()
            messages.success(request, 'Путешествие добавлено!')
            return redirect('trip_detail', pk=trip.pk)
    else:
        form = TripForm()
        photo_form = TripPhotoForm()
    return render(request, 'diary/trip_form.html', {
        'form': form,
        'photo_form': photo_form,
        'title': 'Новое путешествие',
    })


@login_required
def trip_edit(request, pk):
    trip = get_object_or_404(Trip, pk=pk, author=request.user)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        photo_form = TripPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if photo_form.is_valid() and photo_form.cleaned_data.get('image'):
                photo = photo_form.save(commit=False)
                photo.trip = trip
                photo.save()
            messages.success(request, 'Изменения сохранены.')
            return redirect('trip_detail', pk=trip.pk)
    else:
        form = TripForm(instance=trip)
        photo_form = TripPhotoForm()
    return render(request, 'diary/trip_form.html', {
        'form': form,
        'photo_form': photo_form,
        'title': 'Редактировать путешествие',
        'trip': trip,
    })


@login_required
def trip_delete(request, pk):
    trip = get_object_or_404(Trip, pk=pk, author=request.user)
    if request.method == 'POST':
        trip.delete()
        messages.success(request, 'Путешествие удалено.')
        return redirect('trip_list')
    return render(request, 'diary/trip_confirm_delete.html', {'trip': trip})


@login_required
def my_trips(request):
    trips = Trip.objects.filter(author=request.user).prefetch_related('photos')
    return render(request, 'diary/my_trips.html', {'trips': trips})