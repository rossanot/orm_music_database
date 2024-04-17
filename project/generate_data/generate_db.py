"""
This program builds the reduced_spotify_2023 Sqlite database from the
reduced_spotify_2023.csv file
"""

import os
import csv
from importlib import resources
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.modules.models import Base
from project.modules.models import Artist
from project.modules.models import Track
from project.modules.models import Scale


def get_spotify_data(filepath):
    """
    This function gets the data from the csv file
    This function has been obtained from Real Python
    "working-with-sqlalchemy-and-python-objects"
    """
    with open(filepath) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        data = [row for row in csv_reader]
        return data


def populate_database(session, spotify_data):
    """
    This function inserts data into a Sqlite database
    This function has been adapted from Real Python
    "working-with-sqlalchemy-and-python-objects"
    """
    for row in spotify_data:

        artist = (
            session.query(Artist)
            .filter(Artist.artist_name == row['artists'])
            .one_or_none()
        )
        if artist is None:
            artist = Artist(
                artist_name=row['artists']
            )
            session.add(artist)

        track = (
            session.query(Track)
            .filter(Track.track_name == row['track_name'])
            .one_or_none()
        )
        if track is None:
            track = Track(
                track_name=row['track_name'])
            session.add(track)

        scale = (
            session.query(Scale)
            .filter(Scale.scale_key == row['key'])
            .one_or_none()
        )
        if scale is None:
            scale = Scale(
                scale_key=row['key'])
            session.add(scale)

        # add the items to the relationships
        artist.tracks.append(track)
        track.artists.append(artist)
        scale.tracks.append(track)
        session.commit()

    session.close()


def main():
    """
    This function has been adapted from Real Python
    "working-with-sqlalchemy-and-python-objects"
    """
    print("starting")

    # get the spotify data into a dictionary structure
    with resources.path(
        'project.data', 'reduced_spotify_2023.csv'
    ) as csv_filepath:
        data = get_spotify_data(csv_filepath)
        # author_book_publisher_data = data

    # get the filepath to the database file
    with resources.path(
        'project.data', 'reduced_spotify_2023.db'
    ) as sqlite_filepath:
        # remove database if it exists
        if os.path.exists(sqlite_filepath):
            os.remove(sqlite_filepath)

    # create the database
    engine = create_engine(f"sqlite:///{sqlite_filepath}")
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    populate_database(session, data)

    print("finished")


if __name__ == "__main__":
    main()