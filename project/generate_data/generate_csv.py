'''Generate a reduced version of spotify-2023.csv
'''
from typing import List
import pandas as pd


def get_df(FILE_PATH) -> pd.DataFrame:
    """Load pd.DataFrame from .csv
    """
    return pd.read_csv(
        FILE_PATH,
        encoding='latin-1')


def _get_idx_spec_char(
        df: pd.DataFrame
        ) -> List:
    """Get index of rows with special characters
    """
    series = df.loc[(df['track_name'].str.contains('ï¿½ï¿½')) |
                    (df['artist(s)_name'].str.contains('ï¿½ï¿½'))]
    return series.index.to_list()


def drop_spec_char(
        df: pd.DataFrame
        ) -> pd.DataFrame:
    """Drop rows with special characters"""
    idx = _get_idx_spec_char(df)
    return df.drop(idx)


def get_single_singer(
        df: pd.DataFrame
        ) -> pd.DataFrame:
    """Return single singer records
    """
    return df.loc[df['artist_count'] == 1]


def explode_artist(
        df: pd.DataFrame
        ) -> pd.DataFrame:
    """Explode artists column
    """
    df['artists'] = df['artist(s)_name'].apply(lambda x: x.split(', '))
    return df.explode('artists')


def save_csv(
        df: pd.DataFrame
        ):
    """Save pd.DataFrame to csv
    """
    df.to_csv(
        './project/data/reduced_spotify_2023.csv',
        index=False
        )


def main():
    FILE_PATH = './project/data/spotify-2023.csv'
    df = get_df(FILE_PATH)
    df = drop_spec_char(df).loc[:50]
    df = explode_artist(df)
    save_csv(df)


if __name__ == "__main__":
    main()
