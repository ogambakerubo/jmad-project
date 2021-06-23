import pdb
from django.shortcuts import render
# from django.views.generic.detail import DetailView

from rest_framework import viewsets, mixins

import musicbrainzngs as mb

from .models import Solo
from .serializers import SoloSerializer

mb.set_useragent('JMAD - http://jmad.us/', version='0.0.1')


def index(request):
    context = {"solos": []}

    if request.GET.keys():
        solos_queryset = Solo.objects.all()

        if request.GET.get("instrument", None):
            solos_queryset = solos_queryset.filter(
                instrument=request.GET.get(
                    "instrument", None
                )
            )

        # if request.GET.get("artist", None):
            # solos_queryset = solos_queryset.filter(
            #     artist = request.GET.get("artist", None)
            # )

        artist_kwarg = request.GET.get('artist', None)

        if artist_kwarg:
            solos_queryset = solos_queryset.filter(artist=artist_kwarg)

        context = {
            "solos": solos_queryset,
        }

        if context["solos"].count() == 0 and artist_kwarg:
            context["solos"] = Solo.get_artist_tracks_from_musicbrainz(
                artist_kwarg)

    return render(request, 'solos/index.html', context)

# class SoloDetailView(DetailView):
#     model = Solo


def solo_detail(request, album, track, artist):
    context = {
        "solo": Solo.objects.get(slug=artist, track__slug=track, track__album__slug=album)
    }

    return render(request, 'solos/solo_detail.html', context)


class SoloViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Solo.objects.all()
    serializer_class = SoloSerializer
