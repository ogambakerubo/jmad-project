from rest_framework import serializers

from .models import Album, Track


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Album
        fields = ["url", "name", "artist", "slug"]


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Track
        fields = ["url", "name", "album", "track_number", "slug"]
