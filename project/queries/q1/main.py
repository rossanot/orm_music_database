"""
This program gathers information from the reduced_spotify_2023.db
SQLite database file
Adapted from: Real Python #working-with-sqlalchemy-and-python-objects
"""

from importlib import resources

from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import asc, desc, func

from project.modules.models import Artist, Track, Scale


def get_tracks_by_artists(session, ascending=True):
    """Get a list of tracks by artist

    Adapted from: Real Python #working-with-sqlalchemy-and-python-objects
    """
    if not isinstance(ascending, bool):
        raise ValueError(f'Sorting value invalid: {ascending}')

    direction = asc if ascending else desc

    return (
        session.query(
            Artist.artist_name,
            func.count(Track.track_name).label('total_tracks')
        )
        .join(Artist.tracks)
        .group_by(Artist.artist_name)
        .order_by(direction('total_tracks'))
    )


def get_artists(session, ascending=True):
    """Retrieve all artists sorted in order
    """
    if not isinstance(ascending, bool):
        raise ValueError(f'Sorting value invalid: {ascending}')

    direction = asc if ascending else desc

    return (
        session.query(Artist.artist_name)
        .order_by(direction(Artist.artist_name))
    ).all()


def add_track(session, new_track, new_artist, new_scale_id):
    """Add a new track to the database
    """

    # check if the tracks exists
    track = (
        session.query(Track)
        .join(Artist.tracks)
        .filter(Track.track_name == new_track)
        .filter(
            and_(
                Artist.artist_name == new_artist
            )
        )
        .filter(Track.scale_id == new_scale_id)
        .one_or_none()
    )

    # Does the track already exist?
    if track is not None:
        return

    # Check if the track exists for the artist
    track = (
        session.query(Track)
        .join(Artist.tracks)
        .filter(Track.track_name == new_track)
        .filter(
            and_(
                Artist.artist_name == new_artist
            )
        )
        .one_or_none()
    )
    # Create the new book if needed
    if track is None:
        track = Track(track_name=new_track)

    # Get the author
    artist = (
        session.query(Artist)
        .filter(
            and_(
                Artist.artist_name == new_artist
            )
        )
        .one_or_none()
    )
    # Do we need to create the author?
    if artist is None:
        artist = Artist(artist_name=new_artist)
        session.add(artist)

    # Get the publisher
    scale = (
        session.query(Scale)
        .filter(Scale.scale_id == new_scale_id)
        .one_or_none()
    )
    # Do we need to create the publisher?
    if scale is None:
        scale = Scale(scale_id=new_scale_id)
        session.add(scale)

    # Initialize the book relationships
    track.artists.append(artist)
    track.scale = scale
    session.add(track)

    # Commit to the database
    session.commit()


def main():
    """Main entry point of program
    """

    # Connect to the database using SQLAlchemy
    with resources.path(
        'project.data', 'reduced_spotify_2023.db'
    ) as sqlite_filepath:
        engine = create_engine(f'sqlite:///{sqlite_filepath}')
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    # Get the number of tracks by each artist
    tracks_by_artists = get_tracks_by_artists(session, ascending=False)
    for row in tracks_by_artists:
        print("Artist: {:>18}, Total tracks: {:2}".format(
            row.artist_name, row.total_tracks
        ))
    print()

    # Get artists
    artists = get_artists(session)
    for i, row in enumerate(artists):
        print('Artist {:.>4}: {:.>18}'.format(i, row.artist_name))

    # Add a new track
    add_track(
        session,
        new_track='New track name',
        new_artist='Artist X',
        new_scale_id='1',
    )

    artists = get_artists(session)
    for i, row in enumerate(artists):
        print('Artist {:.>4}: {:.>18}'.format(i, row.artist_name))


if __name__ == '__main__':
    main()
