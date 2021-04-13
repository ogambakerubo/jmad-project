import musicbrainzngs as mb
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from albums.models import Album, Track

mb.set_useragent('JMAD - http://jmad.us', version = '0.0.1')

class Solo(models.Model):
    track = models.ForeignKey(Track, on_delete = models.CASCADE)
    artist = models.CharField(max_length = 100)
    instrument = models.CharField(max_length = 50)
    start_time = models.CharField(max_length = 20, blank = True, null = True)
    end_time = models.CharField(max_length = 20, blank = True, null = True)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("solo_detail_view", kwargs = {
            "album": self.track.album.slug,
            "track": self.track.slug,
            "artist": self.slug
        })

    def get_duration(self):
        duration_string = ""

        if self.start_time and self.end_time :
            duration_string = "{}-{}".format(self.start_time, self.end_time)

        return duration_string

    class Meta:
        ordering = ["track", "start_time"]

    # @classmethod
    # def get_artist_tracks_from_musicbrainz(cls, artist):
    #     return mb.search_artists(artist)

    @classmethod
    def get_instrument_from_musicbrainz_tags(cls, tag_list):
        """
        Return a single instrument from a list of dict-tags as returned in the MusicBrainzNGS API

        @param tag_list: a list of dicts with keys 'count' and 'name'

        @return: a string
        """

        swap = {"pianist": "piano", "bassist": "bass"}

        return swap[set(swap.keys()).intersection([tag["name"] for tag in tag_list]).pop()]

    @classmethod
    def get_artist_tracks_from_musicbrainz(cls, artist):
        """
        Create Album, Track, and Solo records for artists we find
        in the MusicBrainz API

        @param artist: an artist's name as a string to search for

        @returns Queryset of Solos
        """

        search_results = mb.search_artists(artist)
        best_result = search_results["artist-list"][0]
        instrument = Solo.get_instrument_from_musicbrainz_tags(
            best_result["tag-list"]
        )

        for album_dict in mb.browse_releases(
            best_result["id"],
            includes = ["recordings"])["release-list"]:
            
            album = Album.objects.create(
                name = album_dict["title"],
                artist = artist,
                slug = slugify(album_dict["title"])
            )

            for track_dict in album_dict["medium-list"][0]["track-list"]:
                
                track = Track.objects.create(
                    album = album,
                    name = track_dict["recording"]["title"],
                    track_number = track_dict["position"],
                    slug = slugify(
                        track_dict["recording"]["title"]
                    )
                )

                Solo.objects.create(
                    track = track,
                    artist = artist,
                    instrument = instrument,
                    slug = slugify(artist)
                )
    
        return Solo.objects.filter(artist = artist)
