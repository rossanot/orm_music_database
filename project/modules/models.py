from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Composer(Base):
    __tablename__ = 'composer'
    composer_id = Column(Integer, primary_key=True)
    composer_name = Column(String)
    tracks = relationship('Track', backref=backref('composer'))


class Track(Base):
    __tablename__ = 'track'
    track_id = Column(Integer, primary_key=True)
    composer_id = Column(Integer, ForeignKey('composer.composer_id'))
    country_id = Column(Integer, ForeignKey('country.country_id'))
    track_bl_id = Column(Integer)
    track_name = Column(String)


class Country(Base):
    __tablename__ = 'country'
    country_id = Column(Integer, primary_key=True)
    country_name = Column(String)
    tracks = relationship('Track', backref=backref('country'))




