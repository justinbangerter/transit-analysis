import numbers
import math

import pandas as pd


def drop_empty_rows(df):
    drop_indexes = []

    is_empty = lambda x: isinstance(x, numbers.Number) and (math.isnan(x) or x == 0)
    for index, row in df.iterrows():
        is_all_empty = all([is_empty(x) for x in row])
        if is_all_empty:
            drop_indexes.append(index)

    return df.drop(drop_indexes)


def extract_alternating_value(df, column, increment=2):
    # extract alternating values from a df
    # return the df without the alternating values
    result = df.iloc[::increment, :][column].copy()
    for i, _ in result.items():
        df.at[i, column] = math.nan
    return result, df


def downshift_alternating_values(df, column, target, increment=2):
    """Move an alternating value from a given column down a row and to a new column"""
    extracted, df = extract_alternating_value(df, column, increment)
    df_extracted = pd.DataFrame(extracted).set_index(extracted.index + 1)  # shift down
    df[target] = df_extracted[column]  # add as column
    return df
