"""
This program gathers information from the records.db
SQLite database file
Adapted from: Real Python #working-with-sqlalchemy-and-python-objects
"""
from typing import List
from importlib import resources

from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import asc, desc, func

from project.modules.models import (Composer,
                                    Track,
                                    Country,
                                    Genre)


def get_tracks_by_composer(
        session,
        ascending: bool = True
        ) -> None:
    """Get a list of tracks by composer

    Adapted from: Real Python #working-with-sqlalchemy-and-python-objects
    """
    if not isinstance(ascending, bool):
        raise ValueError(f'Sorting value invalid: {ascending}')

    direction = asc if ascending else desc

    return (
        session.query(
            Composer.composer_name,
            func.count(Track.track_name).label('total_tracks')
        )
        .join(Composer.tracks)
        .group_by(Composer.composer_name)
        .order_by(direction('total_tracks'))
    )


def get_composers(
        session,
        ascending: bool = True
        ) -> None:
    """Retrieve all composers sorted in order
    """
    if not isinstance(ascending, bool):
        raise ValueError(f'Sorting value invalid: {ascending}')

    direction = asc if ascending else desc

    return (
        session.query(Composer.composer_name)
        .order_by(direction(Composer.composer_name))
    ).all()


def add_track(session,
              new_track_name: str,
              new_composer_name: str,
              new_country_name: str,
              new_genre_name: str
              ) -> None:
    """Add a new track to the database
    """

    # check if the tracks exists
    track = (
        session.query(Track)
        .join(Composer)  # Composer.tracks
        .join(Country)
        .filter(Track.track_name == new_track_name)
        .filter(
            and_(
                Composer.composer_name == new_composer_name
            ),
            and_(Country.country_name == new_country_name)
        )
        .filter(Track.genres.any(
            Genre.genre_name == new_genre_name
            )
            )
        .one_or_none()
    )

    # Check if the track already exists
    if track is not None:
        return

    # Check if the track exists for the composer
    track = (
        session.query(Track)
        .filter(Track.track_name == new_track_name)
        .filter(
            and_(
                Composer.composer_name == new_composer_name
            ),
            and_(Country.country_name == new_country_name)
        )
        .filter(Track.genres.any(
            Genre.genre_name == new_genre_name
            )
            )
        .one_or_none()
    )

    # Create the new track if needed
    if track is None:
        track = Track(track_name=new_track_name)

    # Composer
    # Get the composer
    composer = (
        session.query(Composer)
        .filter(
            and_(
                Composer.composer_name == new_composer_name
            )
        )
        .one_or_none()
    )
    # Create composer if needed
    if composer is None:
        composer = Composer(composer_name=new_composer_name)
        session.add(composer)

    # Country
    # Get the country
    country = (
        session.query(Country)
        .filter(Country.country_name == new_country_name)
        .one_or_none()
    )
    # Create country if needed
    if country is None:
        country = Country(country_name=new_country_name)
        session.add(country)

    # Genre
    # Get the genre
    genre = (
        session.query(Genre)
        .filter(Genre.genre_name == new_genre_name)
        .one_or_none()
    )
    # Create country if needed
    if genre is None:
        genre = Genre(genre_name=new_genre_name)
        session.add(genre)

    # Initialize the track relationships
    track.country = country
    track.composer = composer
    track.genres.append(genre)
    session.add(track)

    # Commit to the database
    session.commit()


def main():
    """Main entry point of program
    """

    # Connect to the database using SQLAlchemy
    with resources.path(
        'project.data', 'records.db'
    ) as sqlite_filepath:
        engine = create_engine(f'sqlite:///{sqlite_filepath}')
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    # Get the number of tracks by each artist
    tracks_by_composers = get_tracks_by_composer(session, ascending=False)
    for row in tracks_by_composers:
        print("Composer: {:>18}, Total tracks: {:2}".format(
            row.composer_name, row.total_tracks
        ))
    
    print("\nDone retrieving total of tracks by composer\n")

    # Get composers
    composers = get_composers(session)
    for i, row in enumerate(composers):
        print('Composer {:.>4}: {:.>18}'.format(i, row.composer_name))

    print("\nDone retrieving composers\n")

    # Add a new track
    add_track(
        session,
        new_track_name='This is a song name',
        new_composer_name='Composer X',
        new_country_name='Rumania',
        new_genre_name='Electro Pop'
    )

    add_track(
        session,
        new_track_name='This is a song name',
        new_composer_name='Composer X',
        new_country_name='Rumania',
        new_genre_name='New Genre X'
    )

    print("\nDone adding new track\n")

    print('\nCheck that the new song has been added\n')
    composers = get_composers(session)
    for i, row in enumerate(composers):
        print(
            'Composer {:.>4}: {:.>18}'.format(i, row.composer_name)
            )

    print("\nDone retrieving composers\n")


if __name__ == '__main__':
    main()
