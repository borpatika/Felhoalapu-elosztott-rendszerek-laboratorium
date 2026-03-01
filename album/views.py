from django.shortcuts import render, get_object_or_404
from .models import Photo, PhotoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def photo_list(request):
    sort = request.GET.get('sort')

    if sort == 'name':
        photos = Photo.objects.all().order_by('name')
    elif sort == 'date':
        photos = Photo.objects.all().order_by('-uploaded_at')
    else:
        photos = Photo.objects.all()

    return render(request, 'album/photo_list.html', {'photos': photos})


def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'album/photo_detail.html', {'photo': photo})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('photo_list')
    else:
        form = UserCreationForm()

    return render(request, 'album/register.html', {'form': form})


@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = request.user
            photo.save()
            return redirect('my_photos')
    else:
        form = PhotoForm()
    return render(request, 'album/upload_photo.html', {'form': form})


@login_required
def my_photos(request):
    photos = Photo.objects.filter(owner=request.user)
    return render(request, 'album/my_photos.html', {'photos': photos})


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, owner=request.user)
    if request.method == 'POST':
        photo.delete()
        return redirect('my_photos')
    return render(request, 'album/confirm_delete.html', {'photo': photo})