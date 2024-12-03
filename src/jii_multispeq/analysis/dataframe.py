"""
Helper functions for working with pandas dataframes
"""

def make_object_col (df, new_column_name):
    """
    Make a new column in a dataframe and assign it as an object type to hold arrays etc.
    Enter df, and the name of the new column
    """
    
    df[new_column_name] = 0
    df[new_column_name] = df[new_column_name].astype(object)
    return df

def add_params_to_info (info, params):
    """
    Add a new entry into the info dictionary called 'info'.
    This will be passed to any function that uses info
    """

    info['params'] = params
    return info