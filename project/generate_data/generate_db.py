"""
This program builds the reduced_detailedrecords.db Sqlite
database from the reduced_detailedrecords.csv file
"""

import os
import csv
from importlib import resources
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.modules.models import Base
from project.modules.models import (Composer,
                                    Track,
                                    Country,
                                    Genre)


def load_csv_data(filepath):
    """
    This function gets the data from the csv file

    It has been sourced from Real Python
    "working-with-sqlalchemy-and-python-objects"
    """
    with open(filepath, encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        data = [row for row in csv_reader]
        return data


def populate_database(session, music_data):
    """
    This function inserts data into a Sqlite database

    It has been adapted from Real Python
    "working-with-sqlalchemy-and-python-objects"
    """
    for row in music_data[:100]:
        composer = (
            session.query(Composer)
            .filter(Composer.composer_name == row['Composer std'])
            .one_or_none()
        )
        if composer is None:
            composer = Composer(
                composer_name=row['Composer std']
            )
            session.add(composer)

        track = (
            session.query(Track)
            .filter(Track.track_name == row['Title'])
            .one_or_none()
        )
        if track is None:
            track = Track(
                track_name=row['Title'],
                track_bl_id=row['BL record ID']
                )
            session.add(track)

        country = (
            session.query(Country)
            .filter(Country.country_name == row['Country of publication'])
            .one_or_none()
        )
        if country is None:
            country = Country(
                country_name=row['Country of publication']
            )
            session.add(country)
        
        genre = (
            session.query(Genre)
            .filter(Genre.genre_name == row['Genre'])
            .one_or_none()
        )
        if genre is None:
            genre = Genre(
                genre_name=row['Genre']
                )
            session.add(genre)

        # add the items to the relationships
        composer.tracks.append(track)
        country.tracks.append(track)
        track.genres.append(genre)
        genre.tracks.append(track)
        session.commit()

    session.close()


def main():
    """
    This function has been adapted from Real Python
    "working-with-sqlalchemy-and-python-objects"
    """
    print("starting")

    # get the music data into a dictionary structure
    with resources.path(
        'project.data', 'reduced_detailedrecords.csv'
    ) as csv_filepath:
        data = load_csv_data(csv_filepath)

    # get the filepath to the database file
    with resources.path(
        'project.data', 'records.db'
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
