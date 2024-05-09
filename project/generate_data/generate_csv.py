"""Process the .csv file acquired from Kaggle
"""
from typing import List
from importlib import resources
import re
import pandas as pd


def load_csv(
        path: str) -> pd.DataFrame:
    """Load .csv file as a pd.DataFrame
    """
    return pd.read_csv(path, low_memory=False)


def save_csv(
        path: str,
        df: pd.DataFrame
        ) -> None:
    """Save pd.DataFrame as .csv file
    """
    df.to_csv(path, index=False)


def get_reduced_df(
        df: pd.DataFrame
        ) -> pd.DataFrame:
    """Reduce dimension of df

    :param df: a pd.DataFrame
    :return: reduced df, pd.DataFrame
    """
    columns = ['BL record ID', 'Composer', 'Title',
               'Country of publication',
               'Publication date (standardised)',
               'Subject/genre terms']

    return df[columns]


def drop_nulls(
        df: pd.DataFrame
        ) -> pd.DataFrame:
    """Drop rows with null values

    :param df: a pd.DataFrame
    :return: reduced df, pd.DataFrame
    """
    return df.dropna().reset_index(drop=True)


def assign_dtypes(
        df: pd.DataFrame
        ) -> pd.DataFrame:
    """Assign column dtypes

    :param df: a pd.DataFrame
    :return: a pd.DataFrame
    """
    df['Publication date (standardised)'] = \
        df['Publication date (standardised)'].astype(
        'int64')

    return df.astype(
        {
            'Genre': 'object',
            'Composer std': 'object',
            'Composer info': 'object'
            }
            )


def explode_genre(
        df: pd.DataFrame
        ) -> pd.DataFrame:
    """Explode genre column

    :param df: a pd.DataFrame
    :return: exploded df wrt 'genres'
    """
    df['Genre'] = df['Subject/genre terms'].apply(lambda x: x.split(' ; '))

    df = df.drop(['Subject/genre terms'], axis=1)

    return df.explode('Genre')


def _subs_text(
        text: str
        ) -> List:
    """Find pattern in text and tag it

    tags: 'pattern' or 'Composer'
    :param text: Composer column row, str
    :return: List[text, (`pattern`|'Composer')]
    """ 
    pattern = r'\(Music[a-zA-Z\s]*\)$|(\(Composer\))$'
    found = re.search(pattern, text)

    if found:
        return [text[:found.span()[0]-2], found.group()]
    else:
        return [text, 'Else']


def simple_composer(
        df: pd.DataFrame
        ) -> pd.DataFrame:
    """Obtain 'Composer std' and 'Composer info'
    
    'Composer std' contains `Composer` info
    'Composer info' contains 'Musician' | 'Musical group'
    :param df: a pd.DataFrame
    :return: a pd.DataFrame
    """
    new_composer = df['Composer'].apply(_subs_text)

    df[['Composer std', 'Composer info']] = pd.DataFrame(
        new_composer.to_list()
        )

    df = df.drop(['Composer'], axis=1)

    return df


def main():
    PATH_INPUT = resources.path('project.data',
                                'detailedrecords.csv')
    PATH_OUTPUT = resources.path('project.data',
                                 'reduced_detailedrecords.csv')
    df = load_csv(PATH_INPUT)
    df = get_reduced_df(df).copy()
    df = drop_nulls(df)
    df = simple_composer(df)
    df = explode_genre(df)
    df = assign_dtypes(df)
    save_csv(PATH_OUTPUT, df)


if __name__ == '__main__':
    main()
