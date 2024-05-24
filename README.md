## **Music Catalogue**

Highlights:
- Object-Relational Mapping Using SQLAlchemy
- Generate a SQL database from a CSV file
- Data acquisition using Kaggle API
    - [History of music (British Library)](https://www.kaggle.com/datasets/peacehegemony/history-of-music-bnb)
- SQL queries

Note: This project was inspired by/was based on [this Real Python tutorial](https://realpython.com/python-sqlite-sqlalchemy/#working-with-sqlalchemy-and-python-objects). Credits of the code are granted accordingly throughout the project.

The database that the present workflow creates has the following architecture

```mermaid
erDiagram
    COMPOSER ||--|{ TRACK : contains
    COMPOSER {
        integer composer_id PK
        string composer_name
    }
    TRACK }|--|{ COUNTRY : contains
    TRACK }|--|{ GENRE : contains
    TRACK {
        integer track_id PK
        integer composer_id FK
        integer country_id FK
        integer track_bl_id
        string track_name
    }
    COUNTRY {
        integer country_id PK
        string country_name
    }
    GENRE{
        integer genre_id PK
        string genre_name
    }

```
