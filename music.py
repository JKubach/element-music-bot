#!/usr/bin/env python3

import sys
import re
import configparser
import functions.element as element
from functions.extract_info import (
        get_video_info,
        get_artist_song,
        get_artist_info,
        get_tags
        )

from matrix_client.client import MatrixClient
from matrix_client.api import MatrixRequestError


def parse_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    server = config['server']
    host = server['url']
    user = server['username']
    password = server['password']
    room_id = server['room_id']

    return host, user, password, room_id


def youtube(event):
    message = event['content']['body']
    message = message.split()
    url = message[0]
    
    title, desc = get_video_info(url)
    song_info = [title]

    artist, song = get_artist_song(title)

    if artist:
        tags = get_tags(artist)
        bio = get_artist_info(artist)

        if tags and bio:
            song_info.append("Genre: " + tags)
            song_info.append(re.sub('<.*?>', '', bio))
    else:
        song_info.append(desc)

    return song_info


def send_message(room, message):
    for m in message:
        room.send_text(m)


def on_message(room, event):
    if event['type'] == 'm.room.message':
        if event['content']['msgtype'] == "m.text":
            if 'youtube.com' in event['content']['body'] or 'youtu.be' in event['content']['body']:
                message = youtube(event)
                send_message(room, message)


def main():
    host, user, password, room_id = parse_config()

    client = MatrixClient(host)

    try:
        client.login_with_password(user, password)
    except MatrixRequestError as e:
        print(e)
        sys.exit(1)

    try:
        room = client.join_room(room_id)
    except MatrixRequestError as e:
        print(e)
        sys.exit(1)

    room.add_listener(on_message)
    client.start_listener_thread()

    while True:
        msg = element.get_input()
        room.send_text(msg)


if __name__ == '__main__':
    main()
