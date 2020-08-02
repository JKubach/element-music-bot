import youtube_dl
import pylast
from youtube_title_parse import get_artist_title
from functions.lastfm_init import lastfm_network

def get_title(url):
    ytdl_opts = {'source_address': '0.0.0.0'}
    ydl = youtube_dl.YoutubeDL(ytdl_opts)
    with ydl:
        video = ydl.extract_info(url, download=False)
        title = video['title']

    return title

def get_artist_song(title):
    try:
        artist, song = get_artist_title(title)
    except TypeError as e:
        artist = None
        song = None

    return artist, song

def get_artist_info(artist):
    info = lastfm_network.get_artist(artist).get_bio_summary()
    return info

def get_tags(artist):
    info = lastfm_network.get_artist(artist).get_top_tags(limit=2)
    genre_list = []
    for t in info:
        genre_list.append(t.item.get_name())

    format_tags = ', '.join(genre_list)

    return format_tags
