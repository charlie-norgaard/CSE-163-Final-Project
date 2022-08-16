"""
Irti Haq and Charlie Norgaard
CSE 163 Final Project

This file contains functions for reformatting and cleaning our data and
for performing some stastical analysis on our data frames.
"""

import pandas as pd


def reshape_data(df, var):
    """
    Takes in a Dataframe and speficied variable and then reshapes the
    given dataframe such that years are now rows instead of columns.
    The and the year is also reformated as an int.
    The % change of the variables in question are also calculated.
    It then returns it as a dataframe
    """
    df_filt = df.melt(id_vars='Country', var_name='Year', value_name=var)
    df_filt['Year'] = df_filt['Year'].str[2:]
    df_filt = df_filt.sort_values(by=['Year'])
    df_filt[var + ' change'] = df_filt.groupby('Country')[var].pct_change()*100
    df_filt = df_filt.dropna()

    return df_filt


def merge_data(df_left, df_right):
    """
    This function takes in 2 Dataframes and merges the given data frames by
    country and year and then returns the merged dataframe
    """
    merged_df = df_left.merge(df_right, left_on=['Country', 'Year'],
                              right_on=['Country', 'Year'],
                              how='inner').sort_values(by=['Country',
                                                           'Year'],
                                                       ascending=(False, True))
    return merged_df


def get_iso_codes(df):
    """
    This function adds a new column to the given dataframe with
    the country's iso code as a dataframe.
    """
    df = df.iloc[:, [0]].copy()
    df.reset_index(inplace=True)
    iso_codes = df.rename(columns={'economy': 'iso3'})
    return iso_codes


def correlate(df, var_x, var_y):
    """
    Takes in a Dataframe and the X variable and Y varaible and then
    this function calculates the R and R^2 value by country according
    the given variables and creates two new columns for these values.
    it then returns and Dataframe with the r and r^2 values
    """
    df_corr = df.groupby('Country')[[var_x, var_y]].corr(method='pearson')
    df_corr = df_corr.unstack().iloc[:, 1].fillna(0)
    df_corr = pd.DataFrame({'Country': df_corr.index, 'R': df_corr.values})
    df_corr['R Square'] = df_corr['R'] ** 2
    df_corr['Correlation'] = (df_corr['R'] >= 0).replace({True: 'Positive',
                                                          False: 'Negetive'})
    df_corr = df_corr.append({'Country': 'Mean',
                              'R': df_corr['R'].mean(),
                              'R Square': df_corr['R Square'].mean(),
                              'Correlation': 'Mean'}, ignore_index=True)
    return df_corr


def net_change(df, var_x, var_y):
    """
    Takes in a Dataframe, a x variable and a y variable and then
    this function calculates the net change of the given variables.
    and returns a series with the net change of Var x and Var y
    """
    old = df.head(1)
    new = df.tail(1)

    if float(old[var_x]) == 0:
        net_x = 0
    else:
        net_x = (float(new[var_x]) - float(old[var_x]))/float(old[var_x])*100

    if float(old[var_y]) == 0:
        net_y = 0
    else:
        net_y = (float(new[var_y]) - float(old[var_y]))/float(old[var_y])*100

    return pd.Series({str(var_x): net_x, str(var_y): net_y})


def df_net_change(df, iso_codes, x, y):
    """
    Takes in a Dataframe, a dataframe with iso codes and
    a x variable and y variable
    This function creates a new column in the given data
    frame containing the calculated net change for x and y and then returns it
    """
    net_df = df[['Country', 'Year', x, y]]
    net_df = net_df.groupby('Country').apply(lambda z: net_change(z, x, y))
    net_df = net_df.reset_index(level=0)
    net_df = net_df.merge(iso_codes,
                          left_on='Country',
                          right_on='Country',
                          how='left')
    return net_df
