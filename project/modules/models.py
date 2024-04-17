from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

track_artist = Table(
    'track_artist',
    Base.metadata,
    Column('track_id', Integer, ForeignKey('track.track_id')),
    Column('artist_id', Integer, ForeignKey('artist.artist_id'))
)


class Artist(Base):
    __tablename__ = 'artist'
    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String)
    tracks = relationship(
        'Track', secondary=track_artist, back_populates='artists'
        )


class Track(Base):
    __tablename__ = 'track'
    track_id = Column(Integer, primary_key=True)
    scale_id = Column(Integer, ForeignKey('scale.scale_id'))
    track_name = Column(String)
    artists = relationship(
        'Artist', secondary=track_artist, back_populates='tracks'
        )


class Scale(Base):
    __tablename__ = 'scale'
    scale_id = Column(Integer, primary_key=True)
    scale_key = Column(String)
    tracks = relationship('Track', backref=backref('scale'))
