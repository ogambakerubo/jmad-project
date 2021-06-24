from rest_framework import serializers
from django.utils.text import slugify

from .models import Solo


class SoloSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Solo
        fields = ["url", "track", "artist", "instrument",
                  "start_time", "end_time", "slug"]
        read_only_fields = ("slug", )

    def validate(self, data):
        data["slug"] = slugify(data["artist"])
        return data
