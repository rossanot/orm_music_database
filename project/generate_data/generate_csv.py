import re
import pandas as pd


def get_reduced_df(df: pd.DataFrame):
    columns = ['BL record ID', 'Composer', 'Title',
               'Country of publication',
               'Publication date (standardised)',
               'Subject/genre terms']

    return df[columns]


def drop_nulls(df):
    """_summary_

    :param df: _description_
    """
    return df.dropna().reset_index(drop=True)


def assign_dtypes(df):
    df['Publication date standardised)'] = \
        df['Publication date (standardised)'].astype(
        'int64')
    return df


def explode_genre(
        df: pd.DataFrame
        ) -> pd.DataFrame:
    """Explode genre column
    """
    df['genres'] = df['Subject/genre terms'].apply(lambda x: x.split(' ;'))
    return df.explode('genres')


def _subs_text(text):
    pattern = r'\(Music[a-zA-Z\s]*\)$'
    found = re.search(pattern, text)
    
    if found:
        return [text[:found.span()[0]], found.group()]
    else:
        return [text, 'Compositor']


def simple_composer(df):
    """Drop '(Musician)' and '(Musical group)'
    from composer and create 'Composer type'
    and 'Composer (standardised)' columns
    """
    new_composer = df['Composer'].apply(_subs_text)
    df[['Composer std', 'Composer info']] = pd.DataFrame(new_composer.to_list())
    return df


def main():
    PATH_INPUT = '../project/data/detailedrecords.csv'
    PATH_OUTPUT = '../project/data/reduced_detailedrecords.csv'
    df = pd.read_csv(PATH_INPUT)
    df = get_reduced_df(df).copy()
    df = drop_nulls(df)
    df = assign_dtypes(df)
    df = simple_composer(df)
    df.to_csv(PATH_OUTPUT, index=False)


if __name__ == '__main__':
    main()
