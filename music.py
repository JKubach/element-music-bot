#!/usr/bin/env python3

import sys
import re
import configparser
import functions.element as element
from functions.extract_info import (
        get_title,
        get_artist_song,
        get_artist_info,
        get_tags
        )

from Naked.toolshed.shell import execute_js, muterun_js
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


def on_message(room, event):
    if event['type'] == 'm.room.message':
        if event['content']['msgtype'] == "m.text":
            if 'youtube.com' in event['content']['body'] or 'youtu.be' in event['content']['body']:
                words = event['content']['body']
                words = words.split()
                url = words[0]

                title = get_title(url)
                artist, song = get_artist_song(title)

                room.send_text(title)

                if artist:
                    tags = get_tags(artist)
                    bio = get_artist_info(artist)

                    room.send_text("Genre: " + tags)

                    room.send_text(re.sub('<.*?>', '', bio))


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
