import os.path

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .form import *
from django.conf import settings
from .generateMusic import generate_music

def home(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            imageFilename = request.FILES.get('image').name
            uploadFolder = os.path.join(settings.MEDIA_ROOT, 'uploads')
            imagePath = os.path.join(uploadFolder, imageFilename)
            request.session['imagePath'] = imagePath
            form.save()
            return redirect('aimusic:upload_complete')
    else:
        form = ImageForm()
    return render(request, 'aimusic/home.html', {'form': form})


def upload_complete(request):
    imagePath = request.session['imagePath']
    relativeImagePath = os.path.relpath(imagePath, 'templates/aimusic/upload_complete.html')
    return render(request, 'aimusic/upload_complete.html', {'relativeImagePath': relativeImagePath})


def music(request):
    generatedMusicPath = generate_music(request.session['imagePath'])
    relativeMusicPath = os.path.relpath(generatedMusicPath, 'templates/aimusic/music.html')
    return render(request, 'aimusic/music.html', {'relativeMusicPath': relativeMusicPath})
